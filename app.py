from flask import Flask, jsonify
from screener import run_screener
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "API is running"

@app.route("/run")
def run():
    data = run_screener()
    return jsonify({
        "status": "success",
        "count": len(data),
        "results": data
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
