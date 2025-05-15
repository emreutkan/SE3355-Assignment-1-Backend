import requests
from datetime import datetime, timedelta
import random
from models.models import WeatherDay, db


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
    """Generate random weather data for Izmir"""
    today = datetime.now()
    weather_days = []

    # Weather conditions and icons
    conditions = ['Güneşli', 'Parçalı Bulutlu', 'Bulutlu', 'Yağmurlu', 'Gök Gürültülü Fırtına']
    icons = ['☀️', '🌤️', '☁️', '🌧️', '⛈️']

    # For 5 days starting from today
    for i in range(5):
        next_day = today + timedelta(days=i)
        day_name = get_day_name(next_day)
        date_str = f"{next_day.day} {get_month_name(next_day.month)}"

        # Generate random temperature range appropriate for Izmir
        high_temp = random.randint(20, 32)  # Izmir is generally warm
        low_temp = high_temp - random.randint(5, 10)  # 5-10 degrees cooler at night

        # Randomly select condition and matching icon
        condition_index = random.randint(0, len(conditions) - 1)

        weather_day = WeatherDay(
            day=day_name,
            date=date_str,
            icon=icons[condition_index],
            highTemp=high_temp,
            lowTemp=low_temp,
            condition=conditions[condition_index],
            city='Izmir',
            last_updated=datetime.utcnow()
        )
        weather_days.append(weather_day)

    return weather_days


def update_weather_data():
    """Generate fresh weather data and update the database"""
    weather_days = fetch_weather_data()

    try:
        # Clear existing data
        db.session.query(WeatherDay).delete()

        # Add new data
        for weather_day in weather_days:
            db.session.add(weather_day)

        db.session.commit()
        return True

    except Exception as e:
        db.session.rollback()
        return False