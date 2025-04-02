# -*- coding: utf-8 -*-
import json, random
with open("logs/reddit_raw.json", "r", encoding="utf-8") as f:
    posts = json.load(f)
signals = []
for post in posts[:10]:
    signal = {
        "delta_accuracy": round(min(post["score"] / 1000.0, 0.15), 3),
        "delta_entropy": 0.01,
        "token_cost": 0.01,
        "time_cost": 0.01,
        "source": "reddit",
        "title": post.get("title", "")
    }
    signals.append(signal)
with open("logs/signal_stream.jsonl", "a", encoding="utf-8") as f:
    for s in signals:
        f.write(json.dumps(s) + "\n")
print("[+] Injected 10 Reddit-derived signals.")
