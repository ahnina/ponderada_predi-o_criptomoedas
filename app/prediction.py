import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split
from keras.losses import MeanSquaredError
import pandas as pd
from datetime import datetime, timedelta
from db_connector import connect_to_db

# Função para tratamento de dados e preparação
def preprocess_and_predict(btc, user_date, n_days=7, window_size=8):
    # Converte a coluna 'date' para datetime
    btc['date'] = pd.to_datetime(btc['date'])

    # Filtrar dados até a data consultada
    btc_filtered = btc[btc['date'] <= pd.to_datetime(user_date)]

    # Checar se há dados suficientes
    if len(btc_filtered) < window_size:
        raise ValueError("Não há dados suficientes para a janela especificada.")

    # Focar apenas na coluna 'close_price'
    btc_filtered = btc_filtered[['date', 'close_price']]
    
    # Normalizar a coluna 'close_price'
    scaler = MinMaxScaler()
    btc_filtered['close_price'] = scaler.fit_transform(btc_filtered[['close_price']])

    # Preparar a janela de dados (últimos 8 dias)
    last_window = btc_filtered['close_price'].values[-window_size:]

    # Carregar o modelo pré-treinado
    model = load_model('../models/modelo_btc.h5', compile=False)

    # Fazer previsões para os próximos 7 dias
    predictions = []
    for _ in range(n_days):
        # Expandir dimensões para (1, 8, 1)
        input_data = np.expand_dims(last_window, axis=0)  # Formato: (1, 8, 1)
        
        # Prever o próximo 'close_price'
        predicted_close = model.predict(input_data)
        predictions.append(predicted_close[0, 0])

        # Atualizar a janela deslizante
        last_window = np.append(last_window[1:], predicted_close)  # Adiciona a nova previsão

    # Inverter a normalização
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    
    return predictions

def salvar_predicao(prediction, n_days =7):
    # Gerar as datas para os próximos dias
    today = datetime.today().date()
    future_dates = [today + timedelta(days=i) for i in range(1, n_days + 1)]

    # Criar um DataFrame com as datas e as previsões
    predictions = pd.DataFrame({
        'date': future_dates,
        'predicted_price': prediction.flatten()  # Ajustar para garantir a forma correta
    })

    # Armazenar previsões no banco de dados
    conn = connect_to_db()
    cursor = conn.cursor()

    # Inserir as previsões na tabela
    for index, row in predictions.iterrows():
        cursor.execute("""
            INSERT INTO predictions (prediction_date, predicted_close)
            VALUES (%s, %s)
        """, (row['date'], row['predicted_price']))
    
    conn.commit()  # Confirmar a transação
    cursor.close()
    conn.close()


