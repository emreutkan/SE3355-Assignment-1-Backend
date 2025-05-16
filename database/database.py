import sqlite3
import os
from datetime import datetime, timedelta
from database.config import Config


def get_db_connection():
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    # Check if database already exists
    db_exists = os.path.isfile(Config.DB_PATH)

    conn = sqlite3.connect(Config.DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            image_url TEXT NOT NULL,
            url TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            temp_high REAL NOT NULL,
            temp_low REAL NOT NULL,
            condition TEXT NOT NULL,
            icon TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS currencies (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            code TEXT NOT NULL,
            value REAL NOT NULL,
            change REAL NOT NULL,
            last_updated TEXT NOT NULL
        )
    ''')

    # Only insert seed data if this is a new database
    if not db_exists:
        _seed_news(c)
        _seed_weather(c)
        _seed_currencies(c)

    conn.commit()
    conn.close()


def _seed_news(cursor):
    api_base_url = "https://se3355a1b-dpd2gycrcegubjaz.polandcentral-01.azurewebsites.net"
    news_data = [
        {
            "title": "Uber, Yeni 'Route Share' Hizmetini Başlattı",
            "image_url": f"{api_base_url}/news_1.jpg",
            "url": "https://www.webtekno.com/uber-route-share-hizmeti-h158534.html"
        },
        {
            "title": "Epic Games'te Mega İndirim Fırsatları Başladı",
            "image_url": f"{api_base_url}/news_2.jpg",
            "url": "https://www.webtekno.com/epic-games-indirimli-oyun-h133591.html"
        },
        {
            "title": "Trump'tan Apple CEO'suna Uyarı",
            "image_url": f"{api_base_url}/news_3.jpg",
            "url": "https://www.webtekno.com/trump-apple-ceo-uyari-h158532.html"
        },
        {
            "title": "Google, Kendimi Şanslı Hissediyorum Seçeneğini Kaldırmaya Hazırlanıyor",
            "image_url": f"{api_base_url}/news_4.jpg",
            "url": "https://www.webtekno.com/google-kendimi-sansli-hissediyorum-kaldiriyor-h158523.html"
        },
        {
            "title": "Apple, Harita Uygulamasına Uzman Yorumları Ekledi",
            "image_url": f"{api_base_url}/news_5.jpg",
            "url": "https://www.webtekno.com/apple-harita-uzman-yorumlari-h158520.html"
        },
        {
            "title": "Son Yılların En Yakışıklı Hatchback'i: Yepyeni DS N°4 Tanıtıldı",
            "image_url": f"{api_base_url}/news_6.jpg",
            "url": "https://www.webtekno.com/ds-no4-tanitildi-h158519.html"
        },
        {
            "title": "BYD'nin Egea'nın Üçte Biri Fiyatına Satılacak Elektrikli Otomobili Ortaya Çıktı",
            "image_url": f"{api_base_url}/news_7.jpeg",
            "url": "https://www.webtekno.com/byd-e7-ozellikleri-ortaya-cikti-h158441.html"
        },
        {
            "title": "Son 2 Yıldır Böylesi Görülmedi: Microsoft Binlerce Çalışanını İşten Çıkarıyor!",
            "image_url": f"{api_base_url}/news_8.jpeg",
            "url": "https://www.webtekno.com/microsoft-binlerce-calisanini-isten-cikariyor-h158507.html"
        },
        {
            "title": "Katlanabilir iPhone Ne Zaman Tanıtılacak? ",
            "image_url": f"{api_base_url}/news_9.jpeg",
            "url": "https://www.webtekno.com/katlanabilir-iphone-fiyati-ozellikleri-h158364.html"
        },
        {
            "title": "Arama Motorları Ölüyor ",
            "image_url": f"{api_base_url}/news_10.jpg",
            "url": "https://www.webtekno.com/microsoft-bing-api-sonlandiriyor-h158526.html"
        }
    ]

    for news in news_data:
        cursor.execute('''
            INSERT INTO news (title, image_url, url) 
            VALUES (?, ?, ?)
        ''', (news["title"], news["image_url"], news["url"]))


def _seed_weather(cursor):
    # Generate 5 days of weather data starting from current date
    today = datetime.now()
    weather_conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Thunderstorm"]
    weather_icons = ["sun", "cloud-sun", "cloud", "cloud-rain", "cloud-bolt"]

    for i in range(5):
        day = today + timedelta(days=i)
        date_str = day.strftime('%Y-%m-%d')
        condition_index = i % len(weather_conditions)
        temp_high = 25 + i  # Starting at 25°C and increasing
        temp_low = 15 + i  # Starting at 15°C and increasing

        cursor.execute('''
            INSERT INTO weather (date, temp_high, temp_low, condition, icon) 
            VALUES (?, ?, ?, ?, ?)
        ''', (date_str, temp_high, temp_low, weather_conditions[condition_index], weather_icons[condition_index]))


def _seed_currencies(cursor):
    # Initial currency data
    currencies_data = [
        {"name": "DOLAR", "code": "USD", "value": 37.45, "change": 0.75},
        {"name": "EURO", "code": "EUR", "value": 40.22, "change": -0.32},
        {"name": "STERLİN", "code": "GBP", "value": 48.15, "change": 0.28},
        {"name": "BITCOIN", "code": "BTC", "value": 82500.25, "change": 2.15},
        {"name": "BIST 100", "code": "BIST", "value": 9250.75, "change": 1.25},
        {"name": "ALTIN", "code": "XAU", "value": 3750.50, "change": 0.95},
        {"name": "FAİZ", "code": "INT", "value": 45.00, "change": 0.00}
    ]

    for currency in currencies_data:
        cursor.execute('''
            INSERT INTO currencies (name, code, value, change, last_updated) 
            VALUES (?, ?, ?, ?, ?)
        ''', (
            currency["name"],
            currency["code"],
            currency["value"],
            currency["change"],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))