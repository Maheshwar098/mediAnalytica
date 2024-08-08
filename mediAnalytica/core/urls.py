from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_homepage, name="homepage"),
    path("get-doctor",views.get_doctors, name="get_doctors"),
    path("get-doctor/<id>", views.get_doctor, name="get_doctor"),
    path("get-specialist", views.get_doctors_by_speciality, name="get_specialists"),
    path("get-specialist-from-disease", views.get_doctors_by_disease, name="get_doctors_by_disease"),
    path("get-specialist-from-symptom", views.get_sepcialist_from_symptoms, name="get_doctors"),
    path("add-doctors", views.add_doctors, name = "add_doctors"),
    path("test-query", views.test_query, name = "test_query"),
]
