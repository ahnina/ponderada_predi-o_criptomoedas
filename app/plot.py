import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64
from db_connector import connect_to_db

def generate_close_price_plot():
    conn = connect_to_db()

    # Consultar os preços de fechamento dos últimos 30 dias
    query = """
    SELECT date, close_price 
    FROM historical_data 
    WHERE date >= NOW() - INTERVAL 30 DAY
    ORDER BY date ASC;
    """
    historical_data = pd.read_sql(query, conn)

    # Consultar as previsões para os próximos 7 dias
    query_pred = """
    SELECT prediction_date, predicted_close
    FROM predictions 
    WHERE prediction_date >= CURDATE() AND prediction_date < CURDATE() + INTERVAL 7 DAY
    ORDER BY prediction_date ASC;
    """
    predicted_data = pd.read_sql(query_pred, conn)
    conn.close()

    # Concatenar os dados históricos com as previsões
    historical_data['date'] = pd.to_datetime(historical_data['date'])
    predicted_data['prediction_date'] = pd.to_datetime(predicted_data['prediction_date'])
    combined_data = pd.concat([historical_data, predicted_data])

    # Criar gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(combined_data['date'], combined_data['close_price'], marker='o', label='Preços Históricos')
    plt.plot(predicted_data['prediction_date'], predicted_data['predicted_close'], marker='x', linestyle='--', color='orange', label='Previsões')
    plt.title('Close Price e Previsões para os Próximos 7 Dias')
    plt.xlabel('Data')
    plt.ylabel('Close Price (USD)')
    plt.xticks(rotation=45)
    plt.grid()
    plt.legend()  # Adicionar legenda

       # Salvar gráfico em memória (em vez de salvar no disco)
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()

    # Converter a imagem para base64
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    
    return img_base64