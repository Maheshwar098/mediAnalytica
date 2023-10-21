from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from .utils import *


cursor = connection.cursor()

def get_doctors(request):
    query = "SELECT * FROM doctor_doctor"
    cursor.execute(query)
    doctors = cursor.fetchall()
    data = serialize_data(doctors)
    return JsonResponse({"message":data})

def get_doctor(request,id):
    query = f"SELECT * FROM doctor_doctor WHERE id = {id}"
    cursor.execute(query)
    doctor = cursor.fetchall()
    data = serialize_data(doctor)
    return JsonResponse({"message":data})