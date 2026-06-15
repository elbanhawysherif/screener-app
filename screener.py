import requests
import os
@app.route("/debug")
def debug():
    return {
        "routes": [str(rule) for rule in app.url_map.iter_rules()]
    }

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(BASE_DIR, "cache.json")

# -----------------------------
# SIGNAL CLASSIFICATION
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
# SCORE ENGINE
# -----------------------------
def momentum_score(change_pct, range_pct):

    score = abs(change_pct) * 2 + range_pct * 1.5

    if abs(change_pct) > 2:
        score += 2

    if abs(change_pct) < 0.5:
        score -= 2

    return round(score, 2)


# -----------------------------
# EXPLANATION ENGINE
# -----------------------------
def explain_signal(symbol, change_pct, range_pct, price, prev_close):

    trend = "bullish" if price > prev_close else "bearish"

    parts = []

    if abs(change_pct) > 2:
        parts.append("strong price momentum with elevated volatility")
    elif abs(change_pct) > 1:
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
# SMART UNIVERSE FILTER
# -----------------------------
def get_universe(key):
    url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={key}"
    r = requests.get(url, timeout=20)

    data = r.json()

    print("UNIVERSE SIZE:", len(data))

    return [x["symbol"] for x in data[:50]]
    # limit universe for performance
    return symbols[:100]


# -----------------------------
# LIQUIDITY CHECK
# -----------------------------
def is_liquid_stock(q):

    price = q.get("c")
    prev = q.get("pc")
    high = q.get("h")
    low = q.get("l")

    if price is None or prev is None:
        return False

    if price < 5 or price > 800:
        return False

    if prev == 0:
        return False

    if high is None or low is None:
        return False

    return True


# -----------------------------
# MAIN SCREENER
# -----------------------------
def run_screener():

    key = os.environ.get("FINNHUB_API_KEY")

    if not key:
        return {
            "count": 0,
            "results": [],
            "pretty_text": "",
            "pretty_html": ""
        }

    symbols = get_universe(key)

    results = []

    for s in symbols:

        try:
            url = f"https://finnhub.io/api/v1/quote?symbol={s}&token={key}"
            r = requests.get(url, timeout=10)

            if r.status_code != 200:
                continue

            q = r.json()

            if not is_liquid_stock(q):
                continue

            price = q["c"]
            prev = q["pc"]
            high = q["h"]
            low = q["l"]

            change_pct = ((price - prev) / prev) * 100
            range_pct = ((high - low) / price) * 100 if price else 0

            signal = classify_stock(change_pct, range_pct, price, prev)

            if signal == "💤 NOISE":
                continue

            score = momentum_score(change_pct, range_pct)
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

    # sort best signals first
    results.sort(key=lambda x: x["score"], reverse=True)

    top = results[:10]

    # -----------------------------
    # TEXT OUTPUT
    # -----------------------------
    text_blocks = []

    for r in top:
        text_blocks.append(
            f"{r['symbol']} | ${r['price']} | {r['change_pct']}% | "
            f"{r['signal']} | Score: {r['score']}\n→ {r['explanation']}"
        )

    pretty_text = "\n\n".join(text_blocks)

    # -----------------------------
    # HTML OUTPUT
    # -----------------------------
    html_blocks = []

    for r in top:
        html_blocks.append(f"""
        <p>
            <b>{r['symbol']}</b> | ${r['price']} | {r['change_pct']}% | {r['signal']} | Score: {r['score']}<br>
            → {r['explanation']}
        </p>
        <hr>
        """)

    pretty_html = "".join(html_blocks)

    return {
        "count": len(results),
        "results": top,
        "pretty_text": pretty_text,
        "pretty_html": pretty_html
    }
