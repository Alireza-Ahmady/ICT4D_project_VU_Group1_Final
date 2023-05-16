from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import Malaria_case
from .serializers import Malaria_caseSerializer
from datetime import datetime, timezone
import time
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.db.models import Count
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
import urllib.parse
from django.utils import timezone
from django.http import HttpResponseServerError
from django.shortcuts import redirect 


class Malaria_caseViewSet(viewsets.ModelViewSet):
    queryset = Malaria_case.objects.all().order_by('id')
    serializer_class = Malaria_caseSerializer


@csrf_exempt
def register_case(request):
    try:
        if request.method == 'POST':
            gender_mapping = {'1': 'Male', '2': 'Female'}
            location_mapping = {'1': 'Diabaly', '2': 'Dogofry', '3': 'Kala Siguida', '4': 'Mariko', '5': 'Nampalari', '6': 'Niono', '7': 'Pogo', '8': 'Siribala', '9': 'Sirifila-Boundy', '10': 'Sokolo', '11': 'Toridaga-Ko', '12': 'Yeredon Saniona'}
            language_mapping = {'1': 'english', '2': 'french'}
            
            gender = gender_mapping.get(request.POST.get('gender'))
            age = request.POST.get('age')
            location = location_mapping.get(request.POST.get('location'))
            date_of_diagnosis = datetime.now(timezone.utc)
            language = language_mapping.get(request.POST.get('lang_'))
            
            malaria_case = Malaria_case(gender=gender, age=age, location=location, date_of_diagnosis=date_of_diagnosis)
            malaria_case.save()

            # create XML response
            root = ET.Element("vxml", version="2.1")
            form = ET.SubElement(root, "form")
            block = ET.SubElement(form, "block")
            prompt = ET.SubElement(block, "prompt")
            
            if language == 'french':
                prompt.text = u"Cas enregistré avec succès !"
            else:
                prompt.text = "Case registered successfully!"

            xml_response = ET.tostring(root)

            return HttpResponse(xml_response, content_type="application/xml", status=200)
        else:
            return HttpResponse('Invalid request method')
    except Exception as e:
        return HttpResponseServerError(f'Server Error: {str(e)}')

      


@csrf_exempt
def calculate_risk(request):
    try:
        if request.method == 'POST':
            difficulty_breathing_mapping = {'1': True, '2': False}
            fever_mapping = {'1': True, '2': False}
            chills_mapping = {'1': True, '2': False}
            muscle_pain_mapping = {'1': True, '2': False}
            nausea_mapping = {'1': True, '2': False}
            language_mapping = {'1': 'english', '2': 'french'}

            difficulty_breathing = difficulty_breathing_mapping.get(request.POST.get('difficulty_breathing'))
            fever = fever_mapping.get(request.POST.get('fever'))
            chills = chills_mapping.get(request.POST.get('chills'))
            muscle_pain = muscle_pain_mapping.get(request.POST.get('muscle_pain'))
            nausea = nausea_mapping.get(request.POST.get('nausea'))
            language = language_mapping.get(request.POST.get('lang_'))
            symptoms = [difficulty_breathing, fever, chills, muscle_pain, nausea]
            risk_percentage = sum(symptoms) * 20

            if language == 'french':
                if risk_percentage > 50:
                    message = "Vous avez la malaria, veuillez demander de l'aide."
                    next_url = "http://51.104.163.1:8000/register_french.vxml"
                else:
                    message = "Bonne nouvelle, vous n'avez pas la malaria."
            else:
                if risk_percentage > 50:
                    message = "Based on your symptoms, there is a possibility that you may have contracted malaria."
                    next_url = "http://51.104.163.1:8000/register.vxml"
                else:
                    message = "Good news, you don't have malaria."

            # create XML response
            root = ET.Element("vxml", version="2.1")
            form = ET.SubElement(root, "form")
            block = ET.SubElement(form, "block")
            prompt = ET.SubElement(block, "prompt")
            prompt.text = message
            if risk_percentage > 50:
                goto = ET.SubElement(block, "goto")
                goto.set("next", next_url)
            xml_response = ET.tostring(root)

            return HttpResponse(xml_response, content_type="application/xml", status=200)
        else:
            return HttpResponse('Invalid request method')
    except Exception as e:
        return HttpResponseServerError(f'Server Error: {str(e)}')





@csrf_exempt
def check_malaria_cases(request):
    try:
        if request.method == 'POST':
            location_mapping = {'1': 'Diabaly', '2': 'Dogofry', '3': 'Kala Siguida', '4': 'Mariko', '5': 'Nampalari', '6': 'Niono', '7': 'Pogo', '8': 'Siribala', '9': 'Sirifila-Boundy', '10': 'Sokolo', '11': 'Toridaga-Ko', '12': 'Yeredon Saniona'}
            language_mapping = {'1': 'english', '2': 'french'}
            location = location_mapping.get(request.POST.get('location'))
            language = language_mapping.get(request.POST.get('lang_'))

            # Get the current month and year
            current_month = timezone.now().month
            current_year = timezone.now().year

            # Query the database for malaria cases in the given location for the current month
            cases_count = Malaria_case.objects.filter(location=location, date_of_diagnosis__month=current_month, date_of_diagnosis__year=current_year).count()

            # Create XML response
            root = ET.Element("vxml", version="2.1")
            form = ET.SubElement(root, "form")
            block = ET.SubElement(form, "block")
            prompt = ET.SubElement(block, "prompt")

            if language == 'french':
                prompt.text = f"Il y a {cases_count} cas de paludisme à {location} ce mois-ci."
            else:
                prompt.text = f"There are {cases_count} malaria cases in {location} this month."

            xml_response = ET.tostring(root)

            return HttpResponse(xml_response, content_type="application/xml", status=200)
        else:
            return HttpResponse('Invalid request method')
    except Exception as e:
        return HttpResponseServerError(f'Server Error: {str(e)}')


        

