import json
import pytest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.http import JsonResponse

from finance.views.watchlist_views import add_new_watchlist, get_watchlists, modify_watchlist_symbol
from finance.url_names import FinanceURLS
from utils.consts import (
    XtraderResponseKeys, XtraderRequestKeys, XtraderResponseMessages, XtraderRequestValues
)


@pytest.mark.django_db
class TestWatchlistViews:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="pass")

    @patch("finance.views.watchlist_views.StrategyService")
    @patch("finance.views.watchlist_views.Watchlist.objects")
    def test_add_new_watchlist_success(self, mock_watchlist_objects, mock_service_cls):
        request = self.rf.post("/watchlists/add", {XtraderRequestKeys.NAME: "MyList"})
        request.user = self.user

        # Patch StrategyService
        service = MagicMock()
        service.get_pack_limit.return_value.watchlist = 10
        mock_service_cls.return_value = service

        # Patch filter() to handle both count() and exists()
        mock_filter = MagicMock()
        mock_filter.count.return_value = 0
        mock_filter.exists.return_value = False
        mock_watchlist_objects.filter.return_value = mock_filter

        # create() returns a real object with pk
        from types import SimpleNamespace
        watchlist_mock = SimpleNamespace(pk=1)
        mock_watchlist_objects.create.return_value = watchlist_mock

        response = add_new_watchlist(request)
        data = json.loads(response.content.decode())

        assert response.status_code == 200
        assert data[XtraderResponseKeys.ID] == 1
        assert data[XtraderResponseKeys.S] == 200




    @patch("finance.views.watchlist_views.StrategyService")
    @patch("finance.views.watchlist_views.Watchlist.objects")
    def test_add_new_watchlist_limit_exceeded(self, mock_watchlist_objects, mock_service_cls):
        request = self.rf.post("/watchlists/add", {XtraderRequestKeys.NAME: "MyList"})
        request.user = self.user

        service = MagicMock()
        service.get_pack_limit.return_value.watchlist = 1
        mock_service_cls.return_value = service

        mock_watchlist_objects.filter.return_value.count.return_value = 1

        response = add_new_watchlist(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.S] == 302
        assert data[XtraderResponseKeys.REDIRECT] == FinanceURLS.SETTINGS_PACKAGES

    @patch("finance.views.watchlist_views.StrategyService")
    @patch("finance.views.watchlist_views.Watchlist.objects")
    def test_add_new_watchlist_empty_name(self, mock_watchlist_objects, mock_service_cls):
        request = self.rf.post("/add-new-watchlist/", {XtraderRequestKeys.NAME: ""})
        request.user = self.user

        # ensure count returns int
        mock_watchlist_objects.filter.return_value.count.return_value = 0

        # Fix: patch StrategyService to return a proper int limit
        service = MagicMock()
        service.get_pack_limit.return_value.watchlist = 10
        mock_service_cls.return_value = service

        response = add_new_watchlist(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.S] == 403
        assert data[XtraderResponseKeys.M] == XtraderResponseMessages.EMPTY_WATCHLIST_NAME

    @patch("finance.views.watchlist_views.StrategyService")
    @patch("finance.views.watchlist_views.Watchlist.objects")
    def test_add_new_watchlist_duplicate_name(self, mock_watchlist_objects, mock_service_cls):
        request = self.rf.post("/add-new-watchlist/", {XtraderRequestKeys.NAME: "MyList"})
        request.user = self.user

        # patch StrategyService properly
        service = MagicMock()
        service.get_pack_limit.return_value.watchlist = 10
        mock_service_cls.return_value = service

        # ensure count returns int
        mock_watchlist_objects.filter.return_value.count.return_value = 0
        mock_watchlist_objects.filter.return_value.exists.return_value = True

        response = add_new_watchlist(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.S] == 403
        assert data[XtraderResponseKeys.M] == XtraderResponseMessages.REPEATED_WATCHLIST_NAME

    @patch("finance.views.watchlist_views.Watchlist.objects")
    @patch("finance.views.watchlist_views.WatchlistSymbol")
    def test_get_watchlists_list_and_default(self, mock_symbol_cls, mock_watchlist_objects):
        request = self.rf.get("/get-watchlists/")
        request.user = self.user

        w1 = MagicMock()
        w1.pk = 1
        w1.name = "List1"
        w2 = MagicMock()
        w2.pk = 2
        w2.name = "List2"
        mock_watchlist_objects.filter.return_value.order_by.return_value = [w1, w2]

        response = get_watchlists(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.S] == 200
        # 2 + default
        assert len(data[XtraderResponseKeys.WATCHLISTS]) == 3

    @patch("finance.views.watchlist_views.Watchlist.objects")
    @patch("finance.views.watchlist_views.WatchlistSymbol")
    def test_get_watchlists_remove_default(self, mock_symbol_cls, mock_watchlist_objects):
        request = self.rf.get("/get-watchlists/")
        request.GET = {XtraderRequestKeys.ID: "0", XtraderRequestKeys.ACTION: XtraderRequestValues.REMOVE}
        request.user = self.user

        response = get_watchlists(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.S] == 403
        assert data[XtraderResponseKeys.M] == XtraderResponseMessages.CANT_DELETE_DEFAULT_WATCHLIST

    @patch("finance.views.watchlist_views.Watchlist.objects")
    @patch("finance.views.watchlist_views.WatchlistSymbol")
    def test_modify_watchlist_symbol_add_success(self, mock_symbol_cls, mock_watchlist_objects):
        request = self.rf.post("/modify-watchlist-symbol/")
        request.GET = {XtraderRequestKeys.WATCHLIST_ID: "1", XtraderRequestKeys.ACTION: XtraderRequestValues.ADD}
        request.user = self.user

        watchlist = MagicMock()
        mock_watchlist_objects.filter.return_value.first.return_value = watchlist
        mock_symbol_cls.objects.filter.return_value.exists.return_value = False
        mock_symbol_cls.objects.create.return_value = None

        response = modify_watchlist_symbol(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.S] == 200
        assert data[XtraderResponseKeys.M] == XtraderResponseMessages.SYMBOL_ADDED_TO_WATCHLIST

    @patch("finance.views.watchlist_views.Watchlist.objects")
    @patch("finance.views.watchlist_views.WatchlistSymbol")
    def test_modify_watchlist_symbol_remove_success(self, mock_symbol_cls, mock_watchlist_objects):
        request = self.rf.post("/modify-watchlist-symbol/")
        request.GET = {XtraderRequestKeys.WATCHLIST_ID: "1", XtraderRequestKeys.ACTION: XtraderRequestValues.REMOVE}
        request.user = self.user

        watchlist = MagicMock()
        mock_watchlist_objects.filter.return_value.first.return_value = watchlist

        response = modify_watchlist_symbol(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.S] == 200
        assert data[XtraderResponseKeys.M] == XtraderResponseMessages.SYMBOL_REMOVED_FROM_WATCHLIST

    def test_modify_watchlist_symbol_default_watchlist(self):
        request = self.rf.post("/modify-watchlist-symbol/")
        request.GET = {XtraderRequestKeys.WATCHLIST_ID: XtraderRequestValues.DEFAULT_WATCHLIST_ID}
        request.user = self.user

        response = modify_watchlist_symbol(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.S] == 403
        assert data[XtraderResponseKeys.M] == XtraderResponseMessages.CANNOT_MODIFY_DEFAULT_WATCHLIST

    @patch("finance.views.watchlist_views.Watchlist.objects")
    def test_modify_watchlist_symbol_invalid_watchlist(self, mock_watchlist_objects):
        request = self.rf.post("/modify-watchlist-symbol/")
        request.GET = {XtraderRequestKeys.WATCHLIST_ID: "999"}
        request.user = self.user

        mock_watchlist_objects.filter.return_value.first.return_value = None

        response = modify_watchlist_symbol(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.S] == 403
        assert data[XtraderResponseKeys.M] == XtraderResponseMessages.INVALID_WATCHLIST_ID
