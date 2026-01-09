from finance.models import Exchange, TradingViewIntegration
from django.contrib.auth.models import User
from .factory import ExchangeServiceFactory


class XtraderExchangeService:

    @staticmethod
    def remove_exchange(trader: User, name: str) -> bool:
        exchange = Exchange.objects.filter(trader=trader, name=name)
        if not exchange.exists():
            return False
        
        trading_vieww = TradingViewIntegration.objects.filter(trader=trader)
        if trading_vieww.exists():
            return False
        
        exchange.delete()
        return True
    
    @staticmethod
    def verify_and_create_exchange(trader: User, kwargs: dict) -> bool:
        valid_fields = {k: v for k, v in kwargs.items() if hasattr(Exchange, k)}
        exchange = Exchange.objects.create(trader=trader, **valid_fields)
        exchange_service = ExchangeServiceFactory.get_service(exchange=exchange)
        if exchange_service.has_spot_trading_permission():
            return True
        exchange.delete()
        return False
    

xtrader_exchange_service = XtraderExchangeService()
