from flask import Flask, jsonify, Response
from screener import run_screener

app = Flask(__name__)


@app.route("/")
def home():
    return "PRO SIGNAL ENGINE RUNNING"


@app.route("/refresh")
def refresh():
    """
    Runs full screener on demand (slow endpoint)
    """
    data = run_screener()
    return jsonify(data)


@app.route("/run-json")
def run_json():
    """
    Always recomputes (safe fallback, no cache complexity)
    """
    return jsonify(run_screener())


@app.route("/run-html")
def run_html():
    """
    Always recomputes and returns HTML (simple + stable)
    """
    data = run_screener()
    return Response(data["pretty_html"], mimetype="text/html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
