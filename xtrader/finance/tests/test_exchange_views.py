import json
import pytest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.http import JsonResponse

from finance.views.exchange_views import (
    trade,
    portfolio,
    get_orders,
    cancel_order,
    get_exchanges,
    save_exchange,
    remove_exchange,
)
from finance.services.exchange.constants.binance import BinanceRequestKeys
from finance.exceptions import NoConnectedExchangeException
from utils.consts import XtraderResponseKeys, XtraderRequestKeys, XtraderResponseMessages


@pytest.mark.django_db
class TestFinanceViews:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(username="tradeuser", password="pass")

    #
    # ---- trade() ----
    #
    @patch("finance.views.exchange_views.ExchangeServiceFactory")
    def test_trade_success(self, mock_factory: MagicMock):
        mock_service = MagicMock()
        mock_service.send_order.return_value = {"result": "ok"}
        mock_factory.get_service_from_request.return_value = mock_service

        payload = {XtraderRequestKeys.ORDER: json.dumps({"symbol": "AAPL"})}
        request = self.rf.post("/finance/trade", data=payload)
        response = trade(request)

        data = json.loads(response.content.decode())
        assert isinstance(response, JsonResponse)
        assert data["result"] == "ok"

    @patch("finance.views.exchange_views.ExchangeServiceFactory")
    def test_trade_invalid_payload(self, mock_factory: MagicMock):
        # Missing ORDER key
        request = self.rf.post("/finance/trade", data={})
        response = trade(request)
        data = json.loads(response.content.decode())

        assert response.status_code == 400
        assert data[XtraderResponseKeys.MESSAGE] == XtraderResponseMessages.INVALID_ORDER_PAYLOAD

    @patch("finance.views.exchange_views.ExchangeServiceFactory")
    def test_trade_exchange_not_connected(self, mock_factory: MagicMock):
        mock_factory.get_service_from_request.side_effect = ValueError("no exchange")
        payload = {XtraderRequestKeys.ORDER: json.dumps({"symbol": "AAPL"})}
        request = self.rf.post("/finance/trade", data=payload)

        response = trade(request)
        data = json.loads(response.content.decode())
        assert response.status_code == 403
        assert data[XtraderResponseKeys.MESSAGE] == XtraderResponseMessages.CONNECT_YOUR_EXCHANGE_TO_PLACE_ORDER

    #
    # ---- portfolio() ----
    #
    @patch("finance.views.exchange_views.ExchangeServiceFactory")
    def test_portfolio_success(self, mock_factory: MagicMock):
        mock_service = MagicMock()
        mock_service.get_portfolio.return_value = [{"asset": "BTC"}]
        mock_factory.get_service_for_user.return_value = mock_service

        request = self.rf.get("/finance/portfolio")
        request.user = self.user

        response = portfolio(request, exchange_service=mock_service)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.ASSETS] == [{"asset": "BTC"}]

    @patch("finance.views.exchange_views.ExchangeServiceFactory")
    def test_portfolio_no_connected_exchange(self, mock_factory: MagicMock):
        mock_factory.get_service_for_user.side_effect = NoConnectedExchangeException("No exchange")
        request = self.rf.get("/finance/portfolio")
        request.user = self.user

        # manually calling decorator to simulate behavior
        from finance.views import user_exchange_must_be_connected

        @user_exchange_must_be_connected
        def dummy_view(request, exchange_service):
            return JsonResponse({"ok": True})

        response = dummy_view(request)
        data = json.loads(response.content.decode())
        assert response.status_code == 403
        assert XtraderResponseKeys.MESSAGE in data

    #
    # ---- get_orders() ----
    #
    @patch("finance.views.exchange_views.ExchangeServiceFactory")
    def test_get_orders(self, mock_factory: MagicMock):
        mock_service = MagicMock()
        mock_service.get_orders.return_value = [{"id": 1}]
        mock_factory.get_service_for_user.return_value = mock_service

        request = self.rf.get("/finance/orders", data={BinanceRequestKeys.SYMBOL: "BTCUSDT"})
        request.user = self.user

        response = get_orders(request, exchange_service=mock_service)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.ORDERS] == [{"id": 1}]

    #
    # ---- cancel_order() ----
    #
    @patch("finance.views.exchange_views.ExchangeServiceFactory")
    def test_cancel_order_success(self, mock_factory: MagicMock):
        mock_service = MagicMock()
        mock_service.cancel_order.return_value = True
        mock_factory.get_service_for_user.return_value = mock_service

        params = {BinanceRequestKeys.SYMBOL: "BTCUSDT", BinanceRequestKeys.ORDER_ID: 123}
        request = self.rf.get("/finance/cancel", data=params)
        request.user = self.user

        response = cancel_order(request, exchange_service=mock_service)
        assert response.status_code == 200
        assert response.content.decode() == "OK"

    @patch("finance.views.exchange_views.ExchangeServiceFactory")
    def test_cancel_order_failure(self, mock_factory: MagicMock):
        mock_service = MagicMock()
        mock_service.cancel_order.return_value = False
        mock_factory.get_service_for_user.return_value = mock_service

        params = {BinanceRequestKeys.SYMBOL: "BTCUSDT", BinanceRequestKeys.ORDER_ID: 999}
        request = self.rf.get("/finance/cancel", data=params)
        request.user = self.user

        response = cancel_order(request, exchange_service=mock_service)
        assert response.status_code == 400
        assert response.content.decode() == "e"

    #
    # ---- get_exchanges() ----
    #
    @patch("finance.views.exchange_views.Exchange")
    def test_get_exchanges(self, mock_exchange_cls: MagicMock):
        mock_exchange_cls.get_exchanges.return_value = [{"id": 1}]
        request = self.rf.get("/finance/exchanges")
        request.user = self.user

        response = get_exchanges(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.EXCHANGES] == [{"id": 1}]

    #
    # ---- save_exchange() ----
    #
    @patch("finance.views.exchange_views.xtrader_exchange_service")
    def test_save_exchange(self, mock_service: MagicMock):
        mock_service.verify_and_create_exchange.return_value = True
        request = self.rf.post("/finance/save", data={"key": "value"})
        request.user = self.user

        response = save_exchange(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.STATUS] is True

    #
    # ---- remove_exchange() ----
    #
    @patch("finance.views.exchange_views.xtrader_exchange_service")
    def test_remove_exchange(self, mock_service: MagicMock):
        mock_service.remove_exchange.return_value = True
        request = self.rf.post("/finance/remove", data={XtraderRequestKeys.NAME: "binance"})
        request.user = self.user

        response = remove_exchange(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.STATUS] is True
