from flask import Flask, send_from_directory
from flask_cors import CORS
from database.config import Config
from routes.finance import finance_bp
from routes.news import news_bp
from routes.weather import weather_bp
from database.database import init_db
from flasgger import Swagger
from models.models import db
from services.weather_service import update_weather_data
from services.finance_service import update_finance_data
from services.news_service import update_news_data
import os

app = Flask(__name__)
CORS(app)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{Config.DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

# Create directory for news images if it doesn't exist
os.makedirs('newsImages', exist_ok=True)

@app.route('/newsImages/<path:filename>')
def serve_news_images(filename):
    return send_from_directory('newsImages', filename)

# Register blueprints
app.register_blueprint(finance_bp, url_prefix='/api')
app.register_blueprint(news_bp, url_prefix='/api')
app.register_blueprint(weather_bp, url_prefix='/api')

# Initialize the database when the app starts
init_db()

with app.app_context():
    db.create_all()
    # Update data with random or API data
    update_weather_data()
    update_finance_data()
    update_news_data()

if __name__ == '__main__':
    app.run(debug=True)