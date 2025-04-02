#!/usr/bin/env python3
import json, os, time
from collections import defaultdict

IMPACT_LOG = "logs/module_impact.jsonl"
FEEDBACK_LOG = "logs/signal_feedback_scores.json"
WEIGHTS_OUT = "config/scoring_weights.json"

def compute_weights():
    impact_data = defaultdict(list)
    if not os.path.exists(IMPACT_LOG): return

    with open(IMPACT_LOG) as f:
        for line in f:
            try:
                data = json.loads(line)
                if "signal" not in data: continue
                src = data["signal"].get("source", "unknown")
                score = (data["signal"]["delta_accuracy"] + data["signal"]["delta_entropy"]) /                         (data["signal"]["token_cost"] + data["signal"]["time_cost"] + 1e-6)
                impact_data[src].append(score)
            except: continue

    weights = {}
    for src, scores in impact_data.items():
        avg = sum(scores) / len(scores)
        weights[src] = round(avg, 4)

    with open(WEIGHTS_OUT, "w") as out:
        json.dump(weights, out, indent=2)
    print("[⚖️] Scoring weights updated:", weights)

if __name__ == "__main__":
    while True:
        compute_weights()
        time.sleep(300)  # every 5 min
