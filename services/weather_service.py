import requests
from datetime import datetime, timedelta
import random
from models.models import WeatherDay, db
from database.database import get_db_connection


def get_day_name(date):
    days = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
    if date.date() == datetime.now().date():
        return 'Bugün'
    return days[date.weekday()]


def get_month_name(month):
    months = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
              'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
    return months[month - 1]


def fetch_weather_data():
    """Fetch weather data from the database"""
    conn = get_db_connection()
    weather_days = []

    try:
        # Query the database for weather data
        weather_records = conn.execute('SELECT * FROM weather').fetchall()

        for record in weather_records:
            # Parse the date
            date_obj = datetime.strptime(record['date'], '%Y-%m-%d')
            day_name = get_day_name(date_obj)
            date_str = f"{date_obj.day} {get_month_name(date_obj.month)}"

            # Map the database condition to Turkish conditions
            conditions_map = {
                "Sunny": "Güneşli",
                "Partly Cloudy": "Parçalı Bulutlu",
                "Cloudy": "Bulutlu",
                "Rainy": "Yağmurlu",
                "Thunderstorm": "Gök Gürültülü Fırtına"
            }

            # Map the database icon to emoji icons
            icons_map = {
                "sun": "☀️",
                "cloud-sun": "🌤️",
                "cloud": "☁️",
                "cloud-rain": "🌧️",
                "cloud-bolt": "⛈️"
            }

            condition = conditions_map.get(record['condition'], "Güneşli")
            icon = icons_map.get(record['icon'], "☀️")

            weather_day = WeatherDay(
                day=day_name,
                date=date_str,
                icon=icon,
                highTemp=record['temp_high'],
                lowTemp=record['temp_low'],
                condition=condition,
                city='Izmir',
                last_updated=datetime.utcnow()
            )
            weather_days.append(weather_day)

    except Exception as e:
        print(f"Error fetching weather data from database: {e}")

    finally:
        conn.close()

    return weather_days


