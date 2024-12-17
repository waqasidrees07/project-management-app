from django.contrib.auth import views as auth_views
from django.urls import path
from .forms import (
    LoginForm
)
from . import views


urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),

    path(
            "accounts/login/",
            auth_views.LoginView.as_view(
                template_name="login.html", authentication_form=LoginForm
            ),
            name="login",
        ),
    path("accounts/logout/", views.custom_logout, name="logout"),

]