import os
import json

FREQS_PATH = "logs/fetch_frequencies.json"
delay = 3600
if os.path.exists(FREQS_PATH):
    try:
        with open(FREQS_PATH) as f:
            delay = json.load(f).get('twitter', 3600)
    except: pass

# -*- coding: utf-8 -*-
import os, json, requests
bearer = os.getenv("TWITTER_BEARER")
headers = {"Authorization": f"Bearer {bearer}"}
res = requests.get("https://api.twitter.com/1.1/trends/place.json?id=1", headers=headers)
    print("[⚠️ debug] Twitter response:", res.text)
    print("[debug] Twitter response:", res.text)
if res.status_code == 200:
    data = res.json()
    if isinstance(data, list) and len(data) > 0 and "trends" in data[0]:
        trends = data[0]["trends"]
    else:
        trends = []
else:
    trends = []
os.makedirs("logs", exist_ok=True)
with open("logs/twitter_raw.json", "w", encoding="utf-8") as f:
    json.dump(trends, f)
print("[✓] Fetched Twitter trending topics.")

import time
time.sleep(delay)
