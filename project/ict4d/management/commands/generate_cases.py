from django.core.management.base import BaseCommand
from ict4d.models import Malaria_case
from random import choice, randint
from django.utils import timezone

class Command(BaseCommand):
    help = 'Generates 100 test cases'

    def handle(self, *args, **kwargs):
        gender_mapping = ['Male', 'Female']
        location_mapping = ['Diabaly', 'Dogofry', 'Kala Siguida', 'Mariko', 'Nampalari', 'Niono', 'Pogo', 'Siribala', 'Sirifila-Boundy', 'Sokolo', 'Toridaga-Ko', 'Yeredon Saniona']
        language_mapping = ['english', 'french']

        for _ in range(100):
            gender = choice(gender_mapping)
            age = randint(1, 100)
            location = choice(location_mapping)
            date_of_diagnosis = timezone.now()
            language = choice(language_mapping)

            malaria_case = Malaria_case(gender=gender, age=age, location=location, date_of_diagnosis=date_of_diagnosis)
            malaria_case.save()

        self.stdout.write(self.style.SUCCESS('Successfully generated test cases'))

