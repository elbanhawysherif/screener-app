import requests
import os

def run_screener():

    API_KEY = os.environ.get("FMP_API_KEY")

    symbols = [
        "AAPL", "MSFT", "NVDA", "AMZN", "META",
        "TSLA", "GOOGL", "AMD", "INTC", "NFLX"
    ]

    results = []

    for symbol in symbols:

        url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={API_KEY}"

        try:
            r = requests.get(url, timeout=10)
            data = r.json()

            if isinstance(data, list) and len(data) > 0:

                stock = data[0]

                price = stock.get("price")

                if price is None:
                    continue

                results.append({
                    "symbol": stock.get("symbol"),
                    "price": price,
                    "change": stock.get("change"),
                    "changePercent": stock.get("changesPercentage"),
                    "volume": stock.get("volume")
                })

        except Exception:
            continue

    # Sort by price (low → high)
    results = sorted(results, key=lambda x: x["price"])

    return {
        "count": len(results),
        "results": results
    }
