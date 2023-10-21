

def serialize_data(data):
    dict = {}
    lst = []
    for row in data:
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
    return lst
