import requests
import os

def run_screener():

    API_KEY = os.environ.get("FMP_API_KEY")

    symbols = "AAPL,MSFT,NVDA,AMZN,META,TSLA,GOOGL,AMD,INTC,NFLX"

    url = f"https://financialmodelingprep.com/api/v3/quote/{symbols}?apikey={API_KEY}"

    try:
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
                    "price": price,
                    "change": stock.get("change"),
                    "changePercent": stock.get("changesPercentage")
                })

        # sort low → high
        results = sorted(results, key=lambda x: x["price"])

        return {
            "count": len(results),
            "results": results
        }

    except Exception as e:
        return {
            "count": 0,
            "results": [],
            "error": str(e)
        }
