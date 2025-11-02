def analyze_crop_stress(ndvi_value, threshold=0.3):
    """Analyze crop stress based on NDVI values"""
    if ndvi_value < threshold:
        return {
            'status': 'stressed',
            'recommendation': 'Consider irrigation or fertilization'
        }
    return {'status': 'healthy', 'recommendation': 'Continue current practices'}

def irrigation_recommendation(soil_moisture, precipitation):
    """Generate irrigation recommendations"""
    if soil_moisture < 0.2 and precipitation < 5:
        return 'Immediate irrigation recommended'
    elif soil_moisture < 0.4:
        return 'Monitor soil moisture closely'
    return 'No irrigation needed'