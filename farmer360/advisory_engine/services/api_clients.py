import requests
from decouple import config

def fetch_nasa_power_data(lat, lon, start_date, end_date):
    """Fetch weather data from NASA POWER API"""
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        'parameters': 'T2M,PRECTOTCORR',
        'community': 'AG',
        'longitude': lon,
        'latitude': lat,
        'start': start_date,
        'end': end_date,
        'format': 'JSON'
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

def fetch_isda_soil_data(lat, lon):
    """Fetch soil data from iSDAsoil API"""
    token = config('ISDA_SOIL_TOKEN')
    headers = {'Authorization': f'Bearer {token}'}
    url = f"https://api.isda-africa.com/v1/soilproperty"
    params = {'lat': lat, 'lon': lon}
    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else None