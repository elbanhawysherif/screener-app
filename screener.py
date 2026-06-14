import requests
import os

def classify_stock(change_pct, range_pct):

    abs_change = abs(change_pct)

    if abs_change > 2 and range_pct > 2:
        return "🚀 BREAKOUT"

    elif abs_change > 1.5:
        return "🔥 MOMENTUM"

    elif abs_change > 0.8 and change_pct < 0:
        return "⚠️ REVERSION"

    elif abs_change < 0.5:
        return "💤 NOISE"

    return "📊 NORMAL"


def run_screener():

    key = os.environ.get("FINNHUB_API_KEY")

    symbols = [
        "TSLA","LLY","AMZN","JPM","AAPL",
        "MRK","ABBV","GOOGL","V","AVGO",
        "META","MSFT","NVDA","HD","PEP"
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

            signal = classify_stock(change_pct, range_pct)

            # FILTER OUT NOISE
            if signal == "💤 NOISE":
                continue

            score = (
                abs(change_pct) * 2 +
                range_pct * 1.2
            )

            results.append({
                "symbol": s,
                "price": round(price, 2),
                "change_pct": round(change_pct, 2),
                "range_pct": round(range_pct, 2),
                "score": round(score, 2),
                "signal": signal
            })

        except Exception:
            continue

    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "count": len(results),
        "results": results[:10]
    }
