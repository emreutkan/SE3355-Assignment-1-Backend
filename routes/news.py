from flask import Blueprint, jsonify
from models.models import NewsItem, db
from services.news_service import update_news_data

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
    news_items = NewsItem.query.order_by(NewsItem.publish_date.desc()).all()
    return jsonify([news.to_dict() for news in news_items])


@news_bp.route('/news/<int:id>', methods=['GET'])
def get_news_item(id):
    """
    Get news by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: News item ID
    responses:
      200:
        description: News item details
      404:
        description: News item not found
    """
    news_item = NewsItem.query.get(id)
    if not news_item:
        return jsonify({'error': 'News item not found'}), 404

    return jsonify(news_item.to_dict())


@news_bp.route('/news/refresh', methods=['GET'])
def refresh_news():
    """
    Refresh news data
    ---
    responses:
      200:
        description: News data refreshed successfully
      500:
        description: Error refreshing news data
    """
    success = update_news_data()

    if success:
        return jsonify({'message': 'News data refreshed successfully'})
    else:
        return jsonify({'error': 'Error refreshing news data'}), 500