"""Urls for the user app."""
from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("registration/", views.registration, name="registration"),
    path("login/", views.custom_login_view, name="login"),
    path("logout/", views.custom_logout_view, name="logout"),
    path("account/", views.account, name="account"),
]
