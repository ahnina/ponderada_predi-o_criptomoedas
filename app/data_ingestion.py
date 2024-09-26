import yfinance as yf
from db_connector import connect_to_db

def fetch_and_store_data():
    conn = connect_to_db()
    cursor = conn.cursor()

    # Baixar dados do BTC
    data = yf.download("BTC-USD", start="2020-01-01", end="2024-01-01")
    data.reset_index(inplace=True)

    for _, row in data.iterrows():
        sql = """INSERT INTO historical_data (symbol, date, open_price, close_price, high_price, low_price, volume)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, ("BTC-USD", row['Date'], row['Open'], row['Close'], row['High'], row['Low'], row['Volume']))
    
    conn.commit()
    cursor.close()
    conn.close()
