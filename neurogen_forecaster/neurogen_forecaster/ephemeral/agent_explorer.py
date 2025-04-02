import random
from recursive_score import RecursiveScore

class Module:
    def __init__(self, config):
        self.task_history = []
        self.max_agents = config.get("max_agents", 3)
        self.scorer = RecursiveScore()

    def run(self, system_state):
        # Simulate launching an agent to try a config variant
        recent_config = system_state.get("recent_configs", [])[-1] if system_state.get("recent_configs") else [0.001]
        test_config = [x * random.uniform(0.9, 1.1) for x in recent_config]
        error_before = system_state.get("recent_errors", [])[-1] if system_state.get("recent_errors") else 0.1

        # Fake outcome: sometimes it helps, sometimes it doesn't
        delta_accuracy = random.uniform(-0.02, 0.03)
        delta_entropy = random.uniform(-0.01, 0.015)
        delta_synergy = random.choice([0.0, 0.01])
        cost_estimate = 0.15 + 0.03 * len(self.task_history)

        result = {
            "tested_config": test_config,
            "delta_accuracy": delta_accuracy,
            "delta_entropy": delta_entropy,
            "cost": cost_estimate
        }

        self.task_history.append(result)
        return self.scorer.compute(
            delta_accuracy=delta_accuracy,
            delta_entropy=delta_entropy,
            delta_synergy=delta_synergy,
            cost=cost_estimate
        )
