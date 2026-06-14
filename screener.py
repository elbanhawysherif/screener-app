import requests
import os

def run_screener():

    API_KEY = os.environ.get("FMP_API_KEY")

    if not API_KEY:
        return [{"error": "Missing API key in environment variables"}]

    url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY}"

    try:
        r = requests.get(url, timeout=30)

        # If API fails, show raw response instead of crashing
        try:
            data = r.json()
        except Exception:
            return [{
                "error": "Invalid JSON response",
                "status_code": r.status_code,
                "raw_text": r.text[:300]
            }]

        # If API returns error message
        if isinstance(data, dict):
            return [{
                "error": "API returned error",
                "response": data
            }]

        results = []

        for stock in data[:10]:
            results.append({
                "symbol": stock.get("symbol"),
                "name": stock.get("name"),
                "price": stock.get("price")
            })

        return results

    except Exception as e:
        return [{
            "error": str(e)
        }]
