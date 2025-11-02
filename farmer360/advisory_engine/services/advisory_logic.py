from datetime import datetime, timedelta
from advisory_engine.models import WeatherRecord, FarmSnapshot

def irrigation_advisory(farm_field):
    """Generate irrigation advisory based on rainfall and NDVI trends"""
    # Get 7-day rainfall data
    week_ago = datetime.now().date() - timedelta(days=7)
    rainfall_records = WeatherRecord.objects.filter(
        farm_field=farm_field,
        date__gte=week_ago
    )
    total_rainfall = sum(record.rainfall_mm for record in rainfall_records)
    
    # Get NDVI trend
    recent_snapshots = FarmSnapshot.objects.filter(
        farm_field=farm_field,
        date__gte=week_ago
    ).order_by('-date')[:2]
    
    if len(recent_snapshots) >= 2 and total_rainfall < 10:
        ndvi_trend = recent_snapshots[0].ndvi_value - recent_snapshots[1].ndvi_value
        if ndvi_trend < 0:  # NDVI dropping
            return {
                'priority': 'URGENT',
                'message': 'Initiate irrigation. Drought stress detected.',
                'action': f'Focus on field: {farm_field.name}'
            }
    return None

def fertilization_advisory(farm_field, crop_type='maize'):
    """Generate fertilization advisory based on soil nitrogen"""
    latest_snapshot = FarmSnapshot.objects.filter(
        farm_field=farm_field
    ).order_by('-date').first()
    
    if latest_snapshot and crop_type.lower() == 'maize':
        if latest_snapshot.nitrogen_percent < 0.1:
            return {
                'priority': 'RECOMMENDATION',
                'message': 'Apply Nitrogen-rich fertilizer (Urea) immediately',
                'reason': 'Soil tests show low nitrogen levels'
            }
    return None

def crop_health_advisory(farm_field):
    """Generate crop health advisory based on NDVI drops"""
    week_ago = datetime.now().date() - timedelta(days=7)
    snapshots = FarmSnapshot.objects.filter(
        farm_field=farm_field,
        date__gte=week_ago
    ).order_by('-date')[:2]
    
    if len(snapshots) >= 2:
        ndvi_change = (snapshots[1].ndvi_value - snapshots[0].ndvi_value) / snapshots[1].ndvi_value
        if ndvi_change > 0.15:  # 15% drop
            return {
                'priority': 'ALERT',
                'message': 'Significant crop stress detected',
                'action': 'Conduct field inspection for pests/disease'
            }
    return None