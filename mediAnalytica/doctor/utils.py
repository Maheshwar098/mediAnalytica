from django.db import connection
import hashlib
cursor = connection.cursor()

def check_doctor(username):
    query = f"SELECT * FROM doctor_doctor WHERE username = '{username}'"
    cursor.execute(query)
    doctors = cursor.fetchall()
    if(len(doctors)==0):
        return False
    return True

def generate_SHA256_hash(data):
    hashed_data = hashlib.sha256(data.encode()).hexdigest()
    return hashed_data

def authenticate_doctor(username, password):
    hashed_password = generate_SHA256_hash(password)
    query = f"SELECT * FROM doctor_doctor WHERE username = '{username}' AND password = '{hashed_password}'"
    cursor.execute(query)
    doctors = cursor.fetchall()
    if(len(doctors)==0):
        return False
    return True
