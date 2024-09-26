# import mysql.connector
from db_connector import connect_to_db
import pandas as pd

# Função para carregar dados do banco de dados MySQL
def load_crypto_data_from_db():
    # Conectar ao banco de dados
    connection = connect_to_db()

    # Query para selecionar os dados desejados
    query = "SELECT * FROM historical_data"

    # Carregar os dados diretamente do banco em um DataFrame
    btc = pd.read_sql(query, connection)

    # Fechar a conexão com o banco
    connection.close()

    return btc
