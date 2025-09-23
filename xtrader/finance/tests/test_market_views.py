import json
from datetime import date
from unittest.mock import patch, MagicMock

import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.http import HttpResponse

from finance.views.market_views import (
    market_watch,
    get_filters,
    display,
    filter_market,
    spot,
    stock_watch,
)
from finance.url_names import FinanceURLS
from utils.consts import XtraderRequestKeys, XtraderResponseKeys, XtraderResponseMessages

@pytest.mark.django_db
class TestFinanceViews:

    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.client.force_login(self.user)

    @patch("finance.views.market_views.get_user_context")
    @patch("finance.views.market_views.Profile.objects.get")
    @patch("finance.views.market_views.render")
    def test_market_watch_subscription_inactive(self, mock_render, mock_profile_get, mock_get_user_context):
        mock_profile = MagicMock()
        mock_profile.expire = None
        mock_profile_get.return_value = mock_profile

        # Return a dict, ensure SUBSCRIBES is iterable if template iterates
        mock_get_user_context.return_value = {"user": self.user, XtraderResponseKeys.SUBSCRIBES: []}

        # render should return HttpResponse
        mock_render.return_value = HttpResponse("ok", status=200)

        response = self.client.get("/market-watch/")
        mock_render.assert_called_once()
        assert response.status_code == 200

    @patch("finance.views.market_views.get_user_context")
    @patch("finance.views.market_views.Profile.objects.get")
    @patch("finance.views.market_views.render")
    def test_market_watch_subscription_active(self, mock_render, mock_profile_get, mock_get_user_context):
        mock_profile = MagicMock()
        mock_profile.expire = date(2100, 1, 1)
        mock_profile_get.return_value = mock_profile
        mock_get_user_context.return_value = {"user": self.user}

        mock_render.return_value = HttpResponse("ok", status=200)

        response = self.client.get("/market-watch/")
        mock_render.assert_called_once()
        assert response.status_code == 200

    def test_get_filters(self):
        response = self.client.get("/get-filters/")
        data = json.loads(response.content.decode())
        assert isinstance(data, list)

    @patch("finance.views.market_views.get_user_context")
    @patch("finance.views.market_views.render")
    def test_display(self, mock_render, mock_get_user_context):
        mock_get_user_context.return_value = {"user": self.user}
        mock_render.return_value = HttpResponse("ok", status=200)

        response = self.client.get("/robots")
        mock_render.assert_called_once()
        args, kwargs = mock_render.call_args
        context = args[2]
        assert context[XtraderResponseKeys.SYMBOL_ID] == "BTCUSDT"

    @patch("finance.views.market_views.dates.Check")
    @patch("finance.views.market_views.MarketWatch.objects.filter")
    @patch("finance.views.market_views.render")
    def test_filter_market(self, mock_render, mock_mw_filter, mock_dates_check):
        mock_dates_check.return_value.last_market.return_value = "2025-01-01"

        # Provide a real list for Paginator
        stocks_list = [MagicMock() for _ in range(5)]
        mock_mw_filter.return_value.order_by.return_value = stocks_list

        mock_render.return_value = HttpResponse("ok", status=200)

        response = self.client.get("/filter-market/", {XtraderRequestKeys.FILTERS: "[]"})
        mock_render.assert_called_once()
        args, kwargs = mock_render.call_args
        context = args[2]
        assert XtraderResponseKeys.STOCKS in context

    @patch("finance.views.market_views.binance_market_service")
    @patch("finance.views.market_views.get_user_context")
    @patch("finance.views.market_views.render")
    def test_spot_with_valid_symbol(self, mock_render, mock_get_user_context, mock_binance_service):
        mock_get_user_context.return_value = {"user": self.user}
        symbol_info_mock = MagicMock()
        symbol_info_mock.base_asset = "BTC"
        mock_binance_service.get_symbol_info.return_value = symbol_info_mock
        mock_render.return_value = HttpResponse("ok", status=200)

        response = self.client.get("/spot/BTCUSDT/")
        mock_render.assert_called_once()
        args, kwargs = mock_render.call_args
        context = args[2]
        assert context[XtraderResponseKeys.TITLE] == "BTC"

    @patch("finance.views.market_views.binance_market_service")
    @patch("finance.views.market_views.render")
    def test_spot_with_exception(self, mock_render, mock_binance_service):
        mock_binance_service.get_symbol_info.side_effect = Exception("Fail")
        mock_render.return_value = HttpResponse("ok", status=200)

        response = self.client.get("/spot/INVALID/")
        mock_render.assert_called_once()
        args, kwargs = mock_render.call_args
        context = args[2]
        assert context[XtraderResponseKeys.MESSAGE] == XtraderResponseMessages.FAILD_TO_GET_SYMBOL

    def test_spot_redirect_no_symbol(self):
        response = self.client.get("/spot/")
        assert response.status_code == 302
        assert response.url == "/spot/BTCUSDT"

    def test_stock_watch_redirect_default(self):
        response = self.client.get("/stock-watch/")
        assert response.status_code == 302
        assert response.url == "/spot/BTCUSDT"

    def test_stock_watch_redirect_symbol(self):
        response = self.client.get("/stock-watch/ETHUSDT/")
        assert response.status_code == 302
        assert response.url == "/spot/ETHUSDT"
