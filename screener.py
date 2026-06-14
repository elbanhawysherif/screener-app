import os

def run_screener():

    return {
        "env_check": True,
        "key_exists": os.environ.get("FMP_API_KEY") is not None,
        "key_preview": (os.environ.get("FMP_API_KEY") or "")[:4]
    }
