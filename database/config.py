import os

class Config:
    # Database path
    DB_PATH = os.path.abspath('news_portal.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False