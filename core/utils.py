from django.db import connection 
import numpy as np
from PIL import Image

cursor = connection.cursor()

def checkUser(username):
    query = f"SELECT * FROM user_user WHERE username = '{username}' "
    cursor.execute(query)
    rows = cursor.fetchall()
    if(len(rows)>0):
        return True
    return False

def serialize_data(data):
   
    lst = []
    for row in data:
        dict = {}
        print(row)
        dict["id"] = row[0]
        dict["first_name"]=row[1]
        dict["last_name"] = row[2]
        dict["username"] = row[3]
        dict["password"] = row[4]
        dict["email"] = row[5]
        dict["phone"] = row[6]
        dict["speciality"] = row[7]
        dict["location"] = row[8]
        lst.append(dict)
    # print(lst)
    return lst

def reshape_image(image, target_height, target_width):
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    resized_image = image.resize((target_width, target_height), Image.BILINEAR)
    return np.array(resized_image)