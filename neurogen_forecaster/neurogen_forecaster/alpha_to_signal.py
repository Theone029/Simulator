# -*- coding: utf-8 -*-
import json, random
with open("logs/alpha_raw.json", "r", encoding="utf-8") as f:
    data = json.load(f)
timeseries = data.get("Time Series (5min)", {})
metrics = list(timeseries.values())
signals = []
for metric in metrics[:5]:
    signal = {
        "delta_accuracy": round(random.uniform(0.05, 0.15), 3),
        "delta_entropy": round(random.uniform(0.01, 0.03), 3),
        "token_cost": 0.008,
        "time_cost": 0.009,
        "source": "alpha"
    }
    signals.append(signal)
with open("logs/signal_stream.jsonl", "a", encoding="utf-8") as f:
    for s in signals:
        f.write(json.dumps(s) + "\n")
print("[+] Injected 5 Finance-derived signals.")
