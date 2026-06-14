from flask import Flask, jsonify
import traceback

app = Flask(__name__)

@app.route("/run")
def run():

    try:
        from screener import get_sp500_symbols

        symbols = get_sp500_symbols()

        return jsonify({
            "count": len(symbols),
            "sample": symbols[:10]
        })

    except Exception as e:

        return jsonify({
            "error": str(e),
            "trace": traceback.format_exc()
        })
