from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import json
from django.db import connection
from .utils import *
from jwt import encode, decode
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY

cursor = connection.cursor()

def register_doctor(request):
    context = {}
    if (request.method == "GET"):
        context["login_btn_1"] = "User Login"
        context["login_btn_2"] = "Doctor Login"
        context['logout_btn_visibility'] = 'd-none'
        # token = request.COOKIES.get('token')
        # if(token):
        #     context['login_btn_visibility'] = 'd-none'
        #     context['logout_btn_visibility'] = None
        return render(request,"doctor_register.html", context = context) 
    queryDict = request.POST
    doctor_data = {}
    for key in (queryDict.keys()):
        doctor_data[key] = queryDict[key]

    doctor_data['password'] = generate_SHA256_hash(doctor_data['password'])
    if(check_doctor(doctor_data['username'])):
        context = {}
        context["alert"] = "Doctor already exists"
        return render(request, "doctor_register.html", context)
    
    query = "INSERT INTO doctor_doctor "
    fields = ""
    for key in (list(doctor_data.keys())):
        fields = fields + key + ","
    
    query = query + "(" + fields[:-1] + ") VALUES"  
    field_values = ""
    for val in (list(doctor_data.values())):
        field_values = field_values + "'" + val +"',"
    field_values = "(" + field_values[:-1] + ")"
    query = query + field_values 
    cursor.execute(query)
    return redirect("/doctor/login")

def login_doctor(request):
    context = {}
    if(request.method == "GET"):
        context["login_btn_1"] = "User Login"
        context["login_btn_2"] = "Doctor Login"
        context['logout_btn_visibility'] = 'd-none'
        token = request.COOKIES.get('token')
        if(token):
            context['login_btn_visibility'] = 'd-none'
            context['logout_btn_visibility'] = None
        return render(request, "doctor_login.html", context = context)
    
    body = request.POST
    credentials = {}
    for key in (body.keys()):
        credentials[key] = body[key]
    username = credentials['username']
    password = credentials['password']
    if(not authenticate_doctor(username, password)):
        context={}
        context["alert"] = "Invalid Credentials"
        return render(request, "doctor_login.html", context)
    payload = {"username":username}
    token = encode(payload, SECRET_KEY)
    response = redirect("/")
    response.set_cookie("token",token)
    type = "doctor"
    response.set_cookie("type",type)
    return response

def update_doctor_profile(request):
    token = request.COOKIES.get('token')
    if(not token):
        return JsonResponse({"message":"Please login to continue"})
    payload = decode(token, SECRET_KEY, algorithms=['HS256'])
    username = payload['username']
    if(not check_doctor(username)):
        return JsonResponse({"message":"invalid token"})
    req_body = request.body.decode('utf-8')
    update_data = json.loads(req_body)
    query = "UPDATE doctor_doctor SET "
    for (field, value) in (update_data.items()):
        query = query + f"{field} = '{value}',"
    query = query[:-1] + f" WHERE username = '{username}'"
    cursor.execute(query)
    return JsonResponse({"message":"Profile updated successfully"})

def logout_doctor(request):
    token = request.COOKIES.get('token')
    if(not token):
        JsonResponse({"message":"Doctor not logged in "})
    
    response = redirect("/")
    # Set a new cookie with the `expires=0` option.
    response.set_cookie('token', 'expired', expires=0)
    response.set_cookie('type', 'expired', expires=0)


    # Set the `Content-Type` header of the response to `application/json`.
    response['Content-Type'] = 'application/json'

    # Serialize the response data to a string.
    response_data = json.dumps({'message': 'Logged out successfully.'})

    # Set the `Content` of the response to the serialized response data.
    response.content = response_data.encode()

    # Return the response object.
    return response
