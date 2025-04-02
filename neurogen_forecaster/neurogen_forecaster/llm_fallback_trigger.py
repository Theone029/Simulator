# -*- coding: utf-8 -*-
import json, time, os
from utils.event_logger import log_event

TRIGGER_PATH = "logs/signal_feedback_scores.json"
THRESHOLD = 3.0  # fallback if avg performance drops below this

def fallback_needed():
    if not os.path.exists(TRIGGER_PATH):
        return False
    with open(TRIGGER_PATH) as f:
        scores = json.load(f)
    avg_score = sum(scores.values()) / len(scores) if scores else 0
    return avg_score < THRESHOLD

def run_trigger_loop():
    while True:
        if fallback_needed():
            log_event("llm_fallback_triggered", {"avg_score": "low"})
            os.system("python3 neurogen_forecaster/llm_consultant.py")
        time.sleep(60)

if __name__ == "__main__":
    run_trigger_loop()
