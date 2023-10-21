from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from django.db import connection
from .utils import *
from jwt import encode, decode
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY

cursor = connection.cursor()

def register_doctor(request):
    request_body = request.body.decode('utf-8')     
    doctor_data = json.loads(request_body)
    doctor_data['password'] = generate_SHA256_hash(doctor_data['password'])
    # cursor.execute("DELETE FROM doctor_doctor")
    if(check_doctor(doctor_data['username'])):
        return JsonResponse({"message" : "Doctor already exists"})
    
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
    return JsonResponse({"message":"Doctor registered successfully"})

def login_doctor(request):
    request_body = request.body.decode('utf-8')
    credentials = json.loads(request_body)
    username = credentials['username']
    password = credentials['password']
    if(not authenticate_doctor(username, password)):
        return JsonResponse({"message":"Invalid credentials"})
    payload = {"username":username}
    token = encode(payload, SECRET_KEY)
    response = HttpResponse()
    response['Content-Type'] = 'application/json'
    response.set_cookie("token", token, httponly=True, secure=True)
    response_data = json.dumps({"message":"Logged in successfully"})
    response.content = response_data.encode()
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
    
    response = HttpResponse()
    # Set a new cookie with the `expires=0` option.
    response.set_cookie('token', 'expired', expires=0)


    # Set the `Content-Type` header of the response to `application/json`.
    response['Content-Type'] = 'application/json'

    # Serialize the response data to a string.
    response_data = json.dumps({'message': 'Logged out successfully.'})

    # Set the `Content` of the response to the serialized response data.
    response.content = response_data.encode()

    # Return the response object.
    return response
