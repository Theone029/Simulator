import json
WEIGHTS_FILE = "config/scoring_weights.json"
def get_weight(source):
    try:
        with open(WEIGHTS_FILE) as f:
            return json.load(f).get(source, 1.0)
    except: return 1.0

from utils.event_logger import log_event
from utils.event_logger import log_event
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import json
import time
from recursive_score import RecursiveScore

score_engine = RecursiveScore()


def inject_signal(signal):
    score = score_engine.compute(
        delta_accuracy=signal["delta_accuracy"],
        delta_entropy=signal["delta_entropy"],
        delta_synergy=0.0,
        cost=signal["token_cost"] + signal["time_cost"]
    )
    if score < 0.1:
        return False

    print(f"[⚙️] High score! Spawning agent for signal: {signal}")
    log_event("agent_spawn", signal)
    log_event("agent_spawn", signal)
    with open("logs/used_signals.jsonl", "a") as f:
        f.write(json.dumps(signal) + "\n")
    with open("logs/module_impact.jsonl", "a") as f:
        f.write(json.dumps({
            "time": time.time(),
            "action": "agent_spawn",
            "signal": signal,
            "score": round(score, 4)
        }) + "\n")

    # Trigger symbolic module if score > 0.5
    if score > 0.5:
        print("[] Symbolic Compressor Activated.")
    log_event("symbolic_compressor", {"reason": "high_score_trigger"})
    with open("logs/module_impact.jsonl", "a") as f:
        f.write(json.dumps({
            "time": time.time(),
            "action": "symbolic_compressor",
            "reason": "high_score_trigger"
        }) + "\n")
    return True


def run():
    try:
        with open("logs/accepted_signals.jsonl", "r") as f:
            accepted = [json.loads(line) for line in f if line.strip()]
    except FileNotFoundError:
        accepted = []

    try:
        with open("logs/used_signals.jsonl", "r") as f:
            used = [json.loads(line) for line in f if line.strip()]
    except FileNotFoundError:
        used = []

    used_set = set(json.dumps(u, sort_keys=True) for u in used)
    for signal in accepted:
        key = json.dumps(signal, sort_keys=True)
        if key not in used_set:
            injected = inject_signal(signal)
            if injected:
                return
    print("No unused signals.")


if __name__ == "__main__":
    run()
