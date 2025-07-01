import inspect
import threading

import numpy as np
import pandas as pd
from django.contrib.auth.models import User
from django.db import connections

from accounts.models import Profile, Wallet
from data.models import StockWatch
from finance import notification
from finance import strategy as strategyModule
from finance.models import Strategy
from sales.models import Payment, Subscription

from . import data_handling as dh

all_functions = dict(inspect.getmembers(dh, inspect.isfunction))


def screener(interval):
    users = set(strategy.trader for strategy in Strategy.objects.all())
    for user in users:
        profile = Profile.objects.filter(user=user).first()
        if profile and profile.telegram_id:
            if (
                strategyModule.get_strategy_counts(user)
                > strategyModule.get_pack_limit(user)["strategy"]
            ):
                notification.send_telegram_message(
                    msg="کاربر گرامی اشتراک شما به اتمام رسیده است",
                    user_id=profile.telegram_id,
                )
                continue
            wallet = Wallet.objects.filter(user=user).first()
            strategy_list = Strategy.objects.filter(
                trader=user, interval=interval
            )
            for strategy in strategy_list:
                watchlist_id = strategy.get_strategy_watchlist_id()
                watchlist_name = "پیش فرض"
                if watchlist_id > 0:
                    subscription = Subscription.have_subscribe(user=user)
                    if not subscription:
                        notification.send_telegram_message(
                            msg="کاربر گرامی اشتراک شما به اتمام رسیده است",
                            user_id=profile.telegram_id,
                        )
                        break
                    watchlist_name = strategy.watchlist.name
                    strategy_params = strategy.loads()
                    gas_fee = (
                        len(strategy_params["filters"])
                        * len(strategy_params["symbols"])
                        * subscription.package.gas_fee
                    )
                    if not wallet or not Payment.pay(
                        wallet=wallet,
                        amount=gas_fee,
                        action="pay",
                        reason="اسکن بازار",
                        pay2ref=True,
                    ):
                        notification.send_telegram_message(
                            msg="کاربر گرامی موجودی کیف پول شما برای پرداخت هزینه اسکن بازار کافی نیست",
                            user_id=profile.telegram_id,
                        )
                        break
                t = threading.Thread(
                    target=scan_thread,
                    args=(
                        strategy.trader.username,
                        strategy.name,
                        strategy.id,
                        profile.telegram_id,
                        interval,
                        watchlist_id,
                        watchlist_name,
                    ),
                )
                t.start()
    for conn in connections.all():
        conn.close()


def scan_thread(
    username,
    strategy_name,
    strategy_id,
    telegram_id,
    interval,
    watchlist_id,
    watchlist_name,
):
    result = scan_market(username, strategy_id, former=False)
    msg = "نتیجه اسکن بازار برای استراتژی {}:".format(strategy_name) + "\n"
    msg += "واچ‌لیست: {}".format(watchlist_name) + "\n"
    msg += "تایم‌فریم: {}".format(interval) + "\n"
    if result["buy"]:
        msg += "سیگنال خرید:" + "\n"
        symbols = result["buy"]
        for symbol in symbols:
            msg += symbol["symbol_id"] + "\n"
            msg += "https://ramzservat.com/spot/" + symbol["symbol_id"] + "\n"
    if result["sell"]:
        msg += "سیگنال فروش:" + "\n"
        symbols = result["sell"]
        for symbol in symbols:
            msg += symbol["symbol_id"] + "\n"
            msg += "https://ramzservat.com/spot/" + symbol["symbol_id"] + "\n"
    if not result["sell"] and not result["buy"]:
        msg += "سیگنالی وجود ندارد" + "\n"
    if watchlist_id == 0:
        msg += "کاربر گرامی با ارتقا اشتراک خود می‌توانید واچ‌لیست‌های شخصی و بیش از یک استراتژی بسازید. "
    notification.send_telegram_message(msg=msg, user_id=telegram_id)
    for conn in connections.all():
        conn.close()


def scan_market(user_name, strategy_id, former=True):
    filters, interval, symbol_ids = find_strategy_filters(
        user_name, strategy_id
    )
    scan_result = {"buy": [], "sell": []}
    for id_index, symbol_id in enumerate(symbol_ids):
        first_kind_dict, second_kind_dict, final_dict = {}, {}, {}
        first, second, bad_symbol = False, False, False
        for index, strategy_filter in enumerate(filters):
            strategy_filter["symbol_id"] = symbol_id
            try:
                result = calculate_filter_result(
                    strategy_filter, interval=interval
                )
            except Exception as e:
                print(e)
                print(
                    "bad symbol !! filter: {}, for symbol: {}".format(
                        index, id_index
                    )
                )
                bad_symbol = True
                continue
            if result["type"] == "first":
                first_kind_dict["filter-first {}".format(index)] = (
                    make_list_ready(result["result"])
                )
                first = True
            if result["type"] == "second":
                second_kind_dict["filter-second {}".format(index)] = (
                    make_list_ready(result["result"])
                )
                second = True
        if first:
            final_dict["first"] = check_first_kind(first_kind_dict)
        if second:
            final_dict["second"] = check_second_type(second_kind_dict)
        if not bad_symbol:
            final = final_check(final_dict)
            if not final[-1] == final[-2] or former:
                if final[-1] == 1:
                    scan_result["buy"].append(create_dict(symbol_id))
                    if not first:
                        scan_result["sell"].append(create_dict(symbol_id))
                if final[-1] == -1:
                    scan_result["sell"].append(create_dict(symbol_id))
    return scan_result


def find_strategy_filters(user_name, strategy_id):
    trader = User.objects.get_by_natural_key(username=user_name)
    strategy = Strategy.objects.get(trader=trader, id=strategy_id).loads()
    return strategy["filters"], strategy["interval"], strategy["symbols"]


def find_symbol_ids():
    symbol_ids = StockWatch.objects.all().values("SymbolId")
    return [symbol_id["SymbolId"] for symbol_id in symbol_ids]


def calculate_filter_result(strategy_filter, interval):
    function = all_functions["give_result_" + strategy_filter["kind"].lower()]
    return eval(function(strategy_filter, interval=interval))


def create_dict(symbol_id):
    return {"symbol_id": symbol_id}


def check_first_kind(results):
    magic_number = len(results)
    first = pd.DataFrame(results)
    result = first.sum(axis=1)
    check = result.apply(
        lambda x: 0 if (x < magic_number and x > -magic_number) else x
    )
    check = check.replace([magic_number, -magic_number], [1, -1])
    return np.asarray(check)


def check_second_type(results):
    second = pd.DataFrame(results)
    result = second.product(axis=1)
    return np.asarray(result)


def final_check(final_dict):
    df = pd.DataFrame(data=final_dict)
    return np.asarray(df.product(axis=1))


def make_list_ready(unready_list):
    return [x[0] for x in eval(unready_list)]
