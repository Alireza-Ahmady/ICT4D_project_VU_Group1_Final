# serializers.py
from rest_framework import serializers

from .models import Malaria_case
from rest_framework import generics

class Malaria_caseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Malaria_case
        fields = ('id', 'gender', 'date_of_diagnosis', 'location')
