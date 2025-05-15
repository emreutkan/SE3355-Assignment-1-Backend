from database.database import get_db_connection


def check_database_data():
    conn = get_db_connection()

    # Check news data
    print("NEWS DATA:")
    news_data = conn.execute('SELECT * FROM news').fetchall()
    for item in news_data:
        print(f"ID: {item['id']}, Title: {item['title']}, Date: {item['publish_date']}")

    # Check weather data
    print("\nWEATHER DATA:")
    weather_data = conn.execute('SELECT * FROM weather').fetchall()
    for item in weather_data:
        print(
            f"Date: {item['date']}, High: {item['temp_high']}°C, Low: {item['temp_low']}°C, Condition: {item['condition']}")

    # Check if currencies table exists
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='currencies'").fetchall()
    has_currencies = len(tables) > 0

    if has_currencies:
        print("\nCURRENCY DATA:")
        currency_data = conn.execute('SELECT * FROM currencies').fetchall()
        for item in currency_data:
            print(f"Name: {item['name']}, Code: {item['code']}, Value: {item['value']}")
    else:
        print("\nCurrencies table does not exist yet.")

    conn.close()


# Run the function
if __name__ == "__main__":
    check_database_data()