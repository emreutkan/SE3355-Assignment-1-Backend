from flask import Blueprint, jsonify
from database.database import get_db_connection

weather_bp = Blueprint('weather', __name__)


@weather_bp.route('/weather', methods=['GET'])
def get_weather():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM weather ORDER BY date ASC")
    weather = [dict(row) for row in c.fetchall()]

    conn.close()
    return jsonify(weather)