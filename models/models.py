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
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'value': self.value,
            'change': self.change,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }


class WeatherDay(db.Model):
    __tablename__ = 'weather_days'

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    icon = db.Column(db.String(20), nullable=False)
    highTemp = db.Column(db.Integer, nullable=False)
    lowTemp = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), default='Izmir')
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'day': self.day,
            'date': self.date,
            'icon': self.icon,
            'highTemp': self.highTemp,
            'lowTemp': self.lowTemp,
            'condition': self.condition,
            'city': self.city,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }


class NewsItem(db.Model):
    __tablename__ = 'news_items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    imageUrl = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'imageUrl': self.imageUrl,
            'link': self.link,
            'publish_date': self.publish_date.isoformat() if self.publish_date else None
        }