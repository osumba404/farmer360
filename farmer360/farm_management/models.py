from django.contrib.gis.db import models
from django.contrib.auth.models import User

class FarmField(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    geometry = models.PolygonField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.owner.username}"