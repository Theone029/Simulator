import json
import os

class DominanceTracker:
    """
    Logs improvement rate, entropy compression, and influence gain for each domain.
    """
    def __init__(self, log_path="logs/dominance_log.jsonl"):
        self.log_path = log_path
        os.makedirs("logs", exist_ok=True)

    def log_dominance(self, domain, improvement_rate, entropy_compression, influence_gain):
        log_entry = {
            "domain": domain,
            "improvement_rate": improvement_rate,
            "entropy_compression": entropy_compression,
            "influence_gain": influence_gain
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        print(f"Dominance logged for domain {domain}")

if __name__ == "__main__":
    tracker = DominanceTracker()
    tracker.log_dominance("high", 0.2, 0.3, 0.5)
