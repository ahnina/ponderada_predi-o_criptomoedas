import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Amlshpo7",
        database="crypto_investment_db"
    )
