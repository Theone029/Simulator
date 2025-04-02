import json
import os
import numpy as np

class MetaOperator:
    """
    A recursive navigator that monitors system logs, entropy trends, and signal activity.
    Decides which modules to activate, suppress, or mutate based on goal vectors.
    """
    def __init__(self, config_log_path="logs/config_history.jsonl", signal_log_path="logs/usage_log.jsonl"):
        self.config_log_path = config_log_path
        self.signal_log_path = signal_log_path
        self.goal_vector = {
            "reduce_entropy": 0.1,
            "increase_synergy": 0.1,
            "domain_conquest": 1.0
        }

    def read_logs(self, path):
        if not os.path.exists(path):
            return []
        logs = []
        with open(path, "r") as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return logs

    def analyze_config_history(self):
        logs = self.read_logs(self.config_log_path)
        if not logs:
            return None
        errors = [entry.get("error", 0) for entry in logs]
        avg_error = np.mean(errors) if errors else None
        return avg_error

    def analyze_signal_activity(self):
        logs = self.read_logs(self.signal_log_path)
        if not logs:
            return None
        scores = [entry.get("score", 0) for entry in logs]
        avg_score = np.mean(scores) if scores else None
        return avg_score

    def decide_actions(self):
        avg_error = self.analyze_config_history()
        avg_signal_score = self.analyze_signal_activity()
        actions = []
        # If error is high, increase mutation aggressiveness.
        if avg_error is not None and avg_error > 50:
            actions.append("Increase mutation aggressiveness")
        # If signal value is low, purge bloated signals.
        if avg_signal_score is not None and avg_signal_score < 1.0:
            actions.append("Purge bloated signals")
        # If no actionable trends, maintain current trajectory.
        if not actions:
            actions.append("Maintain current trajectory")
        return actions

    def run(self):
        actions = self.decide_actions()
        print("MetaOperator Decision:")
        for action in actions:
            print("-", action)
        return actions

if __name__ == "__main__":
    operator = MetaOperator()
    operator.run()
