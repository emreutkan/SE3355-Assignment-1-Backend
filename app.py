from flask import Flask
from flask_cors import CORS
from config import Config
from routes.finance import finance_bp
from routes.news import news_bp
from routes.weather import weather_bp
from database import init_db
from flasgger import Swagger

app = Flask(__name__)
CORS(app)

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

# Initialize the database when the app starts
init_db()

if __name__ == '__main__':
    app.run(debug=True)