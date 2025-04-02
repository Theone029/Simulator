# -*- coding: utf-8 -*-
import json, math, time

def score(post):
    points = post.get("score", 0)
    comments = post.get("comments", 0)
    recency = max(1, time.time() - post.get("time", time.time()))
    entropy = math.log1p(points + comments) / math.log1p(recency)
    return {
        "delta_accuracy": round(min(entropy, 0.15), 3),
        "delta_entropy": round(entropy, 3),
        "token_cost": 0.01,
        "time_cost": 0.01
    }

with open("logs/hn_raw.json") as f:
    posts = json.load(f)

signals = [score(p) for p in posts]
with open("logs/signal_stream.jsonl", "a") as f:
    for s in signals:
        f.write(json.dumps(s) + "\n")

print(f"[+] Injected {len(signals)} HN-derived signals.")
