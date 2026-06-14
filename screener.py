import os

def run_screener():
    return {
        "status": "OK - screener is running",
        "env_check": bool(os.environ.get("FINNHUB_API_KEY"))
    }
