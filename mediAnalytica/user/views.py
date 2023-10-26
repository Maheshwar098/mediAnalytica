from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from django.db import connection
from .utils import *
from jwt import encode, decode
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY

cursor = connection.cursor()



def register_user(request):
    if (request.method == "GET"):
        return render(request, "user_register.html")
    request_body = request.body.decode('utf-8')
    userdata = json.loads(request_body)
    first_name = userdata['first_name']
    last_name = userdata['last_name']
    username = userdata['username']
    password = userdata['password']
    email = userdata['email']
    password_hash = generateSHA256Hash(password)
    # cursor.execute("DELETE FROM user_user")

    if(checkUser(username)):
        message = {"message":"User already exists"}
        return JsonResponse(message)

    query = f"INSERT INTO user_user (first_name, last_name, username, password, email) VALUES ('{first_name}', '{last_name}', '{username}', '{password_hash}', '{email}')"
    cursor.execute(query)

    return JsonResponse({"message":"Successfully registered"})

def login_user(request):
    if (request.method == "GET"):
        return render(request, "user_login.html")
    credentials = json.loads(request.body.decode('utf-8'))
    username = credentials['username']
    password = credentials['password']
    password_hash = generateSHA256Hash(password)

    query = f"SELECT * FROM user_user WHERE username='{username}' AND password = '{password_hash}'"

    cursor.execute(query)

    user = cursor.fetchall()

    if(len(user)==0):
        return JsonResponse({"message":"Invalid credentials"})
    
    payload = {'username':str(user[0][3])}
    token = encode(payload, SECRET_KEY)
    response = HttpResponse()
    response['Content-Type']='application/json'
    response.set_cookie("token",token,secure=True,httponly=True)
    response_data = json.dumps({"message":"Logged in successfully"})
    response.content = response_data.encode()
    return response

def update_user_profile(request):
    token = request.COOKIES.get('token')
    if (not token):
        return JsonResponse({"message":"Please login to continue"})

    payload = decode(token,SECRET_KEY,algorithms=["HS256"])
    username = payload['username']
    request_body = request.body.decode('utf-8')
    userdata = json.loads(request_body)
    fields_to_update = list(userdata.keys())

    if("username" in fields_to_update):
        return JsonResponse({"message":"Username cannot be updated"})

    query = f"UPDATE user_user SET "

    field_update = ""
    for (field,value) in userdata.items():
        field_update = field_update + f"{field} = '{value}',"

    update_on_username = f"WHERE username = '{username}'"
    
    query = query + field_update[:-1] + update_on_username

    cursor.execute(query)

    return JsonResponse({"message":"Request executed successfully"})

def logout_user(request):
    token = request.COOKIES.get('token')

    if(not token):
        return JsonResponse({"message":"User not logged in"})
    
    token = request.COOKIES.get('token')

    # Delete the token from the cookies.
    response = HttpResponse()

    response.delete_cookie('token')

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
