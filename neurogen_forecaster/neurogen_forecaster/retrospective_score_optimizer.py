import json
import os
import time
from recursive_score import RecursiveScore

class RetrospectiveScoreOptimizer:
    def __init__(self, scorer: RecursiveScore, log_path="logs/score_log.jsonl", window=20):
        self.log_path = log_path
        self.window = window
        self.scorer = scorer

    def load_recent_scores(self):
        if not os.path.exists(self.log_path):
            return []
        with open(self.log_path, "r") as f:
            lines = f.readlines()[-self.window:]
            return [json.loads(line) for line in lines if line.strip()]

    def compute_drift(self, entries):
        drift = {"accuracy": 0.0, "entropy": 0.0, "synergy": 0.0}
        total_score = sum(abs(e["score"]) for e in entries) + 1e-6
        for e in entries:
            drift["accuracy"] += e["accuracy"] * abs(e["score"])
            drift["entropy"] += e["entropy"] * abs(e["score"])
            drift["synergy"] += e["synergy"] * abs(e["score"])
        for k in drift:
            drift[k] /= total_score
        return drift

    def normalize_weights(self, weights):
        total = sum(weights.values()) + 1e-6
        return {k: v / total for k, v in weights.items()}

    def run_once(self):
        entries = self.load_recent_scores()
        if not entries:
            return
        new_weights = self.compute_drift(entries)
        norm_weights = self.normalize_weights(new_weights)
        self.scorer.update_weights(norm_weights)

    def run_loop(self, interval=60):
        while True:
            self.run_once()
            time.sleep(interval)

# To run continuously:
# from recursive_score import RecursiveScore
# rso = RetrospectiveScoreOptimizer(RecursiveScore())
# rso.run_loop(interval=120)

    def print_drift(self):
        try:
            with open("logs/score_log.jsonl", "r") as f:
                entries = [json.loads(line) for line in f if line.strip()][-10:]
            print("SCORE WEIGHT DRIFT (latest 10)")
            print("-" * 55)
            for e in entries:
                w = e['weights']
                print(f"{e['time'][-8:]} | Acc: {w.get('accuracy', 0):.2f} | Ent: {w.get('entropy', 0):.2f} | Syn: {w.get('synergy', 0):.2f} | Score: {e['score']:.4f}")
        except Exception as ex:
            print("[DRIFT] Failed to print drift:", ex)

    def run_once(self):
        entries = self.load_recent_scores()
        if not entries:
            return
        new_weights = self.compute_drift(entries)
        norm_weights = self.normalize_weights(new_weights)
        self.scorer.update_weights(norm_weights)
        self.print_drift()
