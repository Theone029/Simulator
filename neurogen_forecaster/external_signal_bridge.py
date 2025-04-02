import numpy as np
import time
import json
from datetime import datetime

class ExternalSignalBridge:
    """
    Filters and scores external signals based on predicted return vs. ingestion cost.
    Only signals with positive ROI are accepted.
    """
    def __init__(self, entropy_tracker, threshold=1.0, max_signals=5):
        self.entropy_tracker = entropy_tracker
        self.threshold = threshold
        self.max_signals = max_signals
        self.accepted_signals = []

    def fetch_signals(self):
        """
        Simulate fetching candidate signals. Replace with real API calls.
        Returns a list of dicts: [{name: str, data: np.array}]
        """
        return [
            {"name": "mock_trend_1", "data": np.random.randn(10)},
            {"name": "mock_trend_2", "data": np.random.randn(10) * 0.2},
            {"name": "mock_trend_3", "data": np.sin(np.linspace(0, 2*np.pi, 10))},
        ]

    def compute_signal_value(self, signal):
        """
        Estimate signal value using entropy delta and accuracy gain over cost.
        """
        start = time.time()

        baseline_entropy = self.entropy_tracker.current_entropy
        new_entropy = self.entropy_tracker.simulate_with(signal["data"])
        delta_entropy = baseline_entropy - new_entropy

        accuracy_gain = delta_entropy
        ingestion_cost = 0.01 + (len(signal["data"]) * 0.001)
        time_cost = time.time() - start
        total_cost = ingestion_cost + time_cost

        value_score = (accuracy_gain + delta_entropy) / (total_cost + 1e-6)
        return value_score, delta_entropy, total_cost

    def evaluate_signals(self):
        """
        Evaluate all candidates and accept only the highest ROI signals.
        """
        candidates = self.fetch_signals()
        results = []

        for signal in candidates:
            score, delta_entropy, cost = self.compute_signal_value(signal)
            results.append({
                "signal": signal,
                "score": score,
                "delta_entropy": delta_entropy,
                "cost": cost
            })

        top = sorted(results, key=lambda r: r["score"], reverse=True)
        accepted = [r for r in top if r["score"] >= self.threshold][:self.max_signals]

        self.accepted_signals = accepted
        self.log_results(accepted)

        return [r["signal"] for r in accepted]

    def log_results(self, accepted_signals):
        """
        Log accepted signals and their value scores to usage_log.jsonl
        """
        with open("logs/usage_log.jsonl", "a") as f:
            for r in accepted_signals:
                log_entry = {
                    "module": "external_signal_bridge",
                    "time": datetime.utcnow().isoformat(),
                    "signal_name": r["signal"]["name"],
                    "score": r["score"],
                    "delta_entropy": r["delta_entropy"],
                    "cost": r["cost"]
                }
                f.write(json.dumps(log_entry) + "\n")
