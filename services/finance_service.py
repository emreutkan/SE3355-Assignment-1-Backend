import requests
from datetime import datetime
import random
from models.models import Currency, db
from database.database import get_db_connection


def fetch_finance_data():
    """Fetch finance data from the database"""
    conn = get_db_connection()
    currencies = []

    try:
        # Query the database for currency records
        currency_records = conn.execute('SELECT * FROM currencies').fetchall()

        for record in currency_records:
            currency = Currency(
                name=record['name'],
                code=record['code'],
                value=record['value'],
                change=record['change'],
                last_updated=datetime.strptime(record['last_updated'], '%Y-%m-%d %H:%M:%S')
            )
            currencies.append(currency)

    except Exception as e:
        print(f"Error fetching currency data from database: {e}")

    finally:
        conn.close()

    return currencies

