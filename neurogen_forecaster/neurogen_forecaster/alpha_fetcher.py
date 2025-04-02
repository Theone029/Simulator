import os
import json

FREQS_PATH = "logs/fetch_frequencies.json"
delay = 3600
if os.path.exists(FREQS_PATH):
    try:
        with open(FREQS_PATH) as f:
            delay = json.load(f).get('finance', 3600)
    except: pass

# -*- coding: utf-8 -*-
import os, json, requests

def fetch_alpha():
    key = os.getenv("ALPHA_VANTAGE_KEY")
    symbols = ["AAPL", "GOOG", "MSFT", "AMZN", "TSLA"]
    data = {}
    for symbol in symbols:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={key}"
        res = requests.get(url)
        if res.status_code == 200:
            data[symbol] = res.json()
    with open("logs/alpha_raw.json", "w") as f:
        json.dump(data, f)
    print("[✓] Retrieved financial metrics from Alpha Vantage.")

if __name__ == "__main__":
    fetch_alpha()

import time
time.sleep(delay)
