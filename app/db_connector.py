import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="  ",
        user="root",
        password="Amlshpo7",
        database="crypto_investment_db"
    )
