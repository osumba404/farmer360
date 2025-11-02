# Farmer360 - Precision Advisory System

Farmer360 is a web-based Precision Advisory System designed to empower African smallholder farmers with data-driven recommendations. It automatically integrates free satellite, climate, and soil data for specific farm fields to deliver timely, actionable advice on irrigation, fertilization, and crop stress.

## Features

- **Field Management**: Create and manage farm fields with interactive mapping
- **Real-time Monitoring**: Track NDVI, soil pH, nitrogen levels, and weather data
- **Smart Advisories**: Automated recommendations for irrigation, fertilization, and crop health
- **Health Indicators**: Visual field status with color-coded health indicators
- **Analytics Dashboard**: Comprehensive farm performance analytics
- **Multi-API Integration**: NASA POWER, iSDAsoil, and Geo-Cledian APIs

## Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite (development) / PostgreSQL + PostGIS (production)
- **Frontend**: HTML, CSS, JavaScript
- **Mapping**: Leaflet.js
- **APIs**: NASA POWER, iSDAsoil, Geo-Cledian
- **Task Queue**: Celery (optional)

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd farmer360
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API credentials
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Start development server:
```bash
python manage.py runserver
```

7. Visit `http://127.0.0.1:8000` to access the application

## API Configuration

Add these credentials to your `.env` file:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ISDASOIL_USERNAME=your-isda-username
ISDASOIL_PASSWORD=your-isda-password
GEOCLEDIAN_API_KEY=your-geocledian-api-key
```

### API Sources
- **NASA POWER**: Weather and climate data (no key required)
- **iSDAsoil**: Soil properties for Africa (free registration)
- **Geo-Cledian**: NDVI and crop health data (free developer account)

## Usage

1. **Sign Up/Login**: Create an account or login
2. **Add Fields**: Use the interactive map to create farm fields
3. **Monitor Data**: View real-time field health and measurements
4. **Receive Advisories**: Get automated recommendations based on:
   - Irrigation needs (rainfall + NDVI trends)
   - Fertilization requirements (soil nitrogen levels)
   - Crop health alerts (NDVI decline detection)

## Data Fetching

Run the scheduler to fetch latest data:
```bash
python manage.py run_scheduler
```

## Project Structure

```
farmer360/
├── farmer360/              # Main Django project
│   ├── settings.py        # Configuration
│   └── urls.py           # URL routing
├── farm_management/       # User interface app
│   ├── models.py         # FarmField model
│   ├── views.py          # UI views
│   └── templates/        # HTML templates
├── advisory_engine/       # Data processing app
│   ├── models.py         # Data models
│   ├── services/         # API clients
│   └── management/       # Scheduler commands
└── requirements.txt       # Dependencies
```

## Advisory Logic

- **Irrigation**: Triggered when 7-day rainfall < 10mm AND NDVI declining
- **Fertilization**: Activated for maize crops with nitrogen < 0.1%
- **Crop Health**: Alerts when NDVI drops > 15% in 7 days

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

## License

MIT License - see LICENSE file for details