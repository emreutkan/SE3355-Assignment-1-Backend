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

    # Create tables if they don't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS finance_menu (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            has_submenu INTEGER DEFAULT 0,
            parent_id INTEGER DEFAULT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            image_url TEXT NOT NULL,
            content TEXT NOT NULL,
            publish_date TEXT NOT NULL,
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
        _seed_finance_menu(c)
        _seed_news(c)
        _seed_weather(c)
        _seed_currencies(c)

    conn.commit()
    conn.close()


def _seed_finance_menu(cursor):
    # Main menu items
    cursor.execute("INSERT INTO finance_menu (name, url, has_submenu) VALUES (?, ?, ?)",
                   ("Borsa", "/borsa", 1))
    cursor.execute("INSERT INTO finance_menu (name, url, has_submenu) VALUES (?, ?, ?)",
                   ("Döviz", "/doviz", 1))
    cursor.execute("INSERT INTO finance_menu (name, url, has_submenu) VALUES (?, ?, ?)",
                   ("Altın", "/altin", 0))
    cursor.execute("INSERT INTO finance_menu (name, url, has_submenu) VALUES (?, ?, ?)",
                   ("Kripto", "/kripto", 1))
    cursor.execute("INSERT INTO finance_menu (name, url, has_submenu) VALUES (?, ?, ?)",
                   ("Ekonomi", "/ekonomi", 0))

    # Submenu items for Borsa
    cursor.execute("INSERT INTO finance_menu (name, url, parent_id) VALUES (?, ?, ?)",
                   ("BIST 100", "/borsa/bist100", 1))
    cursor.execute("INSERT INTO finance_menu (name, url, parent_id) VALUES (?, ?, ?)",
                   ("BIST 30", "/borsa/bist30", 1))
    cursor.execute("INSERT INTO finance_menu (name, url, parent_id) VALUES (?, ?, ?)",
                   ("En Çok Artanlar", "/borsa/artan", 1))
    cursor.execute("INSERT INTO finance_menu (name, url, parent_id) VALUES (?, ?, ?)",
                   ("En Çok Azalanlar", "/borsa/azalan", 1))

    # Submenu items for Döviz
    cursor.execute("INSERT INTO finance_menu (name, url, parent_id) VALUES (?, ?, ?)",
                   ("Dolar", "/doviz/usd", 2))
    cursor.execute("INSERT INTO finance_menu (name, url, parent_id) VALUES (?, ?, ?)",
                   ("Euro", "/doviz/eur", 2))
    cursor.execute("INSERT INTO finance_menu (name, url, parent_id) VALUES (?, ?, ?)",
                   ("Sterlin", "/doviz/gbp", 2))

    # Submenu items for Kripto
    cursor.execute("INSERT INTO finance_menu (name, url, parent_id) VALUES (?, ?, ?)",
                   ("Bitcoin", "/kripto/btc", 4))
    cursor.execute("INSERT INTO finance_menu (name, url, parent_id) VALUES (?, ?, ?)",
                   ("Ethereum", "/kripto/eth", 4))
    cursor.execute("INSERT INTO finance_menu (name, url, parent_id) VALUES (?, ?, ?)",
                   ("Piyasa Değerine Göre", "/kripto/piyasa", 4))


def _seed_news(cursor):
    news_data = [
        {
            "title": "Ekonomi Dünya Çapında Canlanma Belirtileri Gösteriyor",
            "image_url": "https://picsum.photos/id/1/1200/800",
            "content": "Son ekonomik veriler, dünya çapında bir ekonomik canlanma olduğunu gösteriyor. Uzmanlar bu trendin devam edeceğini öngörüyor.",
            "publish_date": "2025-05-14",
            "url": "/haber/ekonomi-dunyada-canlaniyor"
        },
        {
            "title": "Teknoloji Şirketleri Yatırımlarını Artırıyor",
            "image_url": "https://picsum.photos/id/2/1200/800",
            "content": "Büyük teknoloji şirketleri, yapay zeka ve bulut teknolojilerine yaptıkları yatırımları artırıyor. Bu durum sektörde yeni istihdam fırsatları yaratacak.",
            "publish_date": "2025-05-13",
            "url": "/haber/teknoloji-sirketleri-yatirim"
        },
        {
            "title": "Merkez Bankası Faiz Kararını Açıkladı",
            "image_url": "https://picsum.photos/id/3/1200/800",
            "content": "Merkez Bankası bugün yaptığı toplantıda faiz oranlarını değiştirmeme kararı aldı. Piyasalar bu kararı olumlu karşıladı.",
            "publish_date": "2025-05-12",
            "url": "/haber/merkez-bankasi-faiz-karari"
        },
        {
            "title": "Yeni Enerji Politikaları Açıklandı",
            "image_url": "https://picsum.photos/id/4/1200/800",
            "content": "Hükümet, yenilenebilir enerji kaynaklarına geçişi hızlandıracak yeni politikaları açıkladı. 2030 yılına kadar karbon salınımının %50 azaltılması hedefle[...]",
            "publish_date": "2025-05-11",
            "url": "/haber/yeni-enerji-politikalari"
        },
        {
            "title": "Spor Dünyasında Transferler Hızlandı",
            "image_url": "https://picsum.photos/id/5/1200/800",
            "content": "Yaz transfer sezonu yaklaşırken futbol kulüpleri transfer çalışmalarını hızlandırdı. Büyük takımlar yıldız oyuncular için görüşmelere başladı.",
            "publish_date": "2025-05-10",
            "url": "/haber/spor-transferler-hizlandi"
        },
        {
            "title": "Sağlık Bakanlığı Yeni Aşı Programını Duyurdu",
            "image_url": "https://picsum.photos/id/6/1200/800",
            "content": "Sağlık Bakanlığı, önümüzdeki ay başlayacak yeni aşı programını duyurdu. Program kapsamında tüm vatandaşlar ücretsiz aşılanabilecek.",
            "publish_date": "2025-05-09",
            "url": "/haber/saglik-bakanligi-asi-programi"
        },
        {
            "title": "Otomotiv Sektöründe Elektrikli Araç Atağı",
            "image_url": "https://picsum.photos/id/7/1200/800",
            "content": "Otomotiv üreticileri elektrikli araç üretimine ağırlık veriyor. Önümüzdeki 5 yıl içinde piyasaya sürülecek araçların yarısından fazlasının elektrikli ol[...]",
            "publish_date": "2025-05-08",
            "url": "/haber/otomotiv-elektrikli-araclar"
        },
        {
            "title": "Eğitimde Dijital Dönüşüm Başlıyor",
            "image_url": "https://picsum.photos/id/8/1200/800",
            "content": "Milli Eğitim Bakanlığı, eğitimde dijital dönüşüm projesini hayata geçiriyor. Tüm okullara yüksek hızlı internet ve yeni teknolojik cihazlar sağlanacak.",
            "publish_date": "2025-05-07",
            "url": "/haber/egitimde-dijital-donusum"
        },
        {
            "title": "Emlak Piyasasında Yeni Trend: Akıllı Evler",
            "image_url": "https://picsum.photos/id/9/1200/800",
            "content": "Emlak piyasasında akıllı ev teknolojileriyle donatılmış konutlara olan talep artıyor. Yatırımcılar bu alanda yeni projelere yöneliyor.",
            "publish_date": "2025-05-06",
            "url": "/haber/emlak-akilli-evler"
        },
        {
            "title": "Turizm Sektörü Yeni Sezona Hazırlanıyor",
            "image_url": "https://picsum.photos/id/10/1200/800",
            "content": "Turizm sektörü temsilcileri, bu yıl rekor sayıda turist beklediklerini açıkladı. Otel doluluk oranlarının geçen yıla göre %30 artması öngörülüyor.",
            "publish_date": "2025-05-05",
            "url": "/haber/turizm-yeni-sezon"
        }
    ]

    for news in news_data:
        cursor.execute('''
            INSERT INTO news (title, image_url, content, publish_date, url) 
            VALUES (?, ?, ?, ?, ?)
        ''', (news["title"], news["image_url"], news["content"], news["publish_date"], news["url"]))


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