import pytest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import Http404

from accounts.views.profile_list_views import ProfileListView
from accounts.url_names import AccountsURLS


@pytest.mark.django_db
class TestProfileListView:
    def setup_method(self):
        self.rf = RequestFactory()
        # Make user staff to bypass the profile list disable check
        self.user = User.objects.create_user(username="plist", password="pass", is_staff=True)

    @patch.object(ProfileListView, "get_queryset")
    def test_list_view_renders_with_profiles(self, mock_get_queryset: MagicMock):
        request = self.rf.get(reverse(AccountsURLS.PROFILE_LIST))
        request.user = self.user

        mock_queryset = MagicMock()
        mock_get_queryset.return_value = mock_queryset

        view = ProfileListView.as_view()
        response = view(request)
        assert response.status_code == 200
        assert "profile_list" in response.context_data
        assert response.context_data["profile_list"] == mock_queryset
        assert response.context_data["page"] == 1
        assert "paginate_by" in response.context_data
        assert "extra_context" in response.context_data

    def test_disabled_profile_list_for_non_staff_raises_404(self):
        # Non-staff user should raise 404 if profile list is disabled
        non_staff = User.objects.create_user(username="nonstaff", password="pass", is_staff=False)
        request = self.rf.get(reverse(AccountsURLS.PROFILE_LIST))
        request.user = non_staff

        view = ProfileListView.as_view()

        # Patch the setting via monkeypatch
        with patch("accounts.views.profile_list_views.userena_settings") as mock_settings:
            mock_settings.USERENA_DISABLE_PROFILE_LIST = True
            with pytest.raises(Http404):
                view(request)

    @patch.object(ProfileListView, "get_queryset")
    def test_page_query_parameter_is_used(self, mock_get_queryset: MagicMock):
        request = self.rf.get(reverse(AccountsURLS.PROFILE_LIST), {"page": "5"})
        request.user = self.user  # staff user

        mock_queryset = MagicMock()
        mock_get_queryset.return_value = mock_queryset

        view = ProfileListView.as_view()
        response = view(request)
        assert response.status_code == 200
        assert response.context_data["page"] == 5

    @patch.object(ProfileListView, "get_queryset")
    def test_invalid_page_query_defaults_to_one(self, mock_get_queryset: MagicMock):
        request = self.rf.get(reverse(AccountsURLS.PROFILE_LIST), {"page": "invalid"})
        request.user = self.user  # staff user

        mock_queryset = MagicMock()
        mock_get_queryset.return_value = mock_queryset

        view = ProfileListView.as_view()
        response = view(request)
        assert response.status_code == 200
        assert response.context_data["page"] == 1
