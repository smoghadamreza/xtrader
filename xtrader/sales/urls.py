from django.urls import re_path

from sales import views

urlpatterns = [
    re_path(r"^packages/$", views.get_packages),
    re_path(r"^subscribe/$", views.subscribe),
]
