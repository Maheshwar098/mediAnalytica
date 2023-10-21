from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register_doctor, name = "register_doctor"),
    path("login", views.login_doctor, name="login_doctor"),
    path("update-profile", views.update_doctor_profile, name="update_doctor_profile"),
    path("logout", views.logout_doctor, name="doctor_logout")
]
