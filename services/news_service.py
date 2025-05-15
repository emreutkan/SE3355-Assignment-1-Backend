from datetime import datetime, timedelta
import random
from models.models import NewsItem, db
import os
import shutil
from PIL import Image, ImageDraw, ImageFont
import io


def generate_image(filename, text):
    """Generate a placeholder image with text and save to newsImages directory"""
    width, height = 800, 400
    background_color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))

    # Create image
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Add text (using default font)
    text_color = (0, 0, 0)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # Draw text in center
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
    text_position = ((width - text_width) // 2, (height - text_height) // 2)
    draw.text(text_position, text, fill=text_color, font=font)

    # Save image
    image_path = os.path.join('newsImages', filename)
    image.save(image_path)

    return f"/newsImages/{filename}"


def fetch_news_data():
    """Generate random news data"""
    now = datetime.now()
    news_items = []

    news_data = [
        {
            'title': 'Pazartesi-Salı-Çarşamba 0\'ın altında KAR İSTANBUL\'A BU GECE SOKULACAK',
            'description': 'İstanbul\'da kar yağışı bekleniyor, sıcaklıklar düşecek.',
            'image_text': 'Kar_Istanbul',
            'link': '/haber/istanbul-kar-yagisi-1'
        },
        {
            'title': 'Dünyanın en zengin kadınları ve servetleri açıklandı',
            'description': 'Forbes dergisi dünyanın en zengin kadınlarını açıkladı.',
            'image_text': 'Zengin_Kadinlar',
            'link': '/haber/dunyanin-en-zengin-kadinlari-2'
        },
        {
            'title': 'Yeni ekonomi paketi açıklandı, piyasalar hareketlendi',
            'description': 'Hükümetin açıkladığı yeni ekonomi paketi piyasalarda olumlu karşılandı.',
            'image_text': 'Ekonomi_Paketi',
            'link': '/haber/ekonomi-paketi-aciklandi-3'
        },
        {
            'title': 'Milli takım kadrosu açıklandı, sürpriz isimler var',
            'description': 'A Milli Futbol Takımı\'nın kadrosunda sürpriz isimler yer aldı.',
            'image_text': 'Milli_Takim',
            'link': '/haber/milli-takim-kadrosu-4'
        },
        {
            'title': 'Ünlü şarkıcıdan yeni albüm müjdesi',
            'description': 'Ünlü şarkıcı, yeni albümünü önümüzdeki ay çıkaracağını duyurdu.',
            'image_text': 'Yeni_Album',
            'link': '/haber/yeni-album-mujdesi-5'
        },
        {
            'title': 'Büyük teknoloji şirketinde istifa depremi',
            'description': 'Dünyanın önde gelen teknoloji şirketinde üst düzey yöneticiler istifa etti.',
            'image_text': 'Teknoloji_Istifa',
            'link': '/haber/teknoloji-sirketi-istifa-6'
        },
        {
            'title': 'Turizm sektörü 2025\'te rekor bekliyor',
            'description': 'Turizm sektörü temsilcileri 2025 yılında rekor sayıda turist bekliyor.',
            'image_text': 'Turizm_Rekor',
            'link': '/haber/turizm-rekor-bekliyor-7'
        },
        {
            'title': 'Yeni nesil elektrikli arabalar yollara çıkıyor',
            'description': 'Çevre dostu yeni elektrikli otomobiller yakında Türkiye\'de satışa sunulacak.',
            'image_text': 'Elektrikli_Arabalar',
            'link': '/haber/elektrikli-arabalar-8'
        },
        {
            'title': 'Sağlık Bakanlığı\'ndan önemli aşı açıklaması',
            'description': 'Sağlık Bakanlığı yeni aşı programını duyurdu.',
            'image_text': 'Asi_Aciklamasi',
            'link': '/haber/asi-aciklamasi-9'
        },
        {
            'title': 'Son dakika: Büyük deprem tatbikatı başlıyor',
            'description': 'Yarın tüm ülkede büyük deprem tatbikatı gerçekleştirilecek.',
            'image_text': 'Deprem_Tatbikati',
            'link': '/haber/deprem-tatbikati-10'
        }
    ]

    for i, news in enumerate(news_data):
        # Generate publication date (within last 7 days)
        days_ago = random.randint(0, 7)
        pub_date = now - timedelta(days=days_ago)

        # Generate and save image
        image_filename = f"news_{i + 1}.jpg"
        image_url = generate_image(image_filename, news['image_text'])

        # Create news item with local image URL
        news_item = NewsItem(
            id=i + 1,
            title=news['title'],
            description=news['description'],
            imageUrl=f"http://127.0.0.1:5000{image_url}",
            link=news['link'],
            publish_date=pub_date
        )
        news_items.append(news_item)

    return news_items


def update_news_data():
    """Generate fresh news data and update the database"""
    news_items = fetch_news_data()

    try:
        # Clear existing data
        db.session.query(NewsItem).delete()

        # Add new data
        for news_item in news_items:
            db.session.add(news_item)

        db.session.commit()
        return True

    except Exception as e:
        db.session.rollback()
        return False