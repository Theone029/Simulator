import numpy as np
import random

class Module:
    def __init__(self, config):
        self.explorations = 0
        self.max_explorations = config.get("max_explorations", 3)

    def run(self, system_state):
        if system_state.get("entropy_spike", False):
            improvement = random.uniform(0.1, 0.5)
            self.explorations += 1
            print("[AGENT_EXPLORER] Exploration yield:", improvement)
            return improvement
        return 0.0
