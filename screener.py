import requests
from bs4 import BeautifulSoup

def get_sp500_symbols():

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    r = requests.get(url, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find("table", {"id": "constituents"})

    symbols = []

    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if cols:
            symbols.append(cols[0].text.strip())

    return symbols
