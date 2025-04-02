import json
from datetime import datetime
def log_score(signal, score):
    entry = {"time": datetime.utcnow().isoformat(), "signal": signal, "score": score}
    with open("logs/signal_scores.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")
