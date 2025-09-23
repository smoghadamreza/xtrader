import json
import pytest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from django.contrib.auth.models import User

from aum.views import (
    management,
    issue_redeem_unit,
    add_investor,
    investors,
    get_fund,
    transactions_history,
    init_fund_performance,
    get_fund_performance,
)
from aum.exceptions import FundNotFound
from utils.consts import XtraderRequestKeys, XtraderRequestValues, XtraderResponseKeys
from aum.consts import ResponseMessages, ResponseData


@pytest.mark.django_db
class TestAUMViews:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(username="aumuser", password="pass")

    def test_management_renders_template(self):
        request = self.rf.get("/")
        request.user = self.user
        response = management(request)
        assert response.status_code == 200

    @patch("aum.views.FundService")
    def test_issue_redeem_unit_success(self, mock_service_cls: MagicMock):
        request = self.rf.post("/", data=json.dumps({
            XtraderRequestKeys.INVESTOR_ID: 1,
            XtraderRequestKeys.ACTION: "issue",
            XtraderRequestKeys.AMOUNT: 100
        }), content_type="application/json")
        request.user = self.user

        service = MagicMock()
        mock_service_cls.return_value = service

        response = issue_redeem_unit(request)
        data = json.loads(response.content.decode())
        assert response.status_code == 200
        assert data[XtraderResponseKeys.C] == 200
        assert data[XtraderResponseKeys.MESSAGE] == ""

    @patch("aum.views.FundService.issue_redeem_unit", side_effect=FundNotFound)
    def test_issue_redeem_unit_fund_not_found(self, mock_issue: MagicMock):
        request = self.rf.post("/", data=json.dumps({
            XtraderRequestKeys.INVESTOR_ID: 1,
            XtraderRequestKeys.ACTION: "issue",
            XtraderRequestKeys.AMOUNT: 100
        }), content_type="application/json")
        request.user = self.user

        response = issue_redeem_unit(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.MESSAGE] == ResponseMessages.FUND_NOT_FOUND

    @patch("aum.views.Fund.objects.get")
    @patch("aum.views.FundInvestor.create_investor")
    def test_add_investor_success(self, mock_create: MagicMock, mock_get_fund: MagicMock):
        request = self.rf.post("/", data=json.dumps({
            XtraderRequestKeys.FIRST_NAME: "John",
            XtraderRequestKeys.LAST_NAME: "Doe",
            XtraderRequestKeys.NATIONAL_CODE: "123"
        }), content_type="application/json")
        request.user = self.user

        fund_mock = MagicMock()
        mock_get_fund.return_value = fund_mock

        investor_mock = MagicMock()
        investor_mock.pk = 42
        mock_create.return_value = investor_mock

        response = add_investor(request)
        data = json.loads(response.content.decode())
        assert response.status_code == 201
        assert data[XtraderResponseKeys.ID] == 42
        assert data[XtraderResponseKeys.MESSAGE] == ResponseMessages.CREATED

    @patch("aum.views.FundService")
    def test_investors_returns_data(self, mock_service_cls: MagicMock):
        request = self.rf.get("/")
        request.user = self.user

        service = MagicMock()
        service.get_investors_info.return_value = [{"id": 1}]
        mock_service_cls.return_value = service

        response = investors(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.DATA] == [{"id": 1}]

    @patch("aum.views.FundService")
    def test_get_fund_returns_info(self, mock_service_cls: MagicMock):
        request = self.rf.get("/")
        request.user = self.user

        service = MagicMock()
        service.get_fund_info.return_value = {"name": "Fund1"}
        mock_service_cls.return_value = service

        response = get_fund(request)
        data = json.loads(response.content.decode())
        assert data["name"] == "Fund1"

    @patch("aum.views.FundService")
    def test_transactions_history_returns_times(self, mock_service_cls: MagicMock):
        request = self.rf.get("/")
        request.user = self.user

        transaction1 = MagicMock(time="2025-01-01")
        transaction2 = MagicMock(time="2025-01-02")
        service = MagicMock()
        service.sync_and_fetch_transactions.return_value = [transaction1, transaction2]
        mock_service_cls.return_value = service

        response = transactions_history(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.DATA] == ["2025-01-01", "2025-01-02"]

    @patch("aum.views.FundService")
    def test_init_fund_performance_authorized(self, mock_service_cls: MagicMock):
        request = self.rf.get("/", {"pass": XtraderRequestValues.XTREASURY})
        request.user = self.user

        service = MagicMock()
        service.init_fund_performance.return_value = True
        mock_service_cls.return_value = service

        response = init_fund_performance(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.DATA] == ResponseData.CREATED

    def test_init_fund_performance_unauthorized(self):
        request = self.rf.get("/", {"pass": "wrong"})
        request.user = self.user

        response = init_fund_performance(request)
        assert response.status_code == 401
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.MESSAGE] == ResponseMessages.NOT_AUTHORIZED

    @patch("aum.views.FundService")
    def test_get_fund_performance_returns_data(self, mock_service_cls: MagicMock):
        request = self.rf.get("/", {"mode": "all"})
        request.user = self.user

        service = MagicMock()
        service.get_fund_performance.return_value = [{"value": 100}]
        mock_service_cls.return_value = service

        response = get_fund_performance(request)
        data = json.loads(response.content.decode())
        assert data[XtraderResponseKeys.DATA] == [{"value": 100}]
