from flask import Flask, jsonify, render_template
from database import load_crypto_data_from_db  # Função que carrega os dados do banco
from prediction import preprocess_and_predict, salvar_predicao # Função que faz a previsão
from plot import generate_close_price_plot
from data_ingestion import fetch_and_store_data
from datetime import datetime



app = Flask(__name__)


# Endpoint para servir a página HTML
@app.route('/')
def index():
    return render_template('index.html')  # Renderiza a página HTML

# Endpoint para realizar a previsão
@app.route('/predict', methods=['POST'])
def predict():
    # Chamar a função de atualização de dados
    fetch_and_store_data()

    # Obtendo a data de hoje
    user_date = datetime.today().date()
    
    # Carregar dados do banco de dados
    btc = load_crypto_data_from_db()

    # Realizar o tratamento e a previsão
    predictions= preprocess_and_predict(btc, user_date)
    

    salvar_predicao(predictions)

     # Gera o gráfico em base64
    img_data = generate_close_price_plot()

    # Retorna a previsão e o gráfico para o frontend
    return jsonify({
        'predictions': predictions.tolist(),
        'img_data': img_data  # Gráfico codificado em base64
    })

  

if __name__ == '__main__':
    app.run(debug=True)
