#!/usr/bin/env python3
import json, time, os

STREAM = "logs/signal_stream.jsonl"
SCORES_FILE = "logs/signal_feedback_scores.json"
OUT = "logs/accepted_signals.jsonl"

def get_scores():
    try:
        with open(SCORES_FILE) as f:
            return json.load(f)
    except:
        return {}

def signal_score(signal, scores):
    base = (signal["delta_accuracy"] + signal["delta_entropy"]) / (signal["token_cost"] + signal["time_cost"] + 1e-5)
    src = signal.get("source", "unknown")
    weight = scores.get(src, 1)
    return base * weight

if __name__ == "__main__":
    scores = get_scores()
    used = set()
    while True:
        if not os.path.exists(STREAM):
            time.sleep(2)
            continue
        lines = []
        with open(STREAM) as f:
            for line in f:
                try:
                    data = json.loads(line)
                    lines.append(data)
                except:
                    continue
        lines = [s for s in lines if json.dumps(s) not in used]
        if lines:
            ranked = sorted(lines, key=lambda s: -signal_score(s, scores))
            top = ranked[0]
            used.add(json.dumps(top))
            with open(OUT, "a") as f:
                f.write(json.dumps(top) + "\n")
            print("[⚡] Accepted high-score-weighted signal:", top)
        time.sleep(3)
