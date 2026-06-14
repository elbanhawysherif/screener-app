import requests
import os

def run_screener():

    key = os.environ.get("FINNHUB_API_KEY")

    symbols = [
        "AAPL",
        "MSFT",
        "NVDA",
        "AMZN",
        "META"
    ]

    results = []

    for symbol in symbols:

        url = (
            f"https://finnhub.io/api/v1/quote"
            f"?symbol={symbol}"
            f"&token={key}"
        )

        r = requests.get(url, timeout=15)

        if r.status_code != 200:
            continue

        data = r.json()

        results.append({
            "symbol": symbol,
            "price": data.get("c"),
            "high": data.get("h"),
            "low": data.get("l"),
            "open": data.get("o"),
            "previous_close": data.get("pc")
        })

    results.sort(key=lambda x: x["price"] or 0)

    return results
