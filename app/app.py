from flask import Flask, jsonify, render_template
from database import load_crypto_data_from_db  # Função que carrega os dados do banco
from prediction import preprocess_and_predict  # Função que faz a previsão

app = Flask(__name__)

# Endpoint para servir a página HTML
@app.route('/')
def index():
    return render_template('index.html')  # Renderiza a página HTML

# Endpoint para realizar a previsão
@app.route('/predict', methods=['POST'])
def predict():
    # Carregar dados do banco de dados
    btc = load_crypto_data_from_db()

    # Realizar o tratamento e a previsão
    predictions= preprocess_and_predict(btc)

    # Retornar os resultados como uma resposta JSON
    return jsonify({
        'predictions': predictions.tolist(),
    })

if __name__ == '__main__':
    app.run(debug=True)
