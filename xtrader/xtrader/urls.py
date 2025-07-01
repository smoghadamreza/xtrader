"""Xtrader URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path

urlpatterns = [
    re_path(
        r"^accounts/",
        include(("accounts.urls", "accounts"), namespace="accounts"),
    ),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^", include(("finance.urls", "finance"), namespace="finance")),
    re_path(r"^data/", include(("data.urls", "data"), namespace="data")),
    re_path(
        r"^social/", include(("social.urls", "social"), namespace="social")
    ),
    re_path(r"^assetManagement/", include(("aum.urls", "aum"))),
    re_path(r"^sales/", include(("sales.urls", "sales"), namespace="sales")),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
