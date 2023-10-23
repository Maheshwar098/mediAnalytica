from django.db import models

# Create your models here.
class DiseaseSpeciality(models.Model):
    disease = models.CharField(max_length=50)
    speciality = models.CharField(max_length=50)