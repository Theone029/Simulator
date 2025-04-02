import json
import os

def load_last_stable_config(log_path="logs/config_history.jsonl"):
    """
    Load the last stable config from the log file.
    """
    if not os.path.exists(log_path):
        return None
    last_config = None
    with open(log_path, "r") as f:
        for line in f:
            entry = json.loads(line)
            last_config = entry["final_config"]
    return last_config

def rollback_config(current_config, log_path="logs/config_history.jsonl"):
    """
    Rollback to the last stable config if performance criteria are not met.
    Placeholder: compare performance metrics to decide rollback.
    """
    last_config = load_last_stable_config(log_path)
    if last_config:
        print("Rolling back to last stable config.")
        return last_config
    print("No stable config found; keeping current config.")
    return current_config
