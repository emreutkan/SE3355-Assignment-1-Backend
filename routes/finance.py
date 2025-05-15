from flask import Blueprint, jsonify
from database.database import get_db_connection

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