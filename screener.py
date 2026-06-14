import requests

def get_universe(key):

    url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={key}"
    r = requests.get(url, timeout=20)

    if r.status_code != 200:
        return []

    data = r.json()

    cleaned = []

    for item in data:

        symbol = item.get("symbol")

        if not symbol:
            continue

        # -----------------------------
        # BASIC SYMBOL CLEANING
        # -----------------------------
        if len(symbol) > 6:
            continue

        if "." in symbol:
            continue

        if "-" in symbol:
            continue

        # remove obvious garbage
        if symbol.isdigit():
            continue

        cleaned.append(symbol)

    # limit initial universe
    cleaned = cleaned[:300]

    return cleaned
