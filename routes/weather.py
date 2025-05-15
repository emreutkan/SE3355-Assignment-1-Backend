from flask import Blueprint, jsonify
from models.models import WeatherDay, db
from services.weather_service import update_weather_data

weather_bp = Blueprint('weather', __name__)


@weather_bp.route('/weather', methods=['GET'])
def get_weather():
    """
    Get weather forecast
    ---
    responses:
      200:
        description: Weather forecast for the next 5 days
    """
    weather_days = WeatherDay.query.all()
    return jsonify([weather_day.to_dict() for weather_day in weather_days])


@weather_bp.route('/weather/refresh', methods=['GET'])
def refresh_weather():
    """
    Refresh weather data from API
    ---
    responses:
      200:
        description: Weather data refreshed successfully
      500:
        description: Error refreshing weather data
    """
    success = update_weather_data()

    if success:
        return jsonify({'message': 'Weather data refreshed successfully'})
    else:
        return jsonify({'error': 'Error refreshing weather data'}), 500