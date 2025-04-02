#!/usr/bin/env python3
import json, openai, os, yaml
from utils.event_logger import log_event

CONFIG = "config/config.yaml"
HISTORY = "logs/config_history.jsonl"
SCORES = "logs/signal_feedback_scores.json"

def load_config(): return yaml.safe_load(open(CONFIG))
def save_config(cfg): yaml.safe_dump(cfg, open(CONFIG, "w"))

def propose_mutation(config, scores):
    prompt = f"Current config:\n{config}\n\nFeedback scores:\n{scores}\n\nSuggest a mutation to improve performance."
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()

def main():
    if not os.path.exists(SCORES): return
    config = load_config()
    scores = json.load(open(SCORES))
    proposed = propose_mutation(config, scores)
    log_event("llm_mutation_proposed", {"proposal": proposed})

    try:
        new_cfg = yaml.safe_load(proposed)
        save_config(new_cfg)
        with open(HISTORY, "a") as f: f.write(json.dumps({"proposal": proposed, "scores": scores}) + "\n")
        log_event("llm_mutation_applied", {"status": "success"})
    except Exception as e:
        log_event("llm_mutation_failed", {"error": str(e)})

if __name__ == "__main__":
    main()
