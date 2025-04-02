# -*- coding: utf-8 -*-
from utils.event_logger import log_event
#!/usr/bin/env python3
import json, time, os

SCORES = {}
LOG = "logs/module_impact.jsonl"
OUT = "logs/signal_feedback_scores.json"

def score(signal):
    acc, ent, cost = signal["delta_accuracy"], signal["delta_entropy"], signal["token_cost"] + signal["time_cost"]
    return (acc + ent) / (cost + 1e-5)

def update_scores():
    if not os.path.exists(LOG): return
    with open(LOG) as f:
        for line in f:
            try:
                data = json.loads(line)
                if "signal" not in data: continue
                source = data["signal"].get("source", "unknown")
                SCORES.setdefault(source, []).append(score(data["signal"]))
            except: continue
    avg = {k: round(sum(v)/len(v), 4) for k, v in SCORES.items()}
    with open(OUT, "w") as out:
        json.dump(avg, out, indent=2)
        log_event("feedback_score_update", avg)
    print("[✓] Signal feedback scores updated:", avg)

if __name__ == "__main__":
    while True:
        update_scores()
        time.sleep(60)
