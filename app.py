from flask import Flask, jsonify
from screener import run_screener

app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

@app.route("/run")
def run():
    data = run_screener()

    return jsonify({
        "count": len(data),
        "results": data
    })
