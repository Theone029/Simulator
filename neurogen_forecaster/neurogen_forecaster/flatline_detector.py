# -*- coding: utf-8 -*-
import json, time
from statistics import mean

def is_flatlined(scores):
    return len(scores) >= 5 and all(abs(scores[i] - scores[i-1]) < 0.001 for i in range(1, len(scores)))

try:
    with open("logs/module_impact.jsonl") as f:
        lines = [json.loads(x) for x in f if '"score"' in x]
        scores = [x["score"] for x in lines[-10:]]
    if is_flatlined(scores):
        with open("logs/system_events.jsonl", "a") as f:
            f.write(json.dumps({"time": time.time(), "event": "flatline_detected"}) + "\n")
except: pass
