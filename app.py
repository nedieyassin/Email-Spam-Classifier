import sqlite3

from flask import Flask, render_template, request, jsonify, g

from database.controller import save_email, init_db, get_email
from utils import model_predict

app = Flask(__name__)

DATABASE = 'email-spam-classifier.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        init_db(db.cursor())
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/history")
def history():
    con = get_db()
    emails = get_email(con)

    # print(emails)
    return render_template("history.html", emails=emails)


@app.route('/predict', methods=['POST'])
def predict():
    con = get_db()
    #
    email = request.form.get('content')
    prediction = model_predict(email)
    #
    save_email(con, email, prediction)
    return render_template("index.html", prediction=prediction, email=email)


# Create an API endpoint
@app.route('/api/predict', methods=['POST'])
def predict_api():
    data = request.get_json(force=True)  # Get data posted as a json
    email = data['content']

    prediction = model_predict(email)
    return jsonify({'prediction': prediction, 'email': email})  # Return prediction


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
