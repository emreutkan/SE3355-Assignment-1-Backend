from datetime import datetime, timedelta
import random
from models.models import NewsItem, db
import os
import shutil
from PIL import Image, ImageDraw, ImageFont
import io
from database.database import get_db_connection


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
    """Fetch news data from the database"""
    conn = get_db_connection()
    news_items = []

    try:
        # Query the database for news items
        news_records = conn.execute('SELECT * FROM news').fetchall()

        for i, record in enumerate(news_records):
            # Generate a local image for each news item
            image_text = f"News_{i + 1}"
            image_filename = f"news_{i + 1}.jpg"
            image_url = generate_image(image_filename, image_text)

            # Create NewsItem object with data from database
            news_item = NewsItem(
                id=record['id'],
                title=record['title'],
                content=record['content'],
                image_url=f"http://127.0.0.1:5000{image_url}",
                url=record['url'],
                publish_date=record['publish_date']
            )
            news_items.append(news_item)

    except Exception as e:
        print(f"Error fetching news data from database: {e}")

    finally:
        conn.close()

    return news_items

