# -*- coding: utf-8 -*-
import json, os
from utils.event_logger import log_event

LOG = "logs/module_impact.jsonl"
OUT = "logs/signal_feedback_scores.json"
SCORES = {}

def score(signal):
    acc, ent = signal.get("delta_accuracy", 0), signal.get("delta_entropy", 0)
    cost = signal.get("token_cost", 0) + signal.get("time_cost", 0)
    return (acc + ent) / (cost + 1e-5)

def update_scores():
    if not os.path.exists(LOG): return
    with open(LOG) as f:
        for line in f:
            try:
                data = json.loads(line)
                if "signal" not in data: continue
                src = data["signal"].get("source", "unknown")
                SCORES.setdefault(src, []).append(score(data["signal"]))
            except: continue
    avg = {k: round(sum(v)/len(v), 4) for k, v in SCORES.items()}
    with open(OUT, "w") as out:
        json.dump(avg, out, indent=2)
    log_event("feedback_score_update", avg)
    print("[³Šâœ“] Signal feedback scores updated:", avg)

if __name__ == "__main__":
    update_scores()
