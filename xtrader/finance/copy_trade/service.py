import threading
from django.utils import timezone
from django.contrib.auth.models import User
from typing import cast, List, Dict, Any
from social.models import ProTrader, Follow
from finance.exchange.base import BaseExchangeService
from finance.exchange.data import (
    OrderRequestData, OrderType
)
from finance.exchange.factory import ExchangeServiceFactory
from finance.exchange.constants.binance import BinanceRequestKeys
from django.db import connections
from .data import CopyTradeOrderAction, CopyTradeOrderData

    
class CopyTradeService:
    def __init__(self, pro_trader_id: int) -> None:
        try:
            self._pro_trader = ProTrader.objects.get(pk=pro_trader_id)
        except ProTrader.DoesNotExist:
            raise ValueError(f"there is no ProTrader with id: {pro_trader_id}")

        self._followers_exchange_services: List[BaseExchangeService] = self._get_followers_exchange_services()
        self._pro_trader_exchange_service = ExchangeServiceFactory.get_service_for_user(user=self._pro_trader)
        self._market_service = self._pro_trader_exchange_service.market_service
        self._validate()


    def copy_trade(self, order_params: Dict[str, Any]):
        order = self._prepare_copy_trade_data(order_params=order_params)
        self._apply_copy_trade_for_followers(order=order)


    def _apply_copy_trade_for_followers(self, order: CopyTradeOrderData):
        threads = []
        for follower_ex_svc in self._followers_exchange_services:
            if order.order_action == CopyTradeOrderAction.NEW:
                threads.append(
                    threading.Thread(
                        target=self._send_followers_order,
                        args=(follower_ex_svc, order),
                    )
                )
            elif order.order_action == CopyTradeOrderAction.CANCEL:
                threads.append(
                    threading.Thread(
                        target=follower_ex_svc.cancel_all_orders,
                        args=(order.request_data.symbol),
                    )
                )
            else:
                print("invalid action")
        for t in threads:
            t.start()


    def _send_followers_order(self, follower_ex_svc: BaseExchangeService, order: CopyTradeOrderData):
        nav = NetAssetValueCalculator.calculate_net_asset_value(exchange_service=follower_ex_svc)

        value = max(nav * order.nav_ratio, 0)
        price = cast(float, order.request_data.price)
        quantity = value / (price * order.quote_price)
        if quantity * price * order.quote_price >= 10:
            order.request_data.quantity = quantity
            follower_ex_svc.send_order(params=order.request_data.to_dict())
        for conn in connections.all():
            conn.close()
    
    def _prepare_copy_trade_data(self, order_params: dict) -> CopyTradeOrderData:
        order = CopyTradeOrderData()

        request_data = OrderRequestData.loads(params=order_params)
        request_data.validate()

        order.request_data = request_data

        symbol_info = self._market_service.get_symbol_info(
            symbol_id=request_data.symbol
        )

        order.base_asset = symbol_info.base_asset
        order.quote_asset = symbol_info.quote_asset
        order.quote_price = self._market_service.get_assets_prices(
            assets_symbol_ids=[symbol_info.quote_asset]
        ).get(symbol_info.quote_asset, CopyTradeOrderData.UNAVAILABLE_PRICE)

        order_market_value = 0
        if request_data.type == OrderType.MARKET:
            request_data.price = self._market_service.get_last_price(symbol_id=request_data.symbol)
            order_market_value = float(order_params[BinanceRequestKeys.ORDER_MARKET_VALUE])
        elif request_data in {OrderType.STOP_LOSS, OrderType.TAKE_PROFIT}:
            request_data.price = request_data.stop_price
            order_market_value = float(order_params[BinanceRequestKeys.ORDER_MARKET_VALUE])

        order.order_market_value = order_market_value
        order.order_action = order_params[BinanceRequestKeys.ORDER_ACTION]
        if order_params[BinanceRequestKeys.ORDER_ACTION] == CopyTradeOrderAction.NEW:
            order.nav_ratio = NetAssetValueCalculator.order_net_asset_value_ratio(
                order=order, exchange_service=self._pro_trader_exchange_service
            )

        return order

    def _get_followers_exchange_services(self):
        followers = Follow.objects.filter(
            prot_trader=self._pro_trader,
            expiry__gte=timezone.now()
        ).values_list('follower', flat=True)
        followers = cast(List[User], followers)
        
        return [
            ExchangeServiceFactory.get_service_for_user(user=follower)
            for follower in followers
        ]
    
    def _validate(self) -> None:
        # We are assuming that copy-trade only is available on same exchange types
        if not all(
            self._pro_trader_exchange_service.__class__ == ex_svc.__class__
            for ex_svc in self._followers_exchange_services
        ):
            raise ValueError("copy trading must not be avialable cross exchange")

class NetAssetValueCalculator:

    @classmethod
    def calculate_net_asset_value(cls, exchange_service: BaseExchangeService) -> float:  # replaces get_nav in legacy OMS
        assets = exchange_service.get_portfolio()
        asset_prices = exchange_service.get_assets_prices(
            assets_symbol_ids=[asset.symbol for asset in assets]
        )
        net_asset_value = 0
        for asset in assets:
            if asset.symbol not in asset_prices:
                raise ValueError(f"symbol {asset.symbol} has no price")
            amount = asset.free + asset.locked
            unit_price = asset_prices[asset.symbol]
            net_asset_value += amount * unit_price
        return net_asset_value
    
    @classmethod
    def order_net_asset_value_ratio(cls, order: CopyTradeOrderData, exchange_service: BaseExchangeService):  # replaces legacy OMS.order_nav_ratio
        nav = cls.calculate_net_asset_value(exchange_service=exchange_service)
        if order.order_market_value > 0:
            order_value = order.order_market_value
        else:
            order_price = cast(float, order.request_data.price)
            order_quantity = order.request_data.quantity
            order_value = order_quantity * order_price * order.quote_price
        return round(order_value / nav, 3)
