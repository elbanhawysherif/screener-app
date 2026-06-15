from flask import Flask, jsonify, Response
import json
import os
from screener import run_screener
print("🔥 APP IS STARTING")
app = Flask(__name__)

CACHE = {
    "data": None
}

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.route("/")
def home():
    return "PRO SIGNAL ENGINE RUNNING"


# -----------------------------
# FULL REFRESH (SLOW - COMPUTES DATA)
# -----------------------------
@app.route("/refresh")
def refresh():

    data = run_screener()

    try:
        tmp_file = CACHE_FILE + ".tmp"

        with open(tmp_file, "w") as f:
            json.dump(data, f)

        # atomic replace (prevents partial reads)
        os.replace(tmp_file, CACHE_FILE)

        return jsonify({
            "status": "refreshed",
            "count": data.get("count", 0)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# FAST HTML VIEW (USES CACHE ONLY)
# -----------------------------
@app.route("/run-html")
def run_html():

    try:
        if not os.path.exists(CACHE_FILE):
            return "Cache not ready. Run /refresh first.", 200

        with open(CACHE_FILE, "r") as f:
            data = json.load(f)

        html = data.get("pretty_html", "")

        if not html:
            return "Cache empty. Run /refresh again.", 200

        return Response(html, mimetype="text/html")

    except Exception as e:
        return f"Cache error: {str(e)}", 500


# -----------------------------
# FAST JSON VIEW (USES CACHE ONLY)
# -----------------------------
@app.route("/run")
def run_json():

    if not os.path.exists(CACHE_FILE):
        return jsonify({"error": "Cache not ready. Run /refresh first"}), 500

    try:
        with open(CACHE_FILE, "r") as f:
            return jsonify(json.load(f))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# DEBUG ROUTE (VERY USEFUL)
# -----------------------------
@app.route("/debug")
def debug():
    return {
        "routes": [str(rule) for rule in app.url_map.iter_rules()]
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
