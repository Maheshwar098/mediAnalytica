# Generated by Django 5.1 on 2024-08-08 10:41
import os
from django.db import migrations
from django.conf import settings
import json

import logging
logging.basicConfig(level=logging.DEBUG)  # Set the threshold for the logger
logger = logging.getLogger(__name__)


def populate_disease_specialty(apps, schema_editor):
    try:
        DiseaseSpeciality = apps.get_model('core', 'DiseaseSpeciality')
        json_file_path = os.path.join(settings.BASE_DIR, 'data', 'disease-specialist.json')
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        print("fuck")
        for disease, speciality in data.items():    
            DiseaseSpeciality.objects.create(disease=disease, speciality=speciality)

        if settings.DEBUG:
            logger.info("Added preset data to disease-specialist table")

    except Exception as e:
        logger.error('Error adding static data to diseases-specialist table')
        logger.error(e)
        logger.info("You can add this data manually")

class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_disease_specialty),
    ]

