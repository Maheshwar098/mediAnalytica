from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from .utils import *
from django.http import HttpRequest
from django.core.handlers.wsgi import WSGIRequest
import numpy as np
import pickle
import os
import json 
from django.conf import settings

cursor = connection.cursor()
rf_model_path = "core/static/symptom_rf.sav"
with open(rf_model_path, 'rb') as file :
    rf_model = pickle.load(file)

json_file_path = os.path.join(settings.BASE_DIR, 'data', 'symptoms.json')
with open(json_file_path, 'r') as file:
    SYMPTOMS_DICT = json.load(file)

def show_homepage(request):
    context = {}
    context["login_btn_1"] = "User Login"
    context["login_btn_2"] = "Doctor Login"
    context['logout_btn_visibility'] = 'd-none'
    token = request.COOKIES.get('token')
    if(token):
        context['login_btn_visibility'] = 'd-none'
        context['logout_btn_visibility'] = None
    return render(request, "home.html", context)

def get_doctors(request):
    token = request.COOKIES.get('token')
    if(not token):
        context = {}
        context["alert"]="Please login to continue"
        
    query = "SELECT * FROM doctor_doctor"
    
    cursor.execute(query)
    
    doctors = cursor.fetchall()
    data = serialize_data(doctors)
    context = {"doctors":data}
    return render(request, "doctors.html",context)

def get_doctor(request,id):
    token = request.COOKIES.get('token')
    if (not token):
        return JsonResponse({"message":"Please login to continue"})
    
    query = f"SELECT * FROM doctor_doctor WHERE id = {id}"
    
    cursor.execute(query)
    
    doctor = cursor.fetchall()
    data = serialize_data(doctor)
    context = {"doctor":data[0]}
    return render(request, "doctor.html",context)

def get_doctors_by_disease(request):
    token = request.COOKIES.get('token')
    if (not token):
        return JsonResponse({"message":"Please login to continue"})
    disease = request.GET.get('disease')
    print(f"Searching doctors for disease {disease}")
    query = f"SELECT speciality FROM core_diseasespeciality WHERE disease = '{disease}'"
    cursor.execute(query)
    speciality = cursor.fetchall()
    if(len(speciality)==0):
        return JsonResponse({"message":"Speciality Not found"})
    speciality = speciality[0][0]
    print(f"Searching doctors for speciality {speciality}")
    query = f"SELECT * FROM doctor_doctor WHERE speciality = '{speciality}'"
    cursor.execute(query)
    doctors = serialize_data(cursor.fetchall())
    print(doctors)
    context = {"doctors":doctors}
    return render(request, "doctors.html", context)

def get_doctors_by_speciality(request):
    token = request.COOKIES.get('token')
    if (not token):
        return JsonResponse({"message":"Please login to continue"})
    speciality = request.GET.get('speciality')
    query = f"SELECT * FROM doctor_doctor WHERE speciality = '{speciality}'"
    cursor.execute(query)
    doctors = serialize_data(cursor.fetchall())
    context = {"doctors":doctors}
    return render(request, "doctors.html", context)

def get_sepcialist_from_symptoms(request):
    token = request.COOKIES.get('token')
    if (not token):
        return JsonResponse({"message":"Please login to continue"})
    if(request.method == "GET"):
        return render(request, "user_diagnosis.html")
    
    symptoms = [request.POST.get(f's{i}') for i in range(1, 6)]
    x = np.zeros((1,132))
    for symptom in symptoms:
        if symptom in SYMPTOMS_DICT:
            x[0][SYMPTOMS_DICT[symptom]] = 1

    prediction = rf_model.predict(x)[0]
    context = {"result" : prediction}
    return render(request, "result.html", context=context)
    
def add_doctors(request):
    file_path = "core/static/Doctor_Versus_Disease.csv"
    f = open(file_path)
    content = list(f.read().split("\n"))
    data = [("'"+e.split(",")[0]+"'", "'"+e.split(",")[1]+"'") for e in content]
    query = "INSERT INTO core_diseasespeciality VALUES "
    for i in range (len(data)):
        query = query + "(" + str(i) + "," + data[i][0] + "," + data[i][1] + "),"
    query = query[:-1]
    # cursor.execute(query)
    return JsonResponse({"msg":"hello world"})

def test_query(request):
    query = "DELETE FROM user_user WHERE username = 'test_user_4'"
    # cursor.execute(query)
    return JsonResponse({"resposne" : "Request executed successfully"})