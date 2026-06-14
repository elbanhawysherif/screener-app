def run_screener():

    from screener import get_sp500_symbols

    symbols = get_sp500_symbols()

    return {
        "count": len(symbols),
        "sample": symbols[:10]
    }
