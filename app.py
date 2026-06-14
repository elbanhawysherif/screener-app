from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "VERSION_999_WORKING"

@app.route("/run")
def run():

    return jsonify({
        "version": "999",
        "count": 1,
        "results": [{"symbol": "TEST", "price": 123}]
    })
