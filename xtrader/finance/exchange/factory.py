from django.http import HttpRequest

from finance.models import Exchange, ExchangeType
from .base import BaseExchangeService
from binance.service import BinanceService

class ExchangeServiceFactory:
    @classmethod
    def get_service(cls, exchange: Exchange) -> BaseExchangeService:
        if exchange.type == ExchangeType.BINANCE:
            return BinanceService(exchange=exchange)
        raise NotImplementedError(f"Exchange service not implemented for {exchange.type}")

    @classmethod
    def get_service_for_user(cls, user) -> BaseExchangeService:
        exchange = Exchange.objects.filter(trader=user).first()
        if not exchange:
            raise ValueError("No exchange configured for this user")
        return cls.get_service(exchange)

    @classmethod
    def get_service_from_request(cls, request: HttpRequest) -> BaseExchangeService:
        if not request.user:
            raise ValueError("can't offer service for empty user")
        return cls.get_service_for_user(request.user)
