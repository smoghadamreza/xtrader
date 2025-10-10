import json
import pytest
from unittest.mock import MagicMock, patch
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.http import JsonResponse

from sales.views import get_packages, subscribe


@pytest.mark.django_db
class TestSalesViews:
    def setup_method(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(username="salesuser", password="pass")

    #
    # ---- get_packages() ----
    #
    @patch("sales.views.Package")
    @patch("sales.views.Subscription")
    def test_get_packages_with_active_subscription(self, mock_subscription_cls: MagicMock, mock_package_cls: MagicMock):
        # Arrange: mock active packages
        mock_package1 = MagicMock()
        mock_package1.info.return_value = {"id": 1, "name": "Basic"}
        mock_package2 = MagicMock()
        mock_package2.info.return_value = {"id": 2, "name": "Pro"}
        mock_package_cls.objects.filter.return_value.order_by.return_value = [mock_package1, mock_package2]

        # Arrange: mock active subscription
        mock_subscription = MagicMock()
        mock_subscription.package.info.return_value = {"id": 2, "name": "Pro"}
        mock_subscription.expiry = "2025-12-31T00:00:00"
        mock_subscription_cls.objects.filter.return_value.order_by.return_value.first.return_value = mock_subscription

        request = self.rf.get("/sales/packages")
        request.user = self.user

        # Act
        response = get_packages(request)
        data = json.loads(response.content.decode())

        # Assert
        assert isinstance(response, JsonResponse)
        assert response.status_code == 200
        assert "packages" in data
        assert "currentPack" in data
        assert data["currentPack"]["id"] == 2
        assert "expiry" in data["currentPack"]

    @patch("sales.views.Package")
    @patch("sales.views.Subscription")
    def test_get_packages_without_subscription(self, mock_subscription_cls: MagicMock, mock_package_cls: MagicMock):
        # Arrange: mock active packages queryset
        mock_qs = MagicMock()
        mock_package = MagicMock()
        mock_package.info.return_value = {"id": 1, "name": "Basic"}

        mock_qs.order_by.return_value = mock_qs
        mock_qs.__iter__.return_value = iter([mock_package])
        mock_qs.first.return_value = mock_package
        mock_package_cls.objects.filter.return_value = mock_qs

        # No active subscription
        mock_subscription_cls.objects.filter.return_value.order_by.return_value.first.return_value = None

        request = self.rf.get("/sales/packages")
        request.user = self.user

        # Act
        response = get_packages(request)
        data = json.loads(response.content.decode())

        # Assert
        assert isinstance(response, JsonResponse)
        assert response.status_code == 200
        assert data["currentPack"]["id"] == 1
        assert data["currentPack"]["expiry"] == "همیشه"

    @patch("sales.views.Package")
    @patch("sales.views.Subscription")
    def test_get_packages_no_active_packages_raises(self, mock_subscription_cls: MagicMock, mock_package_cls: MagicMock):
        # Mock empty queryset
        mock_qs = MagicMock()
        mock_qs.order_by.return_value = mock_qs
        mock_qs.__iter__.return_value = iter([])
        mock_qs.first.return_value = None
        mock_package_cls.objects.filter.return_value = mock_qs

        # No active subscription either
        mock_subscription_cls.objects.filter.return_value.order_by.return_value.first.return_value = None

        request = self.rf.get("/sales/packages")
        request.user = self.user

        # Act / Assert
        with pytest.raises(ValueError, match="there are not active packages"):
            get_packages(request)

    #
    # ---- subscribe() ----
    #
    @patch("sales.views.Subscription")
    @patch("sales.views.Package")
    def test_subscribe_success(self, mock_package_cls: MagicMock, mock_subscription_cls: MagicMock):
        # Arrange
        mock_package = MagicMock()
        mock_package_cls.objects.filter.return_value.first.return_value = mock_package
        mock_subscription_cls.subscribe.return_value = {"s": 200, "m": "ok"}

        body = json.dumps({"subscribe": 1})
        request = self.rf.post("/sales/subscribe", data=body, content_type="application/json")
        request.user = self.user

        # Act
        response = subscribe(request)
        data = json.loads(response.content.decode())

        # Assert
        assert isinstance(response, JsonResponse)
        assert response.status_code == 200
        assert data["s"] == 200
        assert data["m"] == "ok"
        mock_subscription_cls.subscribe.assert_called_once_with(self.user, mock_package)

    @patch("sales.views.Package")
    def test_subscribe_invalid_package(self, mock_package_cls: MagicMock):
        # Arrange: No matching package
        mock_package_cls.objects.filter.return_value.first.return_value = None

        body = json.dumps({"subscribe": 999})
        request = self.rf.post("/sales/subscribe", data=body, content_type="application/json")
        request.user = self.user

        # Act
        response = subscribe(request)
        data = json.loads(response.content.decode())

        # Assert
        assert isinstance(response, JsonResponse)
        assert response.status_code == 200  # still 200 but includes error code in JSON
        assert data["s"] == 403
        assert data["m"] == "پکیج موجود نیست"
