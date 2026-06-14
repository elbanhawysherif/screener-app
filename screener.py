import requests
import os
from bs4 import BeautifulSoup

# -----------------------------
# 1. GET S&P 500 UNIVERSE
# -----------------------------
def get_sp500_symbols():

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    r = requests.get(url, timeout=15)

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})

    symbols = []

    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if cols:
            symbol = cols[0].text.strip()

            # Fix for Finnhub formatting (BRK.B → BRK-B)
            symbol = symbol.replace(".", "-")

            symbols.append(symbol)

    return symbols


# -----------------------------
# 2. MAIN SCREENER
# -----------------------------
def run_screener():

    key = os.environ.get("FINNHUB_API_KEY")

    if not key:
        return {"error": "Missing FINNHUB_API_KEY"}

    symbols = get_sp500_symbols()

    results = []

    # IMPORTANT: limit for API + Render stability
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
            high = data.get("h")
            low = data.get("l")

            if not price or not prev:
                continue

            # -----------------------------
            # METRICS
            # -----------------------------
            change_pct = ((price - prev) / prev) * 100
            range_pct = ((high - low) / price) * 100 if high and low else 0

            # -----------------------------
            # SCORING MODEL (PRO VERSION)
            # -----------------------------
            score = (
                abs(change_pct) * 2.0 +   # momentum weight
                range_pct * 1.0           # volatility weight
            )

            results.append({
                "symbol": symbol,
                "price": round(price, 2),
                "change_pct": round(change_pct, 2),
                "range_pct": round(range_pct, 2),
                "score": round(score, 2)
            })

        except Exception:
            continue

    # -----------------------------
    # SORT BY SCORE (HEDGE FUND STYLE)
    # -----------------------------
    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "count": len(results),
        "results": results[:20]   # top 20 signals
    }
