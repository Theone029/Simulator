from utils.event_logger import log_event
# -*- coding: utf-8 -*-
import time, json
# MOCK MODE: Injects synthetic improvement signal
fallback_signal = {
    "delta_accuracy": 0.07,
    "delta_entropy": 0.05,
    "token_cost": 0.01,
    "time_cost": 0.01
}
with open("logs/signal_stream.jsonl", "a") as f:
    f.write(json.dumps(fallback_signal) + "\n")
with open("logs/system_events.jsonl", "a") as f:
    f.write(json.dumps({"time": time.time(), "event": "llm_fallback_injected"}) + "\n")
