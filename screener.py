import requests
import os

def run_screener():

    API_KEY = os.environ.get("FMP_API_KEY")

    url = f"https://financialmodelingprep.com/api/v3/quote/AAPL?apikey={API_KEY}"

    try:
        r = requests.get(url, timeout=15)

        return [{
            "status_code": r.status_code,
            "response_text": r.text[:1000]
        }]

    except Exception as e:
        return [{
            "error": str(e)
        }]
