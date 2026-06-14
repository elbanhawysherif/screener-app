import requests
import os

def run_screener():

    API_KEY = os.environ.get("FMP_API_KEY")

    symbols = ["AAPL", "MSFT", "NVDA", "AMZN", "META"]

    results = []

    for symbol in symbols:

        url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={API_KEY}"

        try:
            r = requests.get(url, timeout=10)
            data = r.json()

            if isinstance(data, list) and len(data) > 0:

                stock = data[0]

                results.append({
                    "symbol": stock.get("symbol"),
                    "price": stock.get("price")
                })

        except Exception:
            continue

    return results
