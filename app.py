from flask import Flask, jsonify
from screener import run_screener

app = Flask(__name__)

@app.route("/run", methods=["GET"])
def run():

    data = run_screener()

    return jsonify({
        "status": "success",
        "count": len(data),
        "data": data
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
