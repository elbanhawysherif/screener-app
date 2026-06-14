import requests
import os

def run_screener():

    API_KEY = os.environ.get("7wfaoju6F7rTcZymBjnZCZtJLHUDykmx")

    if not API_KEY:
        return [{"error": "Missing FMP_API_KEY in environment variables"}]

    # Step 1: small universe (reliable endpoint)
    symbols = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "TSLA", "GOOGL", "AMD", "INTC", "NFLX"]

    results = []

    for symbol in symbols:

        url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={API_KEY}"

        r = requests.get(url, timeout=15)

        try:
            data = r.json()

            # FMP returns a LIST
            if isinstance(data, list) and len(data) > 0:

                stock = data[0]

                results.append({
                    "symbol": stock.get("symbol"),
                    "price": stock.get("price"),
                    "change": stock.get("change"),
                    "changesPercent": stock.get("changesPercentage"),
                    "volume": stock.get("volume"),
                })

            else:
                results.append({
                    "symbol": symbol,
                    "error": "No data returned"
                })

        except Exception as e:
            results.append({
                "symbol": symbol,
                "error": str(e)
            })

    # Step 2: sort by price (low → high)
    results = sorted(
        [r for r in results if "price" in r and r["price"] is not None],
        key=lambda x: x["price"]
    )

    return {
        "count": len(results),
        "results": results
    }
