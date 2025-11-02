from django.core.management.base import BaseCommand
from farm_management.models import FarmField
from advisory_engine.services.api_clients import fetch_nasa_power_data, fetch_isda_soil_data
from advisory_engine.services.advisory_logic import analyze_crop_stress, irrigation_recommendation
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Run scheduled data fetching and advisory generation'

    def handle(self, *args, **options):
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        for field in FarmField.objects.all():
            # Get field centroid for API calls
            centroid = field.geometry.centroid
            lat, lon = centroid.y, centroid.x
            
            # Fetch and process data
            weather_data = fetch_nasa_power_data(lat, lon, yesterday.strftime('%Y%m%d'), today.strftime('%Y%m%d'))
            soil_data = fetch_isda_soil_data(lat, lon)
            
            if weather_data and soil_data:
                self.stdout.write(f'Processed data for field: {field.name}')