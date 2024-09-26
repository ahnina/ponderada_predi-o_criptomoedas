import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split

# Função para tratamento de dados e preparação
def preprocess_and_predict(btc):
    # Tratamento de dados
    # Excluir colunas "Dividends" e "Stock Splits"
    # btc = btc_hist.drop(columns=["Dividends", "Stock Splits"])

    # Converter a coluna Date para o tipo datetime
    btc['date'] = pd.to_datetime(btc['date'])

    # Extrair componentes da data
    btc['Year'] = btc['date'].dt.year
    btc['Month'] = btc['date'].dt.month
    btc['Day'] = btc['date'].dt.day
    btc['Weekday'] = btc['date'].dt.weekday
    btc['DayOfYear'] = btc['date'].dt.dayofyear
    btc['Quarter'] = btc['date'].dt.quarter

    # Excluir a coluna 'Date'
    btc = btc.drop(columns=['date'])

    # Normalizar dados
    scaler = MinMaxScaler()
    btc = pd.DataFrame(scaler.fit_transform(btc), columns=btc.columns)

    # Separar as features (X) e o target (y)
    X = btc.drop(columns=['close_price', 'high_price', 'low_price'])
    y = btc['close_price']

    X = X.values.reshape((X.shape[0], X.shape[1], 1))


    # Carregar o modelo pré-treinado
    model = load_model('model/seu_modelo.h5')

    # Fazer a previsão
    predictions = model.predict(X)

    return predictions

