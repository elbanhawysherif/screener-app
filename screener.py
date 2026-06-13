import pandas as pd
import numpy as np
import requests
import os


API_KEY = os.getenv("FMP_API_KEY", "7wfaoju6F7rTcZymBjnZCZtJLHUDykmx")


# =========================
# SAFE REQUEST
# =========================
def safe_get(url):
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None


# =========================
# SAFE FLOAT
# =========================
def f(x):
    try:
        return float(x)
    except:
        return None


# =========================
# UNIVERSE
# =========================
def get_universe():

    url = "https://financialmodelingprep.com/stable/company-screener"

    params = {
        "marketCapMoreThan": 2000000000,
        "volumeMoreThan": 200000,
        "isActivelyTrading": "true",
        "limit": 40,
        "apikey": API_KEY,
    }

    data = safe_get(url + "?" + requests.compat.urlencode(params))

    if not data or isinstance(data, dict):
        return pd.DataFrame()

    return pd.DataFrame(data)


# =========================
# SCORE MODEL
# =========================
def score_stock(m):

    score = 0

    roe = f(m.get("returnOnEquity"))
    debt = f(m.get("debtToEquity"))
    cr = f(m.get("currentRatio"))

    if roe is not None:
        if roe > 0.10:
            score += 3
        elif roe > 0.05:
            score += 2

    if debt is not None:
        if debt < 1:
            score += 3
        elif debt < 2:
            score += 2
        elif debt < 3:
            score += 1

    if cr is not None:
        if cr > 1.5:
            score += 2
        elif cr > 1:
            score += 1

    return score


# =========================
# LABELS
# =========================
def label(score):
    if score >= 7:
        return "A"
    elif score >= 4:
        return "B"
    return "C"


# =========================
# MAIN SCREENING FUNCTION
# =========================
def run_screener():

    df = get_universe()

    if df.empty:
        return []

    results = []

    for _, row in df.iterrows():

        symbol = row.get("symbol")
        if not symbol:
            continue

        price = f(row.get("price"))

        url = (
            f"https://financialmodelingprep.com/stable/key-metrics"
            f"?symbol={symbol}&period=annual&apikey={API_KEY}"
        )

        data = safe_get(url)

        if not data or isinstance(data, dict):
            continue

        m = data[0]

        results.append({
            "ticker": symbol,
            "company": row.get("companyName"),
            "price": price,
            "score": score_stock(m),
            "tier": label(score_stock(m)),
            "roe": m.get("returnOnEquity"),
            "debt_to_equity": m.get("debtToEquity"),
            "current_ratio": m.get("currentRatio"),
        })

    # =========================
    # CLEAN + SAFE SORT (NO PANDAS CRASH RISK)
    # =========================
    clean = []

    for r in results:
        try:
            price = float(r["price"])

            if np.isnan(price) or np.isinf(price):
                continue

            r["price"] = price
            clean.append(r)

        except:
            continue

    # SORT LOW → HIGH PRICE
    clean = sorted(clean, key=lambda x: x["price"])

    return clean
