import json
import pytest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from utils.consts import XtraderResponseKeys

from data.views import (
    get_all_symbol_candles_history,
    stock_watch_info,
    symbol_search,
    get_symbol_candles_history,
    get_symbols,
    get_all_symbols,
    get_intervals,
)
from data.url_names import DataURLs


@pytest.mark.django_db
class TestDataViews:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(username="datauser", password="pass")

    @patch("data.views.StockWatchService")
    def test_get_symbols(self, mock_service_cls: MagicMock):
        request = self.rf.get(reverse(DataURLs.GET_SYMBOLS))
        service = MagicMock()
        service.get_stock_watch_symbols.return_value = ["AAPL", "MSFT"]
        mock_service_cls.return_value = service

        response = get_symbols(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.SYMBOLS] == ["AAPL", "MSFT"]

    @patch("data.views.StockWatchService")
    def test_get_all_symbols(self, mock_service_cls: MagicMock):
        request = self.rf.get(reverse(DataURLs.ALL_SYMBOLS))
        service = MagicMock()
        service.get_all_exchange_symbols.return_value = ["AAPL", "MSFT"]
        mock_service_cls.return_value = service

        response = get_all_symbols(request)
        data = json.loads(response.content.decode())
        expected = [{XtraderResponseKeys.TITLE: "AAPL"}, {XtraderResponseKeys.TITLE: "MSFT"}]
        assert data[XtraderResponseKeys.SYMBOLS] == expected

    @patch("data.views.StockWatchService")
    def test_get_intervals_with_user_time_frame(self, mock_service_cls: MagicMock):
        request = self.rf.get(reverse(DataURLs.GET_INTERVALS))
        request.user = self.user

        service = MagicMock()
        service.get_intervals.return_value = [1, 5, 15]
        service.get_user_time_frame.return_value = 5
        mock_service_cls.return_value = service

        response = get_intervals(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.INTERVALS] == [1, 5, 15]
        assert data[XtraderResponseKeys.USER_TIME_FRAME] == 5

    @patch("data.views.StockWatchService")
    def test_get_intervals_without_user_time_frame(self, mock_service_cls: MagicMock):
        request = self.rf.get(reverse(DataURLs.GET_INTERVALS))
        request.user = self.user

        service = MagicMock()
        service.get_intervals.return_value = [1, 5, 15]
        service.get_user_time_frame.return_value = None
        mock_service_cls.return_value = service

        response = get_intervals(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.INTERVALS] == [1, 5, 15]
        assert XtraderResponseKeys.USER_TIME_FRAME not in data

    @patch("data.views.StockWatchService")
    def test_get_all_symbol_candles_history(self, mock_service_cls: MagicMock):
        request = self.rf.get(reverse(DataURLs.ALL_SYMBOLS_HISTORY))
        service = MagicMock()
        service.get_all_symbol_candles_history.return_value = [{"symbol": "AAPL"}]
        mock_service_cls.return_value = service

        response = get_all_symbol_candles_history(request)
        assert isinstance(response, HttpResponse)
        data = json.loads(response.content.decode())
        assert data == [{"symbol": "AAPL"}]

    @patch("data.views.StockWatchService")
    def test_stock_watch_info(self, mock_service_cls: MagicMock):
        request = self.rf.get(reverse(DataURLs.STOCK_WATCH_INFO, kwargs={"symbol_id": "AAPL"}))
        service = MagicMock()
        service.get_stock_watch_info.return_value = {"symbol": "AAPL"}
        mock_service_cls.return_value = service

        response = stock_watch_info(request, symbol_id="AAPL")
        assert isinstance(response, HttpResponse)
        data = json.loads(response.content.decode())
        assert data["symbol"] == "AAPL"

    @patch("data.views.StockWatchService")
    def test_symbol_search(self, mock_service_cls: MagicMock):
        request = self.rf.get(reverse(DataURLs.SYMBOL_SEARCH, kwargs={"query": "AA"}))
        service = MagicMock()
        service.search_symbols.return_value = ["AAPL", "MSFT"]
        mock_service_cls.return_value = service

        response = symbol_search(request, query="AA")
        assert isinstance(response, HttpResponse)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.ITEMS] == ["AAPL", "MSFT"]

    @patch("data.views.StockWatchService")
    def test_get_symbol_candles_history(self, mock_service_cls: MagicMock):
        request = self.rf.get(reverse(DataURLs.CANDLES_HISTORY, kwargs={"symbol_id": "AAPL", "interval": 60}))
        service = MagicMock()
        service.get_symbol_candles_history.return_value = [{"time": "2025-01-01", "value": 100}]
        mock_service_cls.return_value = service

        response = get_symbol_candles_history(request, symbol_id="AAPL", interval=60)
        assert isinstance(response, JsonResponse)
        data = json.loads(response.content.decode())
        assert data == json.dumps([{"time": "2025-01-01", "value": 100}])
