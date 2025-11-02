from django.shortcuts import render
from .models import FarmField

def dashboard(request):
    fields = FarmField.objects.filter(owner=request.user) if request.user.is_authenticated else []
    return render(request, 'farm_management/dashboard.html', {'fields': fields})

def map_view(request):
    return render(request, 'farm_management/map_edit.html')