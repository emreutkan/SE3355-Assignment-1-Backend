from flask import Blueprint, jsonify
from database.database import get_db_connection
from models.models import Currency, db

finance_bp = Blueprint('finance', __name__)



@finance_bp.route('/currencies', methods=['GET'])
def get_currencies():
    """
    Get all currencies
    ---
    responses:
      200:
        description: List of currencies
    """
    currencies = Currency.query.all()
    return jsonify([currency.to_dict() for currency in currencies])


