from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register_user, name="register_user"),
    path("login", views.login_user, name="login_user"),
    path("update-profile", views.update_user_profile, name="update_profile"),
    path("logout", views.logout_user, name = "user_logout")
]