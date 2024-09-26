from keras.models import load_model
from db_connector import connect_to_db
from keras.losses import MeanSquaredError
import pandas as pd

def fetch_historical_data():
    model = load_model('../models/modelo_btc.h5', custom_objects={'mse': MeanSquaredError()})


    # Conectar ao banco para pegar dados
    conn = connect_to_db()
    query = "SELECT open_price, close_price, high_price, low_price, volume FROM historical_data ORDER BY date DESC LIMIT 7"
    data = pd.read_sql(query, conn)
    conn.close()

    # Pré-processar os dados conforme necessário pelo modelo
    # Normalizar, ajustar shape, etc.
    predicted_value = model.predict(data)
    return predicted_value


# Função para preprocessar os dados
def preprocess_data(btc_hist):
    # Excluindo colunas "Dividends" e "Stock Splits"
    btc = btc_hist.drop(columns=["Dividends", "Stock Splits"])
    
    # Converter a coluna Date para o tipo datetime, se ainda não estiver
    btc['Date'] = pd.to_datetime(btc['Date'])

    # Extrair componentes da data
    btc['Year'] = btc['Date'].dt.year
    btc['Month'] = btc['Date'].dt.month
    btc['Day'] = btc['Date'].dt.day
    btc['Weekday'] = btc['Date'].dt.weekday  # Segunda-feira = 0, Domingo = 6
    btc['DayOfYear'] = btc['Date'].dt.dayofyear
    btc['Quarter'] = btc['Date'].dt.quarter

    # Excluir a coluna original 'Date'
    btc = btc.drop(columns=['Date'])

    # Normalizando dados
    scaler = MinMaxScaler()

    # Normalizar todas as colunas
    btc = pd.DataFrame(scaler.fit_transform(btc), columns=btc.columns)

    # Separando as features (X) e o target (y)
    X = btc.drop(columns=['Close', 'High', 'Low'])  # Ajuste conforme necessário
    y = btc['Close']

    # Dividir os dados em treino e teste (a lógica de divisão deve ser aplicada conforme sua necessidade)
    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # Converte X_train e X_test para arrays NumPy, caso ainda não sejam.
    X_train = np.array(X_train)
    X_test = np.array(X_test)

    # Reestrutura X_train e X_test para ter 3 dimensões.
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

    return X_train, X_test, y_train, y_test, scaler

# Função principal de previsão
def make_prediction():
    # Carregar o modelo
    model = load_model('models/seu_modelo.h5')

    # Obter dados históricos
    btc_hist = fetch_historical_data()

    # Preprocessar os dados
    X_train, X_test, y_train, y_test, scaler = preprocess_data(btc_hist)

    # Fazer previsões
    predictions = model.predict(X_test)

    # Inverter a normalização para as previsões
    predictions = scaler.inverse_transform(predictions)

    return predictions

# Chamando a função de previsão
if __name__ == "__main__":
    predictions = make_prediction()
    print(predictions)

