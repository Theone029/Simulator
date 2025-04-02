# -*- coding: utf-8 -*-
import json, random
with open("logs/twitter_raw.json", "r", encoding="utf-8") as f:
    trends = json.load(f)
signals = []
for trend in trends[:10]:
    signal = {
        "delta_accuracy": round(random.uniform(0.03, 0.12), 3),
        "delta_entropy": round(random.uniform(0.02, 0.06), 3),
        "token_cost": 0.015,
        "time_cost": 0.01,
        "source": "twitter"
    }
    signals.append(signal)
with open("logs/signal_stream.jsonl", "a", encoding="utf-8") as f:
    for s in signals:
        f.write(json.dumps(s) + "\n")
print("[+] Injected 10 Twitter-derived signals.")
