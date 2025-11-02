from django.core.management.base import BaseCommand
from farm_management.models import FarmField
from advisory_engine.models import WeatherRecord, FarmSnapshot
from advisory_engine.services.api_clients import (
    fetch_nasa_power_data, fetch_isda_soil_data, fetch_geocledian_ndvi
)
from advisory_engine.services.advisory_logic import (
    irrigation_advisory, fertilization_advisory, crop_health_advisory
)
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Run scheduled data fetching and advisory generation'

    def handle(self, *args, **options):
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        for field in FarmField.objects.all():
            lat, lon = field.latitude, field.longitude
            
            # Fetch weather data
            weather_data = fetch_nasa_power_data(
                lat, lon, yesterday.strftime('%Y%m%d'), today.strftime('%Y%m%d')
            )
            
            # Fetch soil data
            soil_data = fetch_isda_soil_data(lat, lon)
            
            # Fetch NDVI data
            ndvi_data = fetch_geocledian_ndvi(lat, lon)
            
            # Store weather data
            if weather_data and 'properties' in weather_data:
                props = weather_data['properties']['parameter']
                if 'PRECTOTCORR' in props and 'T2M_MAX' in props:
                    for date_str, rainfall in props['PRECTOTCORR'].items():
                        WeatherRecord.objects.update_or_create(
                            farm_field=field,
                            date=yesterday,
                            defaults={
                                'rainfall_mm': rainfall,
                                'max_temp': props['T2M_MAX'].get(date_str, 0)
                            }
                        )
            
            # Store farm snapshot
            if soil_data and ndvi_data:
                FarmSnapshot.objects.update_or_create(
                    farm_field=field,
                    date=today,
                    defaults={
                        'ndvi_value': ndvi_data.get('ndvi', 0),
                        'soil_ph': soil_data.get('ph', 7.0),
                        'nitrogen_percent': soil_data.get('nitrogen', 0.0)
                    }
                )
            
            # Generate advisories
            advisories = []
            advisories.append(irrigation_advisory(field))
            advisories.append(fertilization_advisory(field))
            advisories.append(crop_health_advisory(field))
            
            active_advisories = [a for a in advisories if a]
            if active_advisories:
                self.stdout.write(f'Generated {len(active_advisories)} advisories for {field.name}')
            else:
                self.stdout.write(f'No advisories needed for {field.name}')