from typing import cast

from django.views.generic.list import ListView
from django.http import Http404

from userena import settings as userena_settings
from userena.models import UserenaBaseProfileManager
from userena.utils import get_profile_model

class ProfileListView(ListView):
    """Lists all profiles."""

    context_object_name = "profile_list"
    page = 1
    template_name = userena_settings.USERENA_PROFILE_LIST_TEMPLATE
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            page = int(self.request.GET.get("page", str(self.page)))
        except (TypeError, ValueError):
            page = self.page

        if (
            userena_settings.USERENA_DISABLE_PROFILE_LIST
            and not self.request.user.is_staff
        ):
            raise Http404

        if not self.extra_context:
            self.extra_context = dict()

        context["page"] = page
        context["paginate_by"] = self.paginate_by
        context["extra_context"] = self.extra_context

        return context

    def get_queryset(self):
        profile_model = get_profile_model()
        userena_profile_manager = cast(
            UserenaBaseProfileManager, profile_model.objects
        )
        queryset = userena_profile_manager.get_visible_profiles(
            self.request.user
        ).select_related()
        return queryset
