from django.urls import path

from users.views import (
    AccountDetailView,
    AccountIsActiveView,
    AccountKwargsView,
    AccountView,
)
from rest_framework.authtoken import views


urlpatterns = [
    path(
        "accounts/",
        AccountView.as_view(),
    ),
    path(
        "accounts/newest/<int:num>/",
        AccountKwargsView.as_view(),
    ),
    path(
        "login/",
        views.obtain_auth_token,
    ),
    path(
        "accounts/<pk>/",
        AccountDetailView.as_view(),
    ),
    path(
        "accounts/<pk>/management/",
        AccountIsActiveView.as_view(),
    ),
]
