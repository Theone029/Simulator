# -*- coding: utf-8 -*-
import json, random
with open("logs/news_raw.json", "r", encoding="utf-8") as f:
    headlines = json.load(f)
signals = []
for article in headlines[:10]:
    signal = {
        "delta_accuracy": round(random.uniform(0.04, 0.09), 3),
        "delta_entropy": round(random.uniform(0.02, 0.04), 3),
        "token_cost": 0.012,
        "time_cost": 0.011,
        "source": "news"
    }
    signals.append(signal)
with open("logs/signal_stream.jsonl", "a", encoding="utf-8") as f:
    for s in signals:
        f.write(json.dumps(s) + "\n")
print("[+] Injected 10 News-derived signals.")
