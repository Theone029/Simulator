#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os, time

SCORES_PATH = "logs/signal_feedback_scores.json"
FREQS_PATH = "logs/fetch_frequencies.json"
DEFAULT = { "reddit": 3600, "news": 3600, "finance": 3600, "twitter": 3600 }

def calc_delay(score): return int(3600 / max(score, 1))

def mutate_freqs():
    if not os.path.exists(SCORES_PATH): return
    with open(SCORES_PATH) as f: scores = json.load(f)
    freqs = {k: calc_delay(v) for k, v in scores.items()}
    for k in DEFAULT:
        if k not in freqs: freqs[k] = DEFAULT[k]
    with open(FREQS_PATH, "w") as out:
        json.dump(freqs, out, indent=2)
    print("[⚙️] Updated fetch frequencies:", freqs)

if __name__ == "__main__":
    while True:
        mutate_freqs()
        time.sleep(300)
