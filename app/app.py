from flask import Flask, render_template
from prediction import predict
from db_connector import connect_to_db

app = Flask(__name__)

@app.route('/')
def index():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions")
    predictions = cursor.fetchall()
    cursor.close()
    conn.close()

    # Fazer nova previsão (opcional)
    new_prediction = predict()

    return render_template('index.html', predictions=predictions, new_prediction=new_prediction)

if __name__ == '__main__':
    app.run(debug=True)
