from django.shortcuts import render, redirect
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
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    password_hash = generateSHA256Hash(password)
    # cursor.execute("DELETE FROM user_user")
    context = {}
    if(checkUser(username)):
        context["alert"] = "User already exists"
        return render(request,"user_register.html", context)

    query = f"INSERT INTO user_user (first_name, last_name, username, password, email) VALUES ('{first_name}', '{last_name}', '{username}', '{password_hash}', '{email}')"
    cursor.execute(query)

    return redirect("/user/login")

def login_user(request):
    if (request.method == "GET"):
        return render(request, "user_login.html")
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    password_hash = generateSHA256Hash(password)

    query = f"SELECT * FROM user_user WHERE username='{username}' AND password = '{password_hash}'"

    cursor.execute(query)

    user = cursor.fetchall()
    context = {}
    if(len(user)==0):
        context["alert"] = "Invalid Credentials"
        return render(request, "user_login.html",context)
    
    payload = {'username':str(user[0][3])}
    token = encode(payload, SECRET_KEY)

    response = redirect("/")
    print(response)
    response.set_cookie('token',token)
    type = 'user'
    response.set_cookie('type', type)
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
    response = redirect('/')

    response.delete_cookie('token')
    response.delete_cookie('type')

    # Set a new cookie with the `expires=0` option.
    response.set_cookie('token', 'expired', expires=0)
    response.set_cookie('type', 'expired', expires=0)

    return response