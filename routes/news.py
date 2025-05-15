from flask import Blueprint, jsonify
from database.database import get_db_connection

news_bp = Blueprint('news', __name__)


@news_bp.route('/news', methods=['GET'])
def get_news():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM news ORDER BY publish_date DESC")
    news = [dict(row) for row in c.fetchall()]

    conn.close()
    return jsonify(news)


@news_bp.route('/news/<int:news_id>', methods=['GET'])
def get_news_by_id(news_id):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM news WHERE id = ?", (news_id,))
    news = c.fetchone()

    conn.close()

    if news:
        return jsonify(dict(news))
    else:
        return jsonify({"error": "News not found"}), 404