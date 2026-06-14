import requests
import os

# -----------------------------
# SIGNAL CLASSIFICATION (BASIC STRUCTURE)
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
# MOMENTUM SCORING (MULTI-DAY EDGE SIMULATION)
# -----------------------------
def momentum_score(change_pct, range_pct):

    score = abs(change_pct) * 2 + range_pct * 1.5

    if abs(change_pct) > 2:
        score += 2

    if abs(change_pct) < 0.5:
        score -= 2

    return round(score, 2)


# -----------------------------
# AI-STYLE EXPLANATION LAYER (RULE BASED)
# -----------------------------
def explain_signal(symbol, change_pct, range_pct, price, prev_close):

    trend = "bullish" if price > prev_close else "bearish"
    strength = abs(change_pct)

    parts = []

    if strength > 2:
        parts.append("strong price momentum with elevated volatility")
    elif strength > 1:
        parts.append("moderate directional momentum")
    else:
        parts.append("low directional pressure")

    if range_pct > 3:
        parts.append("high intraday volatility indicating active trading")
    elif range_pct > 1.5:
        parts.append("moderate volatility with stable flow")
    else:
        parts.append("low volatility environment")

    parts.append(f"overall {trend} bias vs previous close")

    return f"{symbol} shows " + ", ".join(parts) + "."


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
            score = momentum_score(change_pct, range_pct)

            if signal == "💤 NOISE":
                continue

            explanation = explain_signal(s, change_pct, range_pct, price, prev)

            results.append({
                "symbol": s,
                "price": round(price, 2),
                "change_pct": round(change_pct, 2),
                "range_pct": round(range_pct, 2),
                "score": score,
                "signal": signal,
                "explanation": explanation
            })

        except Exception:
            continue

    results.sort(key=lambda x: x["score"], reverse=True)

    # -----------------------------
    # FORMATTED OUTPUT (ONE STOCK PER LINE)
    # -----------------------------
    formatted_lines = []

    for r in results[:10]:

        formatted_lines.append(
            f"{r['symbol']} | ${r['price']} | {r['change_pct']}% | "
            f"{r['signal']} | Score: {r['score']}\n→ {r['explanation']}"
        )

    return {
        "count": len(results),
        "results": results[:10],
        "formatted": "\n\n".join(formatted_lines)
    }
