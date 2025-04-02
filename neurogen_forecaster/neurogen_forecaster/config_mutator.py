#!/usr/bin/env python3
import json, time, os

CONFIG_FILE = "config.json"
MUTATION_LOG = "logs/config_mutation.jsonl"
FEEDBACK_FILE = "logs/signal_feedback_scores.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # Default config structure with source weights for each feed
    return {"source_weights": {"reddit": 1.0, "twitter": 1.0, "news": 1.0, "alpha": 1.0}}

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def mutate_config(feedback, config):
    changed = {}
    for source, avg in feedback.items():
        if source in config.get("source_weights", {}):
            current = config["source_weights"][source]
            # Example mutation: adjust weight by 5% up or down depending on feedback
            if avg < 0.5:
                new = max(current * 0.95, 0.1)
            else:
                new = min(current * 1.05, 2.0)
            if abs(new - current) > 0.001:
                changed[source] = {"old": current, "new": new}
                config["source_weights"][source] = new
    return changed, config

def log_mutation(change):
    entry = {"time": time.time(), "mutation": change}
    with open(MUTATION_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    print("Config mutation logged:", entry)

if __name__ == "__main__":
    config = load_config()
    feedback = load_feedback()
    changed, new_config = mutate_config(feedback, config)
    if changed:
        save_config(new_config)
        log_mutation(changed)
    else:
        print("No significant config changes.")
