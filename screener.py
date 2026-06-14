import requests
import os

API_KEY = os.environ.get("FMP_API_KEY")


def run_screener():

    url = "https://financialmodelingprep.com/stable/company-screener"

    params = {
        "marketCapMoreThan": 1000000000,  # $1B+
        "volumeMoreThan": 100000,         # very loose
        "isActivelyTrading": "true",
        "limit": 20,
        "apikey": API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=30)

        if response.status_code != 200:
            return [{
                "error": f"HTTP {response.status_code}"
            }]

        data = response.json()

        if not data:
            return [{
                "error": "FMP returned no data"
            }]

        results = []

        for stock in data[:20]:

            results.append({
                "ticker": stock.get("symbol"),
                "company": stock.get("companyName"),
                "price": stock.get("price"),
                "marketCap": stock.get("marketCap"),
                "exchange": stock.get("exchangeShortName")
            })

        return results

    except Exception as e:
        return [{
            "error": str(e)
        }]
