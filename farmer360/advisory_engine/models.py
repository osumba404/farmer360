from django.db import models
from farm_management.models import FarmField

class WeatherRecord(models.Model):
    farm_field = models.ForeignKey(FarmField, on_delete=models.CASCADE)
    date = models.DateField()
    rainfall_mm = models.FloatField()
    max_temp = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class FarmSnapshot(models.Model):
    farm_field = models.ForeignKey(FarmField, on_delete=models.CASCADE)
    ndvi_value = models.FloatField()
    soil_ph = models.FloatField()
    nitrogen_percent = models.FloatField(default=0.0)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)