import requests
import os

def run_screener():

    API_KEY = os.environ.get("FMP_API_KEY")

    symbols = "AAPL,MSFT"

    url = f"https://financialmodelingprep.com/api/v3/quote/{symbols}?apikey={API_KEY}"

    r = requests.get(url, timeout=15)
    data = r.json()

    results = []

    if isinstance(data, list):

        for stock in data:

            price = stock.get("price")

            if price is None:
                continue

            results.append({
                "symbol": stock.get("symbol"),
                "price": price
            })

    return results
