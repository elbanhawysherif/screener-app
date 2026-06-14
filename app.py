from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "APP_RUNNING"

@app.route("/run")
def run():
    return jsonify({
        "status": "ok",
        "count": 1,
        "results": [
            {"symbol": "TEST", "price": 123}
        ]
    })
