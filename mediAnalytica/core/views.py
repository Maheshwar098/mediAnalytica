from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from .utils import *
from django.http import HttpRequest
from django.core.handlers.wsgi import WSGIRequest
import numpy as np
import pickle
cursor = connection.cursor()
model_path = "core/static/rf_disease.sav"
with open(model_path, 'rb') as file :
    model = pickle.load(file)

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

def get_specialist(request):
    token = request.COOKIES.get('token')
    if (not token):
        return JsonResponse({"message":"Please login to continue"})
    disease = request.GET.get('disease')
    query = f"SELECT speciality FROM core_diseasespeciality WHERE disease = '{disease}'"
    cursor.execute(query)
    speciality = cursor.fetchall()
    if(len(speciality)==0):
        return JsonResponse({"message":"Speciality Not found"})
    speciality = speciality[0][0]
    query = f"SELECT * FROM doctor_doctor WHERE speciality = '{speciality}'"
    cursor.execute(query)
    doctors = serialize_data(cursor.fetchall())
    context = {"doctors":doctors}
    return render(request, "doctors.html",context)

def get_sepcialist_from_symptoms(request):
    token = request.COOKIES.get('token')
    if (not token):
        return JsonResponse({"message":"Please login to continue"})
    if(request.method == "GET"):
        return render(request, "user_diagnosis.html")
    s1 = request.POST.get('s1')
    s2 = request.POST.get('s2')
    s3 = request.POST.get('s3')
    s4 = request.POST.get('s4')
    s5 = request.POST.get('s5')

    print(s1, s2, s3,s4,s5)
   
    symptom_dict = {
        'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremities': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}  

    x = np.zeros((1,132))

    if s1 in symptom_dict:
        x[0][symptom_dict[s1]] = 1
    if s2 in symptom_dict:
        x[0][symptom_dict[s2]] = 1
    if s3 in symptom_dict:
        x[0][symptom_dict[s3]] = 1
    if s4 in symptom_dict:
        x[0][symptom_dict[s4]] = 1
    if s5 in symptom_dict:
        x[0][symptom_dict[s5]] = 1
    # model_path = "core/dbms_rf_1.pkl"

    prediction = model.predict(x)

    print(prediction)

    diseases = [
    "Fungal infection",
    "Hepatitis C",
    "Hepatitis E",
    "Alcoholic hepatitis",
    "Tuberculosis",
    "Common Cold",
    "Pneumonia",
    "Dimorphic hemmorhoids(piles)",
    "Heart attack",
    "Varicose veins",
    "Hypothyroidism",
    "Hyperthyroidism",
    "Hypoglycemia",
    "Osteoarthristis",
    "Arthritis",
    "(vertigo) Paroymsal Positional Vertigo",
    "Acne",
    "Urinary tract infection",
    "Psoriasis",
    "Hepatitis D",
    "Hepatitis B",
    "Allergy",
    "Hepatitis A",
    "GERD",
    "Chronic cholestasis",
    "Drug Reaction",
    "Peptic ulcer diseae",
    "AIDS",
    "Diabetes",
    "Gastroenteritis",
    "Bronchial Asthma",
    "Hypertension",
    "Migraine",
    "Cervical spondylosis",
    "Paralysis (brain hemorrhage)",
    "Jaundice",
    "Malaria",
    "Chicken pox",
    "Dengue",
    "Typhoid",
    "Impetigo"]

    print(prediction[0])
    context = {"alert" : f"diagnosis : {prediction[0]}"}
    context = {"result" : prediction[0]}

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