import requests
from decouple import config

def fetch_nasa_power_data(lat, lon, start_date, end_date):
    """Fetch weather data from NASA POWER API (no key required)"""
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        'parameters': 'PRECTOTCORR,T2M_MAX',
        'community': 'AG',
        'longitude': lon,
        'latitude': lat,
        'start': start_date,
        'end': end_date,
        'format': 'JSON'
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

def get_isda_token():
    """Get Bearer token from iSDAsoil API"""
    url = "https://api.isda-africa.com/v1/login"
    data = {
        'username': config('ISDASOIL_USERNAME'),
        'password': config('ISDASOIL_PASSWORD')
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def fetch_isda_soil_data(lat, lon):
    """Fetch soil data from iSDAsoil API with token authentication"""
    token = get_isda_token()
    if not token:
        return None
    
    headers = {'Authorization': f'Bearer {token}'}
    url = "https://api.isda-africa.com/v1/soilproperty"
    params = {'lat': lat, 'lon': lon, 'property': 'ph,nitrogen'}
    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else None

def fetch_geocledian_ndvi(lat, lon, parcel_id=None):
    """Fetch NDVI data from Geo-Cledian ag|knowledge API"""
    api_key = config('GEOCLEDIAN_API_KEY')
    url = "https://api.geocledian.com/agknow/api/v3/parcels/vitality"
    headers = {'X-API-Key': api_key}
    params = {
        'lat': lat,
        'lon': lon,
        'parcel_id': parcel_id
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else None