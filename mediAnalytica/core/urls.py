from django.urls import path
from . import views

urlpatterns = [
    path("get-doctor",views.get_doctors, name="get_doctors"),
    path("get-doctor/<id>", views.get_doctor, name="get_doctors"),
    path("get-specialist", views.get_specialist, name="get_doctors"),
]
