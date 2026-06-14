from flask import Flask, jsonify, Response
import json
from screener import run_screener

app = Flask(__name__)

CACHE_FILE = "cache.json"


@app.route("/")
def home():
    return "PRO SIGNAL ENGINE RUNNING"


# optional manual refresh (still slow, but useful)
@app.route("/refresh")
def refresh():
    data = run_screener()
    return jsonify(data)


# FAST endpoint (this is what Zapier / browser should use)
@app.route("/run-html")
def run_html():

    try:
        with open(CACHE_FILE, "r") as f:
            data = json.load(f)

        return Response(data["pretty_html"], mimetype="text/html")

    except Exception:
        return "Cache not ready. Run /refresh first.", 500


@app.route("/run")
def run_json():

    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)

    except Exception:
        return jsonify({"error": "Cache not ready"})
