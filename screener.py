import requests

API_KEY = "7wfaoju6F7rTcZymBjnZCZtJLHUDykmx"  # temporarily hardcoded for testing


def run_screener():

    url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY}"

    r = requests.get(url, timeout=30)

    data = r.json()

    # keep only first 10 to test
    results = []

    for stock in data[:10]:

        results.append({
            "symbol": stock.get("symbol"),
            "name": stock.get("name"),
            "price": stock.get("price"),
        })

    return results
