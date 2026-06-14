from flask import Flask, jsonify
from screener import run_screener

app = Flask(__name__)

@app.route("/")
def home():
    return "PRO SIGNAL ENGINE RUNNING"

@app.route("/run")
def run():
    return jsonify(run_screener())
