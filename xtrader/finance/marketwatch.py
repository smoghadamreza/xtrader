from utils.dates import Check
from data.models import StockWatch as MarketWatch

keys = {
    "InstrumentName": "نماد",
    "InstrumentTitle": "نام",
    "TotalNumberOfTrades": "تعداد",
    "TotalNumberOfSharesTraded": "حجم",
    "TotalTradeValue": "ارزش معاملات",
    "PreviousDayPrice": "دیروز",
    "FirstTradePrice": "اولین",
    "LastTradePrice": "آخرین",
    "ClosingPrice": "پایانی",
    "LowestTradePrice": "کمترین",
    "HighestTradePrice": "بیشترین",
    "Eps": "Eps",
    "PricePerEarning": "P/E",
    "SymbolId": "symbol_id",
}

trans = {
    # yesterday price
    "(py)": "PreviousDayPrice",
    "(pf)": "FirstTradePrice",
    "(pmin)": "LowestTradePrice",
    "(pmax)": "HighestTradePrice",
    "(pl)": "LastTradePrice",
    "(plc)": "ReferencePriceVariation",
    "(plp)": "ReferencePriceVariationPercent",
    "(pc)": "ClosingPrice",
    "(pcc)": "ClosingPriceVariation",
    "(pcp)": "ClosingPriceVariationPercent",
    "(tmin)": "LowerPriceThreshold",
    "(tmax)": "UpperPriceThreshold",
    "(eps)": "Eps",
    "(pe)": "PricePerEarning",
    "(z)": "NumberOfSharesOrBonds",
    # industry group
    "(bvol)": "BaseQuantity",
    "(tvol)": "TotalNumberOfSharesTraded",
    "(tno)": "TotalNumberOfTrades",
    "(tval)": "TotalTradeValue",
    "(ct).Buy_CountI": "BuyIndividualCount",
    "(ct).Buy_CountN": "BuyFirmCount",
    "(ct).Sell_CountI": "SellIndividualCount",
    "(ct).Sell_CountN": "SellFirmCount",
    "(ct).Buy_I_Volume": "BuyIndividualVolume",
    "(ct).Buy_N_Volume": "BuyFirmVolume",
    "(ct).Sell_I_Volume": "SellIndividualVolume",
    "(ct).Sell_N_Volume": "SellFirmVolume",
    "(mv)": "InstrumentMarketValue",
    # logical:
    "&&": "AND",
    "& &": "AND",
    "||": "OR",
    "| |": "OR",
}


def query(query_text):
    date = Check().last_market()
    query_text = translate(query_text)
    query_text = "SELECT * FROM api_MarketWatch WHERE {} ORDER BY TotalNumberOfSharesTraded DESC".format(
        query_text
    )
    results = MarketWatch.objects.raw(query_text)
    r = []
    for result in results:
        if result.dict(keys, date) != "wrong symbol":
            r.append(result.dict(keys, date))
    return {"keys": keys, "result": r}


def translate(query_text):
    for key in trans:
        query_text = query_text.replace(key, trans[key])
    return query_text
