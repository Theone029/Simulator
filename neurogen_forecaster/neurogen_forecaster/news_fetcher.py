import os
import json

FREQS_PATH = "logs/fetch_frequencies.json"
delay = 3600
if os.path.exists(FREQS_PATH):
    try:
        with open(FREQS_PATH) as f:
            delay = json.load(f).get('news', 3600)
    except: pass

# -*- coding: utf-8 -*-
import os, json, requests
key = os.getenv("NEWSAPI_KEY")
res = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={key}")
articles = res.json().get("articles", []) if res.status_code == 200 else []
titles = [{"title": a["title"], "source": a["source"]["name"]} for a in articles]
os.makedirs("logs", exist_ok=True)
with open("logs/news_raw.json", "w", encoding="utf-8") as f:
    json.dump(titles, f)
print(f"[✓] Parsed {len(titles)} news headlines from NewsAPI.")

import time
time.sleep(delay)
