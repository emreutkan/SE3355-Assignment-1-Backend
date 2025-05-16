from flask import Flask, send_from_directory
from flask_cors import CORS
from database.config import Config
from routes.finance import finance_bp
from routes.news import news_bp
from routes.weather import weather_bp
from database.database import init_db
from flasgger import Swagger
from models.models import db

import os

app = Flask(__name__)
CORS(app)

# Configure SQLAlchemy
app.config.from_object(Config)
db.init_app(app)

# Configure Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/"
}

swagger = Swagger(app, config=swagger_config)

# Register blueprints
app.register_blueprint(finance_bp, url_prefix='/api')
app.register_blueprint(news_bp, url_prefix='/api')
app.register_blueprint(weather_bp, url_prefix='/api')

# Initialize database
with app.app_context():
    init_db()


if __name__ == '__main__':
    app.run(debug=True)