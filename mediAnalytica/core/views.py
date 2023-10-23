from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from .utils import *


cursor = connection.cursor()

def get_doctors(request):
    token = request.COOKIES.get('token')
    if (not token):
        return JsonResponse({"message":"Please login to continue"})
    query = "SELECT * FROM doctor_doctor"
    cursor.execute(query)
    doctors = cursor.fetchall()
    data = serialize_data(doctors)
    return JsonResponse({"message":data})

def get_doctor(request,id):
    token = request.COOKIES.get('token')
    if (not token):
        return JsonResponse({"message":"Please login to continue"})
    query = f"SELECT * FROM doctor_doctor WHERE id = {id}"
    cursor.execute(query)
    doctor = cursor.fetchall()
    data = serialize_data(doctor)
    return JsonResponse({"message":data})

def get_specialist(request):
    token = request.COOKIES.get('token')
    if (not token):
        return JsonResponse({"message":"Please login to continue"})
    disease = request.GET.get('disease')
    query = f"SELECT speciality FROM core_diseasespeciality WHERE disease = '{disease}'"
    cursor.execute(query)
    speciality = cursor.fetchall()
    if(len(speciality)==0):
        JsonResponse({"message":"Speciality Not found"})
    speciality = speciality[0][0]
    query = f"SELECT * FROM doctor_doctor WHERE speciality = '{speciality}'"
    cursor.execute(query)
    doctors = cursor.fetchall()
    return JsonResponse({"message":doctors})