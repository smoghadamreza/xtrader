import time
from datetime import datetime

from data import jalali, redis
from data.models import StockWatch


def to_timestamp(date, mode):
    if mode == "farabi":
        return fix_date_farabi(date)
    if mode == "mabna":
        return fix_date_mabna(date)


def fix_date_mabna(date):
    jdate = "{}/{}/{}".format(date[:4], date[4:6], date[6:8])
    gorgeain_date = jalali.Persian(jdate).gregorian_string("{}/{}/{}")
    hour = int(date[8:10]) if int(date[8:10]) < 13 else 12
    minute = int(date[10:12])
    second = int(date[12:14])
    utc_min = minute - 30
    utc_hour = hour + 5
    if utc_min < 0:
        utc_min += 60
        utc_hour -= 1
    dt = datetime.strptime(gorgeain_date, "%Y/%m/%d").replace(
        hour=utc_hour, minute=utc_min, second=second
    )
    timestamp = time.mktime(dt.timetuple())
    return 1000 * timestamp


def fix_date_farabi(date):
    year = int(date[:4])
    month = int(date[5:7])
    day = int(date[8:10])
    hour = int(date[11:13]) if int(date[11:13]) < 13 else 12
    minute = int(date[14:16])
    second = int(date[17:])
    utc_min = minute - 30
    utc_hour = hour + 5
    if utc_min < 0:
        utc_min += 60
        utc_hour -= 1
    utc_date = datetime(
        year=year,
        month=month,
        day=day,
        hour=utc_hour,
        minute=utc_min,
        second=second,
    ).timetuple()
    timestamp = time.mktime(utc_date)
    return 1000 * timestamp


def to_str(date):
    return str(date)[:10]


class Check:
    now = datetime.now()

    def day(self):
        return self.now.weekday() not in [3, 4]

    def time(self):
        market_time = True
        state = "at market"
        if self.now < self.now.replace(hour=8, minute=30):
            market_time = False
            state = "before market"
        if self.now > self.now.replace(hour=12, minute=30):
            market_time = False
            state = "after market"
        return {"market_time": market_time, "state": state}

    def last_market(self):
        last_day = StockWatch.objects.order_by("-LastTradeDate").first()
        last_day = to_str(last_day.LastTradeDate)
        return last_day

    def find_the_last_day(self):
        for delta in range(10):
            if StockWatch.objects.filter(
                LastTradeDate=self.strdate()
            ).exists():
                return self.strdate()
        return None

    def strdate(self):
        return str(self.now)[:10]

    def is_history_updated(self):
        last_market = StockWatch.objects.order_by("-LastTradeDate").first()
        SymbolId = last_market.SymbolId
        last_market_date = to_str(last_market.LastTradeDate)
        last_historical_date = redis.hget(SymbolId, "date")[-1]
        last_historical_date *= 0.001
        last_historical_date = datetime.utcfromtimestamp(last_historical_date)
        last_historical_date = to_str(last_historical_date)
        return last_historical_date == last_market_date
