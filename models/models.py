from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Currency(db.Model):
    __tablename__ = 'currencies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(10), nullable=False, unique=True)
    value = db.Column(db.Float, nullable=False)
    change = db.Column(db.Float, nullable=False)
    last_updated = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'value': self.value,
            'change': self.change,
            'last_updated': self.last_updated
        }


class WeatherDay(db.Model):
    __tablename__ = 'weather'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    temp_high = db.Column(db.Float, nullable=False)
    temp_low = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'temp_high': self.temp_high,
            'temp_low': self.temp_low,
            'condition': self.condition,
            'icon': self.icon
        }



class NewsItem(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(500), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'imageUrl': self.image_url,
            'link': self.url,
        }