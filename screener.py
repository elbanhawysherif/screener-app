import requests
import os

API_KEY = os.environ.get("7wfaoju6F7rTcZymBjnZCZtJLHUDykmx")


import requests
import os

def run_screener():

    key = os.environ.get("FMP_API_KEY")

    url = f"https://financialmodelingprep.com/api/v3/quote/AAPL?apikey={key}"

    r = requests.get(url, timeout=20)

    return [{
        "status_code": r.status_code,
        "response": r.json()
    }]
