import requests
import os

def run_screener():

    key = os.environ.get("FINNHUB_API_KEY")

    # stable S&P 100 subset (SAFE for production)
    symbols = [
        "AAPL", "MSFT", "NVDA", "AMZN", "META",
        "TSLA", "GOOGL", "AVGO", "JPM", "V",
        "UNH", "XOM", "LLY", "MA", "HD",
        "PG", "COST", "MRK", "ABBV", "PEP"
    ]

    results = []

    for s in symbols:

        try:
            url = f"https://finnhub.io/api/v1/quote?symbol={s}&token={key}"
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

            change_pct = ((price - prev) / prev) * 100
            range_pct = ((high - low) / price) * 100 if high and low else 0

            # simple hedge-fund scoring model
            score = abs(change_pct) * 2 + range_pct

            results.append({
                "symbol": s,
                "price": round(price, 2),
                "change_pct": round(change_pct, 2),
                "range_pct": round(range_pct, 2),
                "score": round(score, 2)
            })

        except Exception:
            continue

    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "count": len(results),
        "results": results[:10]
    }
