import requests
import os

# -----------------------------
# SIGNAL CLASSIFIER
# -----------------------------
def classify_stock(change_pct, range_pct, price, prev_close):

    trend = "UP" if price > prev_close else "DOWN"
    abs_change = abs(change_pct)

    if abs_change > 2 and range_pct > 2 and trend == "UP":
        return "🚀 STRONG BREAKOUT"

    if abs_change > 1.5 and trend == "UP":
        return "🔥 MOMENTUM UP"

    if abs_change > 1.5 and trend == "DOWN":
        return "⚠️ STRONG SELL PRESSURE"

    if abs_change < 0.5:
        return "💤 NOISE"

    return "📊 NORMAL"


# -----------------------------
# MAIN SCREENER
# -----------------------------
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

            signal = classify_stock(change_pct, range_pct, price, prev)

            # FILTER OUT NOISE
            if signal == "💤 NOISE":
                continue

            score = abs(change_pct) * 2 + range_pct * 1.2

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

    # sort by strongest signals
    results.sort(key=lambda x: x["score"], reverse=True)

    # -----------------------------
    # FORMATTED OUTPUT (ONE STOCK PER LINE)
    # -----------------------------
    formatted_lines = []

    for r in results[:10]:

        line = (
            f"{r['symbol']} | "
            f"${r['price']} | "
            f"{r['change_pct']}% | "
            f"{r['signal']} | "
            f"Score: {r['score']}"
        )

        formatted_lines.append(line)

    return {
        "count": len(results),
        "results": results[:10],
        "formatted": "\n".join(formatted_lines)
    }
