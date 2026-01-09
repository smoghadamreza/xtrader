import json
import pytest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from django.contrib.auth.models import User

from finance.views.strategy_views import (
    calculate_indicators,
    save_strategy,
    get_strategy_names,
    load_strategy,
    scan_market,
    strategy_notif,
    indicators_api,
    back_test,
    run_martingale_strategy,
)
from utils.consts import XtraderRequestKeys, XtraderResponseKeys, XtraderResponseMessages, XtraderRequestValues

@pytest.mark.django_db
class TestStrategyViews:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="pass")

    @patch("finance.views.strategy_views.IndicatorService")
    def test_calculate_indicators_success(self, mock_service_cls):
        data = {XtraderRequestKeys.SYMBOL_ID: "BTCUSDT"}
        request = self.rf.get("/calculate-indicators/", {XtraderRequestKeys.PARAM: json.dumps(data)})
        request.user = self.user

        service = MagicMock()
        service.caculate_indicators.return_value = {"indicator": 123}
        mock_service_cls.return_value = service

        response = calculate_indicators(request, interval="1h")
        assert response.status_code == 200
        assert json.loads(response.content.decode()) == {"indicator": 123}

    def test_calculate_indicators_invalid(self):
        request = self.rf.get("/calculate-indicators/", {XtraderRequestKeys.PARAM: "invalid"})
        request.user = self.user
        response = calculate_indicators(request, interval="1h")
        assert response.status_code == 400
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.ERROR] == XtraderResponseMessages.SOMETHING_WENT_WRONG

    @patch("finance.views.strategy_views.StrategyService")
    def test_save_strategy_success(self, mock_service_cls):
        data = {"name": "TestStrategy"}
        request = self.rf.post("/save-strategy/", {XtraderRequestKeys.PARAM: json.dumps(data)})
        request.user = self.user

        service = MagicMock()
        mock_strategy = MagicMock()
        mock_strategy.to_dict.return_value = {"name": "TestStrategy"}
        service.add_or_update_strategy.return_value = mock_strategy
        mock_service_cls.return_value = service

        response = save_strategy(request)
        assert response.status_code == 200
        assert json.loads(response.content.decode()) == {"name": "TestStrategy"}

    def test_save_strategy_invalid(self):
        request = self.rf.post("/save-strategy/", {XtraderRequestKeys.PARAM: "invalid"})
        request.user = self.user
        response = save_strategy(request)
        assert response.status_code == 400
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.ERROR] == XtraderResponseMessages.SOMETHING_WENT_WRONG

    @patch("finance.views.strategy_views.StrategyService")
    def test_get_strategy_names(self, mock_service_cls):
        request = self.rf.get("/get-strategy-names/")
        request.user = self.user

        service = MagicMock()
        mock_strategy1 = MagicMock(name="Strat1")
        mock_strategy1.name = "Strat1"
        mock_strategy2 = MagicMock(name="Strat2")
        mock_strategy2.name = "Strat2"
        service.get_strategies.return_value = [mock_strategy1, mock_strategy2]
        mock_service_cls.return_value = service

        response = get_strategy_names(request)
        assert response.status_code == 200
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.STRATEGIES] == ["Strat1", "Strat2"]

    @patch("finance.views.strategy_views.StrategyService")
    def test_load_strategy_success(self, mock_service_cls):
        request = self.rf.get("/load-strategy/", {XtraderRequestKeys.ID: "1"})
        request.user = self.user

        service = MagicMock()
        strategy = MagicMock()
        strategy.filters = {"filter": 123}
        service.get_strategy.return_value = strategy
        mock_service_cls.return_value = service

        response = load_strategy(request)
        assert response.status_code == 200
        assert json.loads(response.content.decode()) == json.dumps({"filter": 123})

    def test_load_strategy_invalid(self):
        request = self.rf.get("/load-strategy/", {XtraderRequestKeys.ID: "invalid"})
        request.user = self.user
        response = load_strategy(request)
        assert response.status_code == 400
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.ERROR] == XtraderResponseMessages.INVALID_REQUESTED_ACTION

    @patch("finance.views.strategy_views.ScanService")
    def test_scan_market_success(self, mock_scan_cls):
        request = self.rf.get("/scan-market/", {XtraderRequestKeys.STRATEGY_ID: "1"})
        request.user = self.user

        scan_service = MagicMock()
        scan_service._scan_market.return_value = {"result": "ok"}
        mock_scan_cls.return_value = scan_service

        response = scan_market(request)
        assert response.status_code == 200
        assert json.loads(response.content.decode()) == json.dumps({"result": "ok"})

    def test_scan_market_no_strategy_id(self):
        request = self.rf.get("/scan-market/")
        request.user = self.user
        response = scan_market(request)
        assert response.status_code == 400

    @patch("finance.views.strategy_views.ScanService")
    @patch("finance.views.strategy_views.threading.Thread")
    @patch("finance.views.strategy_views.FundService")
    def test_strategy_notif(self, mock_fund, mock_thread, mock_scan_cls):
        request = self.rf.get("/strategy-notif/1h/")
        request.user = self.user
        mock_scan_cls.return_value.run_all_users = MagicMock()
        mock_fund.create_today_snapshots = MagicMock()

        response = strategy_notif(request, interval="1h")
        assert response.status_code == 200
        assert json.loads(response.content.decode())[XtraderResponseKeys.S] == 200

        # Test daily interval triggers fund snapshot
        response = strategy_notif(request, interval=XtraderRequestValues.Interval.ONE_DAY)
        assert response.status_code == 200

    @patch("finance.views.strategy_views.indicator_catalog")
    def test_indicators_api(self, mock_catalog):
        mock_catalog.get_group_api.return_value = {"indicators": [1, 2]}
        request = self.rf.get("/indicators-api/")
        response = indicators_api(request)
        assert response.status_code == 200
        assert json.loads(response.content.decode()) == json.dumps({"indicators": [1, 2]})

    @patch("finance.views.strategy_views.IndicatorService")
    def test_back_test_success(self, mock_service_cls):
        data = {
            XtraderRequestKeys.NAME: "BTCUSDT",
            XtraderRequestKeys.TRADES: json.dumps([]),
            XtraderRequestKeys.CONFIG: {},
        }
        request = self.rf.get("/back-test/", {XtraderRequestKeys.PARAM: json.dumps(data)})
        request.user = self.user

        service = MagicMock()
        service.give_result_backtest.return_value = {"result": "ok"}
        mock_service_cls.return_value = service

        response = back_test(request)
        assert response.status_code == 200
        assert json.loads(response.content.decode()) == {"result": "ok"}

    @patch("finance.views.strategy_views.MartingaleStopLossTakeProfitService")
    @patch("finance.views.strategy_views.MartingaleStrategyConfig")
    @patch("finance.views.strategy_views.binance_market_service")
    def test_run_martingale_strategy(self, mock_binance, mock_config_cls, mock_service_cls):
        data = {"param": 1}
        request = self.rf.get("/martingale-strategy/", {XtraderRequestKeys.PARAM: json.dumps(data)})
        request.user = self.user

        mock_config = MagicMock()
        mock_config_cls.from_dict.return_value = mock_config

        service = MagicMock()
        service.run_strategy.return_value = {"result": "ok"}
        mock_service_cls.return_value = service

        response = run_martingale_strategy(request)
        assert response.status_code == 200
