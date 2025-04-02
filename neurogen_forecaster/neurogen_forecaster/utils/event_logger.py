#!/usr/bin/env python3
import os, json

LOG_PATH = "logs/system_events.jsonl"
os.makedirs("logs", exist_ok=True)
if not os.path.exists(LOG_PATH):
    open(LOG_PATH, "w").close()

def log_event(event_type, data):
    entry = {"type": event_type, "data": data}
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
