# -*- coding: utf-8 -*-
import json, os, time
from collections import defaultdict

IMPACT_LOG = "logs/module_impact.jsonl"
FREQS_OUT = "logs/fetch_frequencies.json"
SCORES = defaultdict(list)

def score(sig):
    acc, ent, cost = sig["delta_accuracy"], sig["delta_entropy"], sig["token_cost"] + sig["time_cost"]
    return (acc + ent) / (cost + 1e-5)

def optimize():
    if not os.path.exists(IMPACT_LOG): return
    with open(IMPACT_LOG) as f:
        for line in f:
            try:
                obj = json.loads(line)
                if obj.get("action") != "agent_spawn": continue
                src = obj["signal"].get("source", "unknown")
                SCORES[src].append(score(obj["signal"]))
            except: continue

    out = {}
    for src, vals in SCORES.items():
        avg = sum(vals)/len(vals)
        delay = round(max(60, 3600 / avg), 2)
        out[src] = delay

    with open(FREQS_OUT, "w") as f:
        json.dump(out, f, indent=2)
    print("[✓] Updated fetch frequencies:", out)

if __name__ == "__main__":
    while True:
        optimize()
        time.sleep(120)
