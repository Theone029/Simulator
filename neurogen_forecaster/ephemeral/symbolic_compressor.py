import numpy as np
import random

class Module:
    def __init__(self, config):
        self.rules = []
        self.history = []
        self.max_rules = config.get("max_rules", 5)

    def run(self, system_state):
        recent_errors = system_state.get("recent_errors", [])
        recent_configs = system_state.get("recent_configs", [])
        if len(recent_errors) < 3 or len(recent_configs) < 3:
            return 0.0
        delta_errors = np.diff(recent_errors)
        delta_configs = np.diff(recent_configs, axis=0)
        correlation = np.corrcoef(delta_errors, delta_configs[:, 0])[0, 1]
        if abs(correlation) > 0.6:
            rule = f"IF config[0] increases THEN error changes ≈ {correlation:.2f}"
            if rule not in self.rules and len(self.rules) < self.max_rules:
                self.rules.append(rule)
                print("[SYMBOLIC_COMPRESSOR] Added Rule:", rule)
                return abs(correlation) * 0.5
        return -0.01
