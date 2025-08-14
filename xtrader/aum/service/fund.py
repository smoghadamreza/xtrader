from typing import List, Dict, Any
from datetime import timedelta
from django.utils import timezone

from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from finance.exchange.base import BaseExchangeService
from finance.exchange.factory import ExchangeServiceFactory
from aum.models import Fund, FundInvestor, FundUnitSnapshot
from finance.exchange.data import AssetBalance, Candlestick
from finance.exchange.constants.binance import BinanceRequestKeys, BinanceRequestValues
from xtrader.utils.consts import Symbol
from finance.copy_trade.service import NetAssetValueCalculator
from aum.exception import (
    FundNotFound, FundInvestorNotFound, InvalidAction,
    InsufficientDepositInFund, InsufficientUnitsFromInvestor,
    NoSnapshotFound
)
from aum.service.data import FundPerformanceSnapshot 
from utils.consts import XtraderRequestValues
from utils.unix_millis import UnixMillis
from django.db import connections, close_old_connections


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
    
    @classmethod
    def create_today_snapshots(cls):
        close_old_connections()

        funds = Fund.objects.all()
        for fund in funds:
            service = cls.from_fund(fund=fund)
            if FundUnitSnapshot.objects.filter(fund=fund).exists():
                service._create_today_snapshot()
            else:
                service.init_fund_performance()
        
        connections.close_all()

    @classmethod
    def from_fund(cls, fund: Fund) -> "FundService":
        obj = cls.__new__(cls)  # create instance without calling __init__
        obj.fund = fund
        return obj

    def sync_and_fetch_transactions(self, symbol_id: str = Symbol.USDT):  # replaces legacy Fund.get_transactions
        transactions = self.exchange_service.get_transactions(
            params={BinanceRequestKeys.ASSET: symbol_id}
        )
        self.fund.update_fund_balance(transactions=transactions)
        return transactions
    
    def get_assets(self) -> List[AssetBalance]:
        return self.exchange_service.get_portfolio()
    
    def sync_and_fetch_fund_assets_in_cash(self) -> float:  # replaces legacy Fund.get_cash
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

    def init_fund_performance(self, history_offest: int = 120) -> bool:  # replaces legacy Fund.init_fund_performance
        snapshots = self._get_sorted_fund_snapshots(ascending=False)
        if snapshots:
            return False
        self.create_fund_unit_snapshots(
            asset_quantities=self._get_unit_assets(),
            history_offset=history_offest
        )
        return True

    def get_fund_performance(self, mode: str = XtraderRequestValues.ALL, history_offset: int = 120):
        """
        Retrieve fund performance data over time.

        :param mode: "all" for fund + BTC, "fund" for fund NAV only, "btc" for BTC prices only.
        :param history_offset: Number of historical entries to return.
        """
        snapshots = self._get_sorted_fund_snapshots().values("age", "nav", "insert_date")
    
        fp_snapshots: List[FundPerformanceSnapshot] =\
            self._calculate_fund_returns(snapshots=snapshots)
        fp_snapshots = fp_snapshots[-history_offset:] 

        if mode == XtraderRequestValues.FUND:
            return self._format_for_chart(fp_snapshots=fp_snapshots, key="nav")

        btc_prices = self._fetch_btc_prices(required_count=len(fp_snapshots))
        self._add_btc_returns(fp_snapshots, btc_prices)

        if mode == XtraderRequestValues.BTC:
            return self._format_for_chart(fp_snapshots, "btc")

        return fp_snapshots[::-1]
    
    def get_investors_info(self) -> list[dict]:
        investors = FundInvestor.objects.filter(fund=self.fund)
        return [
            {
                "id": investor.pk,
                "name": f"{investor.first_name} {investor.last_name}",
                "units": investor.units,
                "national_code": investor.national_code,
            }
            for investor in investors
        ]


    def _create_today_snapshot(self) -> None:
        last_snapshot = self._get_last_snapshot_or_raise()

        if self._is_today_snapshot(last_snapshot["insert_date"]):
            return

        age = last_snapshot["age"] + 1
        asset_quantities = self._get_unit_assets()
        prices = self.exchange_service.get_assets_prices(
            assets_symbol_ids=list(asset_quantities.keys())
        )
        nav = self._calculate_nav(asset_quantities, prices)

        self._save_snapshots(asset_quantities, prices, nav, age)

    def _calculate_fund_returns(self, snapshots) -> list[FundPerformanceSnapshot]:
        fund_returns = []
        last_age = -1
        previous_nav = None

        for snapshot in snapshots:
            if snapshot["age"] <= last_age:
                continue
            last_age += 1

            if previous_nav is None:
                previous_nav = snapshot["nav"]
                continue

            nav_change = (snapshot["nav"] / previous_nav) - 1
            previous_nav = snapshot["nav"]

            fund_returns.append(FundPerformanceSnapshot(
                age=snapshot["age"],
                nav=round(snapshot["nav"], 2),
                date=snapshot["insert_date"],
                return_percentage=100 * round(nav_change, 3)
            ))
        return fund_returns

    def _fetch_btc_prices(self, required_count: int):
        """Fetch historical BTCUSDT daily close prices."""

        candles = self.exchange_service.get_candles(
            params={
                BinanceRequestKeys.SYMBOL: Symbol.BTCUSDT,
                BinanceRequestKeys.INTERVAL: BinanceRequestValues.Interval.ONE_DAY,
                BinanceRequestKeys.LIMIT: 500
            }
        )

        # Take enough BTC prices to match fund_returns length
        return [c.close_price for c in candles[-required_count - 2 : -1]]

    def _add_btc_returns(self, fp_snapshots: List[FundPerformanceSnapshot], btc_prices: List[float]):
        """Add BTC prices and returns to fp_snapshots."""
        if not btc_prices:
            raise ValueError("btc_prices cannot be empty")

        previous_price = btc_prices[0]
        for idx, price in enumerate(btc_prices[1:], start=1):
            fp_snapshots[idx - 1].btc = price
            fp_snapshots[idx - 1].btc_return_percentage = 100 * round((price / previous_price) - 1, 3)
            previous_price = price

    def _format_for_chart(self, fp_snapshots: List[FundPerformanceSnapshot], key: str):
        """Format fp_snapshots for chart plotting."""
        return [
            [UnixMillis.from_date_to_ms(fps.date), getattr(fps, key)]
            for fps in fp_snapshots
        ]

    def _get_unit_assets(self) -> Dict[str, float]:  # replaces legacy Fund.get_unit_assets  
        assets: List[AssetBalance] = self.get_assets()
        fund_cash = self.sync_and_fetch_fund_assets_in_cash()
        units_count = self.fund.get_units_count()
        fund_assets = {
            asset.symbol: asset.free + asset.locked
            for asset in assets
            if not asset.symbol == Symbol.USDT
        }
        fund_assets[Symbol.USDT] = fund_cash
        return {
            symbol: quantity / units_count
            for symbol, quantity in fund_assets.items()
        }

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
        interval = BinanceRequestValues.Interval.ONE_DAY
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
    
    def _get_sorted_fund_snapshots(self, ascending: bool = True) -> QuerySet[FundUnitSnapshot]:
        order_key = "age" if ascending else "-age"
        return FundUnitSnapshot.objects.filter(fund=self.fund).order_by(order_key)
    
    def _get_last_snapshot_or_raise(self):
        last_snapshot = (
            self._get_sorted_fund_snapshots(ascending=False)
            .values("age", "insert_date")
            .first()
        )
        if last_snapshot is None:
            raise NoSnapshotFound()
        return last_snapshot

    def _is_today_snapshot(self, insert_date):
        today = timezone.datetime.today().date()
        return insert_date == today

    def _calculate_nav(self, asset_quantities, prices):
        return sum(prices[asset] * qty for asset, qty in asset_quantities.items())

    def _save_snapshots(self, asset_quantities, prices, nav, age):
        insert_date = timezone.datetime.today()
        for asset, quantity in asset_quantities.items():
            value = quantity * prices[asset]
            ratio = value / nav
            FundUnitSnapshot(
                fund=self,
                asset=asset,
                quantity=quantity,
                value=value,
                ratio=ratio,
                insert_date=insert_date,
                age=age,
                nav=nav,
            ).save()