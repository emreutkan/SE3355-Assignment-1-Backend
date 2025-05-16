from flask import Blueprint, jsonify
from models.models import NewsItem, db

news_bp = Blueprint('news', __name__)


@news_bp.route('/news', methods=['GET'])
def get_news():
    """
    Get all news
    ---
    responses:
      200:
        description: List of news articles
    """
    news_items = NewsItem.query.order_by(NewsItem.id.asc()).all()
    return jsonify([news.to_dict() for news in news_items])


