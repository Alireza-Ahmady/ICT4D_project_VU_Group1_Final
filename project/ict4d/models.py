from django.db import models

class Malaria_case(models.Model):
    """
    Represents a patient who has been diagnosed with malaria.
    """
    gender = models.CharField(max_length=10)
    age = models.PositiveIntegerField()
    date_of_diagnosis = models.DateTimeField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.gender} - {self.date_of_diagnosis}"

