from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FarmField
from advisory_engine.models import FarmSnapshot, WeatherRecord
from advisory_engine.services.advisory_logic import (
    irrigation_advisory, fertilization_advisory, crop_health_advisory
)
from datetime import datetime, timedelta

def get_field_data(user):
    """Helper function to get field data with health status and advisories"""
    fields = FarmField.objects.filter(owner=user)
    field_data = []
    
    for field in fields:
        latest_snapshot = FarmSnapshot.objects.filter(farm_field=field).order_by('-date').first()
        health_status = 'green'
        
        if latest_snapshot:
            if latest_snapshot.ndvi_value < 0.3:
                health_status = 'red'
            elif latest_snapshot.ndvi_value < 0.5:
                health_status = 'yellow'
        
        advisories = []
        for advisory_func in [irrigation_advisory, fertilization_advisory, crop_health_advisory]:
            advisory = advisory_func(field)
            if advisory:
                advisories.append(advisory)
        
        field_data.append({
            'field': field,
            'health_status': health_status,
            'advisories': advisories,
            'latest_snapshot': latest_snapshot
        })
    
    return field_data

def dashboard(request):
    if not request.user.is_authenticated:
        return render(request, 'farm_management/dashboard.html', {'field_data': []})
    field_data = get_field_data(request.user)
    return render(request, 'farm_management/dashboard.html', {'field_data': field_data})

@login_required
def fields(request):
    field_data = get_field_data(request.user)
    return render(request, 'farm_management/fields.html', {'field_data': field_data})

@login_required
def field_detail(request, field_id):
    field = get_object_or_404(FarmField, id=field_id, owner=request.user)
    latest_snapshot = FarmSnapshot.objects.filter(farm_field=field).order_by('-date').first()
    
    health_status = 'green'
    if latest_snapshot:
        if latest_snapshot.ndvi_value < 0.3:
            health_status = 'red'
        elif latest_snapshot.ndvi_value < 0.5:
            health_status = 'yellow'
    
    # Get recent weather data
    week_ago = datetime.now().date() - timedelta(days=7)
    weather_records = WeatherRecord.objects.filter(
        farm_field=field, date__gte=week_ago
    ).order_by('-date')
    
    # Get advisories
    advisories = []
    for advisory_func in [irrigation_advisory, fertilization_advisory, crop_health_advisory]:
        advisory = advisory_func(field)
        if advisory:
            advisories.append(advisory)
    
    context = {
        'field': field,
        'latest_snapshot': latest_snapshot,
        'health_status': health_status,
        'weather_records': weather_records,
        'advisories': advisories
    }
    return render(request, 'farm_management/field_detail.html', context)

@login_required
def analytics(request):
    field_data = get_field_data(request.user)
    
    total_fields = len(field_data)
    healthy_fields = sum(1 for data in field_data if data['health_status'] == 'green')
    fields_need_attention = sum(1 for data in field_data if data['advisories'])
    
    # Calculate average NDVI
    ndvi_values = [data['latest_snapshot'].ndvi_value for data in field_data if data['latest_snapshot']]
    avg_ndvi = sum(ndvi_values) / len(ndvi_values) if ndvi_values else 0
    
    # Advisory statistics
    all_advisories = []
    for data in field_data:
        all_advisories.extend(data['advisories'])
    
    advisory_stats = {
        'urgent': sum(1 for a in all_advisories if a['priority'] == 'URGENT'),
        'recommendations': sum(1 for a in all_advisories if a['priority'] == 'RECOMMENDATION'),
        'alerts': sum(1 for a in all_advisories if a['priority'] == 'ALERT')
    } if all_advisories else None
    
    context = {
        'field_data': field_data,
        'total_fields': total_fields,
        'healthy_fields': healthy_fields,
        'fields_need_attention': fields_need_attention,
        'avg_ndvi': avg_ndvi,
        'advisory_stats': advisory_stats
    }
    return render(request, 'farm_management/analytics.html', context)

@login_required
def advisories(request):
    field_data = get_field_data(request.user)
    
    all_advisories = {}
    urgent_count = recommendation_count = alert_count = 0
    
    for data in field_data:
        if data['advisories']:
            all_advisories[data['field'].name] = data['advisories']
            for advisory in data['advisories']:
                if advisory['priority'] == 'URGENT':
                    urgent_count += 1
                elif advisory['priority'] == 'RECOMMENDATION':
                    recommendation_count += 1
                elif advisory['priority'] == 'ALERT':
                    alert_count += 1
    
    context = {
        'all_advisories': all_advisories,
        'urgent_count': urgent_count,
        'recommendation_count': recommendation_count,
        'alert_count': alert_count
    }
    return render(request, 'farm_management/advisories.html', context)

@login_required
def profile(request):
    field_data = get_field_data(request.user)
    
    total_fields = len(field_data)
    healthy_fields = sum(1 for data in field_data if data['health_status'] == 'green')
    
    # Calculate average NDVI
    ndvi_values = [data['latest_snapshot'].ndvi_value for data in field_data if data['latest_snapshot']]
    avg_ndvi = sum(ndvi_values) / len(ndvi_values) if ndvi_values else 0
    
    context = {
        'field_data': field_data,
        'total_fields': total_fields,
        'healthy_fields': healthy_fields,
        'avg_ndvi': avg_ndvi
    }
    return render(request, 'farm_management/profile.html', context)

@login_required
def map_view(request):
    return render(request, 'farm_management/map_edit.html')