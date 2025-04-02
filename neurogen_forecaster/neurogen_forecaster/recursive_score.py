import numpy as np
import json
from datetime import datetime

class RecursiveScore:
    def __init__(self, weights=None):
        self.weights = weights or {
            "accuracy": 0.7,
            "entropy": 0.3,
            "synergy": 0.0
        }
        self.history = []

    def compute(self, delta_accuracy, delta_entropy, delta_synergy=0.0, cost=1.0):
        w = self.weights
        numerator = (
            w["accuracy"] * delta_accuracy +
            w["entropy"] * delta_entropy +
            w["synergy"] * delta_synergy
        )
        score = numerator / (cost + 1e-6)
        self.log_score(delta_accuracy, delta_entropy, delta_synergy, cost, score)
        return score

    def log_score(self, acc, ent, syn, cost, score):
        entry = {
            "time": datetime.utcnow().isoformat(),
            "accuracy": acc,
            "entropy": ent,
            "synergy": syn,
            "cost": cost,
            "score": score,
            "weights": self.weights.copy()
        }
        self.history.append(entry)
        with open("logs/score_log.jsonl", "a") as f:
            f.write(json.dumps(entry) + "\n")

    def update_weights(self, new_weights):
        for k in self.weights:
            if k in new_weights:
                self.weights[k] = new_weights[k]
        print("[RECURSIVE_SCORE] Updated weights:", self.weights)
