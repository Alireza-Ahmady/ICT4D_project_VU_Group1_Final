from django.contrib import admin
from .models import Malaria_case
from django.contrib.admin import AdminSite
from django.contrib import admin
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from .models import Malaria_case

from django.contrib import admin
from .models import Malaria_case
from django.db.models import Count
from django.db.models.functions import TruncMonth
#from django_chartit import DataPool, Chart
from chartit import Chart, PivotDataPool, PivotChart, DataPool
from django.shortcuts import render


class MyAdminSite(AdminSite):
    site_header = 'ICT4D VU 2023'
    site_title = 'Group 1'
    index_title = 'Malaria Cases Mali'


class Malaria_caseAdmin(admin.ModelAdmin):
    list_display = ('id', 'gender', 'age', 'date_of_diagnosis', 'location')
    
    

# Replace the default admin site with our custom site
admin.site = MyAdminSite()
admin.site.register(Malaria_case, Malaria_caseAdmin)