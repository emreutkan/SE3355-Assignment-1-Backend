from flask import Blueprint, jsonify
from database.database import get_db_connection
from models.models import Currency, db

finance_bp = Blueprint('finance', __name__)


@finance_bp.route('/finance-menu', methods=['GET'])
def get_finance_menu():
    conn = get_db_connection()
    c = conn.cursor()

    # Get main menu items
    c.execute("SELECT * FROM finance_menu WHERE parent_id IS NULL")
    main_items = [dict(row) for row in c.fetchall()]

    # Get submenu items for each main item
    for item in main_items:
        if item['has_submenu']:
            c.execute("SELECT * FROM finance_menu WHERE parent_id = ?", (item['id'],))
            item['submenu'] = [dict(row) for row in c.fetchall()]
        else:
            item['submenu'] = []

    conn.close()
    return jsonify(main_items)


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


@finance_bp.route('/currencies/<code>', methods=['GET'])
def get_currency(code):
    """
    Get currency by code
    ---
    parameters:
      - name: code
        in: path
        type: string
        required: true
        description: Currency code (e.g., USD, EUR)
    responses:
      200:
        description: Currency details
      404:
        description: Currency not found
    """
    currency = Currency.query.filter_by(code=code.upper()).first()
    if not currency:
        return jsonify({'error': 'Currency not found'}), 404

    return jsonify(currency.to_dict())