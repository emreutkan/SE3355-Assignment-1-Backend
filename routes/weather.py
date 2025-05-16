from flask import Blueprint, jsonify
from models.models import WeatherDay, db

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


