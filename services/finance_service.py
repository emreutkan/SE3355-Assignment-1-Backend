import requests
from datetime import datetime
import random
from models.models import Currency, db


def fetch_finance_data():
    """Generate random finance data"""
    try:
        # Try to get basic exchange rates from a free API with no key required
        response = requests.get('https://open.er-api.com/v6/latest/TRY', timeout=5)

        if response.status_code == 200:
            data = response.json()
            rates = data.get('rates', {})

            currencies = []

            # USD (Dollar)
            if 'USD' in rates and rates['USD'] > 0:
                usd_rate = 1 / rates['USD']
                currencies.append(Currency(
                    name='DOLAR',
                    code='USD',
                    value=round(usd_rate, 2),
                    change=round(random.uniform(-2.5, 2.5), 2),
                    last_updated=datetime.utcnow()
                ))

            # EUR (Euro)
            if 'EUR' in rates and rates['EUR'] > 0:
                eur_rate = 1 / rates['EUR']
                currencies.append(Currency(
                    name='EURO',
                    code='EUR',
                    value=round(eur_rate, 2),
                    change=round(random.uniform(-2.5, 2.5), 2),
                    last_updated=datetime.utcnow()
                ))

            # GBP (Sterling)
            if 'GBP' in rates and rates['GBP'] > 0:
                gbp_rate = 1 / rates['GBP']
                currencies.append(Currency(
                    name='STERLİN',
                    code='GBP',
                    value=round(gbp_rate, 2),
                    change=round(random.uniform(-2.5, 2.5), 2),
                    last_updated=datetime.utcnow()
                ))

            # If we got real data for the main currencies, add random data for others
            if currencies:
                # Add other currencies with random data
                currencies.extend(_get_random_other_currencies())
                return currencies

    except Exception as e:
        pass

    # If API call failed or returned invalid data, generate all random data
    return _get_all_random_currencies()


def _get_random_other_currencies():
    """Generate random data for non-major currencies"""
    return [
        Currency(
            name='BIST 100',
            code='BIST',
            value=round(random.uniform(8000, 10000), 2),
            change=round(random.uniform(-2.5, 2.5), 2),
            last_updated=datetime.utcnow()
        ),
        Currency(
            name='ALTIN',
            code='XAU',
            value=round(random.uniform(3500, 4000), 2),
            change=round(random.uniform(-2.5, 2.5), 2),
            last_updated=datetime.utcnow()
        ),
        Currency(
            name='FAİZ',
            code='INT',
            value=round(random.uniform(40, 50), 2),
            change=0.00,
            last_updated=datetime.utcnow()
        ),
        Currency(
            name='BITCOIN',
            code='BTC',
            value=round(random.uniform(75000, 90000), 2),
            change=round(random.uniform(-5, 5), 2),
            last_updated=datetime.utcnow()
        )
    ]


def _get_all_random_currencies():
    """Generate random data for all currencies"""
    return [
        Currency(name='DOLAR', code='USD', value=round(random.uniform(35, 40), 2),
                 change=round(random.uniform(-2.5, 2.5), 2)),
        Currency(name='EURO', code='EUR', value=round(random.uniform(38, 45), 2),
                 change=round(random.uniform(-2.5, 2.5), 2)),
        Currency(name='STERLİN', code='GBP', value=round(random.uniform(45, 55), 2),
                 change=round(random.uniform(-2.5, 2.5), 2)),
        Currency(name='BITCOIN', code='BTC', value=round(random.uniform(75000, 90000), 2),
                 change=round(random.uniform(-5, 5), 2)),
        Currency(name='BIST 100', code='BIST', value=round(random.uniform(8000, 10000), 2),
                 change=round(random.uniform(-2.5, 2.5), 2)),
        Currency(name='ALTIN', code='XAU', value=round(random.uniform(3500, 4000), 2),
                 change=round(random.uniform(-2.5, 2.5), 2)),
        Currency(name='FAİZ', code='INT', value=round(random.uniform(40, 50), 2), change=0.00)
    ]


def update_finance_data():
    """Fetch fresh finance data and update the database"""
    currencies = fetch_finance_data()

    try:
        # Clear existing data
        db.session.query(Currency).delete()

        # Add new data
        for currency in currencies:
            db.session.add(currency)

        db.session.commit()
        return True

    except Exception as e:
        db.session.rollback()
        return False