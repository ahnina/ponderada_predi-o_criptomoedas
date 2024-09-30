import yfinance as yf
from db_connector import connect_to_db
from datetime import datetime

def fetch_and_store_data():
    # Obter a data atual para garantir que os dados sejam sempre atualizados até o dia da previsão
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    conn = connect_to_db()
    cursor = conn.cursor()

    # Baixar dados do BTC até a data atual
    data = yf.download("BTC-USD", start="2020-01-01", end=end_date)
    data.reset_index(inplace=True)

    for _, row in data.iterrows():
        sql = """INSERT INTO historical_data (symbol, date, open_price, close_price, high_price, low_price, volume)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)
                 ON DUPLICATE KEY UPDATE
                 open_price = VALUES(open_price), close_price = VALUES(close_price),
                 high_price = VALUES(high_price), low_price = VALUES(low_price), volume = VALUES(volume)"""
        cursor.execute(sql, ("BTC-USD", row['Date'], row['Open'], row['Close'], row['High'], row['Low'], row['Volume']))
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    fetch_and_store_data()
