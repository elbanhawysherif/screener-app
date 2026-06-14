import requests
import os
import pandas as pd

def get_sp500_symbols():

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    tables = pd.read_html(url)

    df = tables[0]

    # Column: Symbol
    return df["Symbol"].tolist()


def run_screener():

    key = os.environ.get("FINNHUB_API_KEY")

    symbols = get_sp500_symbols()

    results = []

    # limit for performance (IMPORTANT for Render + free API)
    symbols = symbols[:100]

    for symbol in symbols:

        try:
            url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={key}"
            r = requests.get(url, timeout=10)

            if r.status_code != 200:
                continue

            data = r.json()

            price = data.get("c")
            prev = data.get("pc")

            if not price or not prev:
                continue

            change_pct = ((price - prev) / prev) * 100

            results.append({
                "symbol": symbol,
                "price": price,
                "change_pct": round(change_pct, 2),
                "high": data.get("h"),
                "low": data.get("l"),
            })

        except Exception:
            continue

    # ranking (momentum + volatility)
    for r in results:
        r["score"] = round(abs(r["change_pct"]) + (r["high"] - r["low"]) * 0.1, 2)

    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "count": len(results),
        "results": results[:20]   # top 20 only
    }
