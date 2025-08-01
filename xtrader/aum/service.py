from typing import List, Dict, Any
from datetime import timedelta
from django.utils import timezone

from django.contrib.auth.models import User
from finance.exchange.base import BaseExchangeService
from finance.exchange.factory import ExchangeServiceFactory
from aum.models import Fund, FundInvestor, FundUnitSnapshot
from finance.exchange.data import AssetBalance, Candlestick
from finance.exchange.constants.binance import BinanceRequestKeys, BinanceResponseValues
from xtrader.utils.consts import Symbol
from finance.copy_trade.service import NetAssetValueCalculator
from .exception import (
    FundNotFound, FundInvestorNotFound, InvalidAction,
    InsufficientDepositInFund, InsufficientUnitsFromInvestor
)
from utils.consts import XtraderRequestValues
from utils.unix_millis import UnixMillis

# Mostly replaces legacy Fund internal methods that held business logic.
class FundService:

    def __init__(self, fund_manager: User) -> None:
        try:
            self.fund = Fund.objects.get(manager=fund_manager)
        except Fund.DoesNotExist:
            raise FundNotFound("No Fund configured for this manager.")

    @property
    def exchange_service(self) -> "BaseExchangeService":
        return ExchangeServiceFactory.get_service_for_user(
            user=self.fund.manager
        )

    def sync_and_fetch_transactions(self, symbol_id: str = Symbol.USDT):  # replaces legacy Fund.get_transactions
        transactions = self.exchange_service.get_transactions(
            params={BinanceRequestKeys.ASSET: symbol_id}
        )
        self.fund.update_fund_balance(transactions=transactions)
        return transactions
    
    def get_assets(self) -> List[AssetBalance]:
        return self.exchange_service.get_portfolio()
    
    def sync_and_fetch_fund_assets_in_cash(self):  # replaces legacy Fund.get_cash
        assets = self.get_assets()
        usdt_asset_sum = sum(a.locked + a.free for a in assets if a.symbol == Symbol.USDT)
        _ = self.sync_and_fetch_transactions(symbol_id=Symbol.USDT)

        fund = self.fund
        net_fund_activity = fund.fee + fund.deposit + fund.withdrawal

        fund_cash = usdt_asset_sum - net_fund_activity

        net_asset_value = NetAssetValueCalculator.calculate_net_asset_value(
            exchange_service=self.exchange_service
        )
        self.fund.aum = net_asset_value - net_fund_activity
        self.fund.save(update_fields=["aum"])

        return fund_cash


    def get_fund_info(self, float_precision: int = 2) -> Dict[str, str|float|int]:
        round_func = lambda x: round(x, float_precision)

        fund_cash = self.sync_and_fetch_fund_assets_in_cash()
        fund_units_count = self.fund.get_units_count()
        nav = round_func(self.fund.aum / fund_units_count) if fund_units_count else 0
        fund_info = self.fund.get_fund_info(float_precision=float_precision)
        
        fund_info.update(
            {
                "units": fund_units_count,
                "cash": round_func(fund_cash),
                "nav": nav,
            }
        )
        fund_info.update(
            self._calc_issue_redeem_by_nav(
                nav=nav, float_precision=float_precision
            )
        )
        return fund_info
    
    def issue_redeem_unit(self, investor_id: int, unit_amount: float, action: str):
        try:
            # TODO: Assuming that each FundInvestor can only invest on a single fund?
            fund_investor = FundInvestor.objects.get(
                fund=self.fund, pk=investor_id
            )
        except FundInvestor.DoesNotExist:
            raise FundInvestorNotFound()
        
        fund_info = self.get_fund_info()
        if action == XtraderRequestValues.ISSUE:
            self._issue(
                fund_investor=fund_investor,
                units_amount=unit_amount,
                fund_info=fund_info
            )
        elif action == XtraderRequestValues.REDEEM:
            self._redeem(
                fund_investor=fund_investor,
                units_amount=unit_amount,
                fund_info=fund_info
            )
        else:
            raise InvalidAction()
        
        self.fund.save()
        fund_investor.save()

    def create_fund_unit_snapshots(self, asset_quantities: Dict[str, float], history_offset: int = 120):  # replaces legacy Fund.create_snapshots
        candles_history = self._create_candle_history(
            asset_symbol_ids=list(asset_quantities.keys()),
            history_offset=history_offset
        )
        for age in range(1, history_offset + 1):
            snapshot_data = self._create_fund_unit_snapshot_data(
                candles_history=candles_history,
                asset_quantities=asset_quantities,
                history_offset=history_offset,
                age=age
            )
            self.fund.save_fund_unit_snapshots(
                snapshot_data=snapshot_data,
                asset_quantities=asset_quantities
            )

    def init_fund_performance(self) -> bool:  # replaces legacy Fund.init_fund_performance
        snapshots = FundUnitSnapshot.objects.filter(fund=self.fund).order_by("-age")
        if snapshots:
            return "already exists"
        self.create_snapshots(assets=self.get_unit_assets(), history=history)
        return "created"


    def _issue(self, fund_investor: FundInvestor, units_amount: float, fund_info: Dict[str, str|float|int]):
        issue_nav = float(fund_info["issue"])
        nav = float(fund_info["nav"])
        fund = self.fund
        if fund.deposit >= units_amount * issue_nav:
            fund_investor.units += units_amount
            value = units_amount * issue_nav
            fund.deposit -= value
            fee = units_amount * (issue_nav - nav)
            fund.fee += fee
            fund.last_update = UnixMillis.from_dt_to_ms(dt=timezone.now())
            fund.unit_transfer(
                investor=fund_investor,
                units=units_amount,
                action=XtraderRequestValues.ISSUE,
                nav=nav,
                value=value,
                fee=fee,
            )
        else:
            raise InsufficientDepositInFund()

    def _redeem(self, fund_investor: FundInvestor, units_amount: float, fund_info: Dict[str, str|float|int]):
        redeem_nav = float(fund_info["redeem"])
        nav = float(fund_info["nav"])

        fund = self.fund
        if fund_investor.units >= units_amount:
            fund_investor.units -= units_amount
            value = units_amount * redeem_nav
            fund.withdrawal += value
            fee = units_amount * (nav - redeem_nav)
            fund.fee += fee
            fund.last_update = UnixMillis.from_dt_to_ms(dt=timezone.now())
            fund.unit_transfer(
                investor=fund_investor,
                units=units_amount,
                action=XtraderRequestValues.REDEEM,
                value=value,
                nav=nav,
                fee=fee,
            )
        else:
            raise InsufficientUnitsFromInvestor()


    def _calc_issue_redeem_by_nav(self, nav: float, float_precision: int = 2) -> Dict[str, float]:
        round_func = lambda x: round(x, float_precision)
        return  {
            "issue": round_func((1 + self.fund.issue_fee) * nav),
            "redeem": round_func((1 - self.fund.redeem_fee) * nav),
        }
    
    def _create_candle_history(
            self, asset_symbol_ids: List[str],
            history_offset: int,
        ) -> Dict[str, List[Candlestick]]:
        history = {}
        interval = BinanceResponseValues.Interval.ONE_DAY
        limit = 500

        for symbol in asset_symbol_ids:
            if symbol == Symbol.USDT:
                continue

            pair_symbol = symbol + Symbol.USDT
            candles = self.exchange_service.get_candles(
                params={
                    BinanceRequestKeys.SYMBOL: pair_symbol,
                    BinanceRequestKeys.INTERVAL: interval,
                    BinanceRequestKeys.LIMIT: limit,
                }
            )
            # excluding the last candle
            history[symbol] = candles[-(history_offset + 5) : -1]

        return history
    
    def _create_fund_unit_snapshot_data(
            self, candles_history: Dict[str, List[Candlestick]],
            asset_quantities: Dict[str, float], history_offset: int,
            age: int
        ) -> Dict[str, Any]:
        snapshot_data = {
            "age": history_offset - age + 1,
            "nav":  max(asset_quantities.get(Symbol.USDT, 0), 0)
        }

        for symbol_id, quantity in asset_quantities.items():
            if symbol_id == Symbol.USDT:
                continue
            asset_candles = candles_history.get(symbol_id, [])
            candle = asset_candles[-age]

            close_price = candle.close_price
            value = close_price * quantity

            snapshot_data.update({
                symbol_id: {"value": value}, 
                "nav": snapshot_data["nav"] + value,
                "date": UnixMillis.from_ms_to_dt(candle.open_time).date()
            })

        for symbol_id, quantity in asset_quantities.items():
            if symbol_id == Symbol.USDT:
                snapshot_data[Symbol.USDT] = {
                    "ratio": quantity / snapshot_data["nav"],
                    "value": quantity,
                }
            else:
                snapshot_data[symbol_id]["ratio"] = (
                    snapshot_data[symbol_id]["value"] / snapshot_data["nav"]
                )

            if "date" not in snapshot_data:
                usdt_date = timezone.now() - timedelta(
                    days=age - 2
                )
                snapshot_data["date"] = usdt_date.date()
        return snapshot_data