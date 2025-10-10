import json
import pytest
from unittest.mock import MagicMock, patch
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse

from social import views


@pytest.mark.django_db
class TestSocialViews:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(username="john", password="123")

    #
    # ---- pro_traders() ----
    #
    @patch("social.views.ExchangeServiceFactory")
    @patch("social.views.ProTrader")
    @patch("social.views.Follow")
    @patch("social.views.User")
    def test_pro_traders_post_success(self, mock_user_cls, mock_follow_cls, mock_protrader_cls, mock_exchange_factory):
        mock_trader = MagicMock()
        mock_user_cls.objects.get_by_natural_key.return_value = mock_trader

        mock_exchange_service = MagicMock()
        mock_exchange_factory.get_service_for_user.return_value = mock_exchange_service

        mock_pro = MagicMock()
        mock_pro.pk = 123
        mock_protrader_cls.objects.create.return_value = mock_pro

        body = json.dumps({"username": "trader", "subscription": 50})
        request = self.rf.post("/social/pro-traders", data=body, content_type="application/json")

        response = views.pro_traders(request)
        data = json.loads(response.content.decode())

        assert isinstance(response, JsonResponse)
        assert data["e"] == 123

    @patch("social.views.ProTrader")
    @patch("social.views.Follow")
    def test_pro_traders_get(self, mock_follow_cls, mock_protrader_cls):
        mock_follow = MagicMock()
        mock_follow.pro_trader.pk = 42
        mock_follow_cls.objects.filter.return_value.first.return_value = mock_follow
        mock_protrader_cls.get_all.return_value = [{"id": 42}]

        request = self.rf.get("/social/pro-traders")
        request.user = self.user

        response = views.pro_traders(request)
        data = json.loads(response.content.decode())

        assert isinstance(response, JsonResponse)
        assert data["data"] == [{"id": 42}]
        mock_protrader_cls.get_all.assert_called_once_with(42)

    def test_pro_traders_invalid_method(self):
        request = self.rf.put("/social/pro-traders")
        response = views.pro_traders(request)
        assert response.status_code == 405

    #
    # ---- follow_toggle() ----
    #
    @patch("social.views.Follow")
    def test_follow_toggle_post(self, mock_follow_cls):
        mock_follow_cls.copy_trade.return_value = {"m": "ok"}
        body = json.dumps({"protrader_brand": "X", "action": "follow"})
        request = self.rf.post("/social/follow-toggle", data=body, content_type="application/json")
        request.user = self.user

        response = views.follow_toggle(request)
        data = json.loads(response.content.decode())
        assert data["m"] == "ok"

    def test_follow_toggle_get(self):
        request = self.rf.get("/social/follow-toggle")
        request.user = self.user

        response = views.follow_toggle(request)
        data = json.loads(response.content.decode())
        assert data["m"] == "OK"

    #
    # ---- get_publics() ----
    #
    @patch("social.views.Exchange")
    @patch("social.views.ProTrader")
    def test_get_publics(self, mock_protrader_cls, mock_exchange_cls):
        pro = MagicMock(pk=1)
        trader = MagicMock()
        pro.trader = trader
        mock_protrader_cls.objects.all.return_value = [pro]

        ex = MagicMock(public_key="abc123")
        mock_exchange_cls.objects.filter.return_value.first.return_value = ex

        request = self.rf.get("/social/get-publics")
        response = views.get_publics(request)
        data = json.loads(response.content.decode())

        assert data["publicKeys"] == [{"id": 1, "public": "abc123"}]

    #
    # ---- copy_order() ----
    #
    @patch("social.views.CopyTradeService")
    def test_copy_order_success(self, mock_copy_service_cls):
        mock_service = MagicMock()
        mock_copy_service_cls.return_value = mock_service
        body = json.dumps({"id": 1, "order": {"symbol": "BTC"}})
        request = self.rf.post("/social/copy-order", data=body, content_type="application/json")

        response = views.copy_order(request)
        data = json.loads(response.content.decode())

        assert data["m"] == "ok"
        mock_service.copy_trade.assert_called_once()

    def test_copy_order_failure(self):
        body = "{invalid_json"
        request = self.rf.post("/social/copy-order", data=body, content_type="application/json")
        response = views.copy_order(request)
        data = json.loads(response.content.decode())
        assert data["m"] == "something went wrong"

    #
    # ---- promote() ----
    #
    @patch("social.views.ProTraderService")
    @patch("social.views.ProTrader")
    @patch("social.views.Follow")
    @patch("social.views.Profile")
    @patch("social.views.ExchangeServiceFactory")
    @patch("social.views.TelegramService")
    def test_promote_success(self, mock_telegram_cls, mock_exchange_factory, mock_profile_cls, mock_follow_cls, mock_protrader_cls, mock_service_cls):
        mock_exchange_factory.get_service_for_user.return_value = MagicMock()
        mock_profile = MagicMock(telegram_id="123")
        mock_profile_cls.objects.filter.return_value.first.return_value = mock_profile

        mock_follow_cls.objects.filter.return_value.first.return_value = None
        mock_protrader_cls.objects.filter.return_value.first.return_value = None

        mock_service = MagicMock()
        mock_service.get_recent_nav_snapshots.return_value = list(range(30))
        mock_service_cls.return_value = mock_service

        body = json.dumps({"brand": "BrandX", "subscription": 12.5})
        request = self.rf.post("/social/promote", data=body, content_type="application/json")
        request.user = self.user

        response = views.promote(request)
        data = json.loads(response.content.decode())

        assert data["s"] == 200
        assert "ارتقا پیدا کرد" in data["m"]

    @patch("social.views.ExchangeServiceFactory")
    def test_promote_no_exchange(self, mock_factory):
        mock_factory.get_service_for_user.side_effect = views.NoConnectedExchangeException()
        body = json.dumps({"brand": "B", "subscription": 1})
        request = self.rf.post("/social/promote", data=body, content_type="application/json")
        request.user = self.user

        response = views.promote(request)
        data = json.loads(response.content.decode())
        assert data["href"] == "exchange"

    #
    # ---- trader() ----
    #
    @patch("social.views.get_user_context")
    @patch("social.views.render")
    def test_trader_view(self, mock_render, mock_get_user_context):
        mock_get_user_context.return_value = {"u": "ok"}
        request = self.rf.get("/social/trader")
        request.user = self.user
        views.trader(request)
        mock_render.assert_called_once()

    #
    # ---- get_profile() ----
    #
    @patch("social.views.ProTraderService")
    @patch("social.views.Follow")
    def test_get_profile_following(self, mock_follow_cls, mock_service_cls):
        mock_service = MagicMock()
        mock_service.get_records.return_value = [{"r": 1}]
        mock_service.pro_trader.brand = "BrandY"
        mock_service.pro_trader.subscription = 10
        mock_service_cls.return_value = mock_service

        mock_follow = MagicMock()
        mock_follow.pro_trader = mock_service.pro_trader
        mock_follow_cls.objects.filter.return_value = MagicMock(
            filter=MagicMock(return_value=MagicMock(first=MagicMock(return_value=mock_follow))),
            __bool__=lambda _: True,
        )

        request = self.rf.get("/social/get-profile/1")
        request.user = self.user

        response = views.get_profile(request, 1)
        data = json.loads(response.content.decode())

        assert data["status"] == 1
        assert data["proTraderBrand"] == "BrandY"

    @patch("social.views.ProTraderService", side_effect=views.NoProTraderFound())
    def test_get_profile_no_protrader(self, mock_service_cls):
        request = self.rf.get("/social/get-profile/99")
        response = views.get_profile(request, 99)
        data = json.loads(response.content.decode())
        assert data["href"] == "/social/copy-trading"

    #
    # ---- copy_trading() ----
    #
    @patch("social.views.get_user_context")
    @patch("social.views.render")
    def test_copy_trading(self, mock_render, mock_ctx):
        mock_ctx.return_value = {"ok": True}
        request = self.rf.get("/social/copy-trading")
        request.user = self.user
        views.copy_trading(request)
        mock_render.assert_called_once()

    #
    # ---- league() ----
    #
    @patch("social.views.get_user_context")
    @patch("social.views.render")
    def test_league(self, mock_render, mock_ctx):
        mock_ctx.return_value = {"ok": True}
        request = self.rf.get("/social/league")
        request.user = self.user
        views.league(request)
        mock_render.assert_called_once()

    #
    # ---- exchange() ----
    #
    @patch("social.views.xtrader_exchange_service")
    @patch("social.views.Exchange")
    def test_exchange_get(self, mock_exchange_cls, mock_service):
        mock_exchange_cls.get_exchanges.return_value = [{"id": 1}]
        request = self.rf.get("/social/exchange")
        request.user = self.user

        response = views.exchange(request)
        data = json.loads(response.content.decode())
        assert data["exchanges"] == [{"id": 1}]

    @patch("social.views.xtrader_exchange_service")
    def test_exchange_post(self, mock_service):
        mock_service.verify_and_create_exchange.return_value = True
        request = self.rf.post("/social/exchange", data={"a": "b"})
        request.user = self.user
        response = views.exchange(request)
        data = json.loads(response.content.decode())
        assert data["status"] is True

    def test_exchange_invalid_method(self):
        request = self.rf.put("/social/exchange")
        request.user = self.user
        response = views.exchange(request)
        assert response.status_code == 400
