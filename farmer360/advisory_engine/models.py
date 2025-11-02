from django.db import models
from farm_management.models import FarmField

class WeatherRecord(models.Model):
    field = models.ForeignKey(FarmField, on_delete=models.CASCADE)
    date = models.DateField()
    temperature = models.FloatField()
    precipitation = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class FarmSnapshot(models.Model):
    field = models.ForeignKey(FarmField, on_delete=models.CASCADE)
    ndvi_value = models.FloatField()
    soil_moisture = models.FloatField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)