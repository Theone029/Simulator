from utils.event_logger import log_event
# -*- coding: utf-8 -*-
import json, os
from collections import defaultdict
from datetime import datetime

def load_jsonl(path):
    if not os.path.exists(path): return []
    with open(path, "r") as f:
        return [json.loads(line) for line in f if line.strip()]

def summarize_scores(score_logs):
    if not score_logs: return "No scoring logs."
    total, count = 0, 0
    for entry in score_logs:
        total += entry.get("score", 0)
        count += 1
    avg = total / count if count else 0
    return f"Avg Score: {avg:.4f} across {count} entries"

def summarize_modules(orch_logs):
    spawns, kills = defaultdict(int), defaultdict(int)
    for log in orch_logs:
        event = log.get("event", "")
        if "SPAWNED" in event:
            name = event.split(":")[-1].strip()
            spawns[name] += 1
        elif "TERMINATED" in event:
            name = event.split(":")[0].strip()
            kills[name] += 1
    return spawns, kills

def summarize_configs(config_logs):
    accepted = [e for e in config_logs if e.get("accepted", True)]
    rejected = [e for e in config_logs if not e.get("accepted", True)]
    return len(accepted), len(rejected)

if __name__ == "__main__":
    scores = load_jsonl("logs/score_log.jsonl")
    orch = load_jsonl("logs/orchestrator_log.jsonl")
    configs = load_jsonl("logs/config_history.jsonl") if os.path.exists("logs/config_history.jsonl") else []

    print("COGNITION AUDIT SUMMARY")
log_event("cognition_audit_summary", {"avg_score": avg_score, "accepted": accepted, "rejected": rejected})
    print("-" * 50)
    print("SCORES:", summarize_scores(scores))
    spawns, kills = summarize_modules(orch)
    print("\nMODULES SPAWNED:")
    for k, v in spawns.items():
        print(f"  {k}: {v}x")

    print("\nMODULES TERMINATED:")
    for k, v in kills.items():
        print(f"  {k}: {v}x")

    accepted, rejected = summarize_configs(configs)
    print(f"\nCONFIG MUTATIONS: {accepted} accepted | {rejected} rejected")

    print("\nNOTE: LLM usage + signal ingestion tracking will be auto-included once their logs exist.")
