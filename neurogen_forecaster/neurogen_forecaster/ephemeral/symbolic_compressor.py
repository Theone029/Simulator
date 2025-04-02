import numpy as np
from recursive_score import RecursiveScore

class Module:
    def __init__(self, config):
        self.rules = []
        self.history = []
        self.max_rules = config.get("max_rules", 5)
        self.scorer = RecursiveScore()

    def run(self, system_state):
        recent_errors = system_state.get("recent_errors", [])
        recent_configs = system_state.get("recent_configs", [])

        if len(recent_errors) < 3 or len(recent_configs) < 3:
            return self.scorer.compute(0.0, 0.0, 0.0, cost=0.1)

        delta_errors = np.diff(recent_errors)
        delta_configs = np.diff(recent_configs, axis=0)

        correlation = np.corrcoef(delta_errors, delta_configs[:, 0])[0, 1]
        cost_estimate = 0.1 + 0.02 * len(self.rules)  # simulate memory cost

        if abs(correlation) > 0.6:
            rule = f"IF config[0] increases THEN error changes ≈ {correlation:.2f}"
            if rule not in self.rules and len(self.rules) < self.max_rules:
                self.rules.append(rule)
                print("[SYMBOLIC_COMPRESSOR] Rule added:", rule)
                return self.scorer.compute(
                    delta_accuracy=abs(correlation) * 0.1,
                    delta_entropy=0.01,
                    delta_synergy=0.01,
                    cost=cost_estimate
                )
        return self.scorer.compute(0.0, 0.0, 0.0, cost=cost_estimate)
