from django.db import connection
import hashlib

cursor = connection.cursor()

def checkUser(username):
    query = f"SELECT * FROM user_user WHERE username = '{username}' "
    cursor.execute(query)
    rows = cursor.fetchall()
    if(len(rows)>0):
        return True
    return False

def generateSHA256Hash(data):
    data_hash = hashlib.sha256(data.encode()).hexdigest()
    return data_hash