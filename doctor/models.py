from django.db import models

class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=150)
    email = models.CharField(max_length=50)
    phone = models.BigIntegerField()
    speciality = models.CharField(max_length=30)
    location = models.CharField(max_length=30)

