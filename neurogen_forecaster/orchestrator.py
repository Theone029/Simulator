import time
import importlib
import json
from datetime import datetime

class EphemeralModule:
    def __init__(self, name, config):
        self.name = name
        self.module = importlib.import_module(f"ephemeral.{name}")
        self.instance = self.module.Module(config)
        self.score = 0.0
        self.cycles = 0
        self.max_cycles = config.get("max_cycles", 5)
        self.id = f"{name}_{datetime.utcnow().isoformat()}"

    def run(self, system_state):
        improvement = self.instance.run(system_state)
        self.score += improvement
        self.cycles += 1
        return improvement

    def should_terminate(self):
        avg_score = self.score / (self.cycles + 1e-6)
        return avg_score <= 0 or self.cycles >= self.max_cycles

class Orchestrator:
    def __init__(self, config):
        self.config = config
        self.active_modules = []
        self.logs = []

    def check_triggers(self, system_state):
        triggers = []
        if system_state.get("error_streak", 0) >= 3:
            triggers.append("symbolic_compressor")
        if system_state.get("entropy_spike", False):
            triggers.append("agent_explorer")
        if system_state.get("domain_shift", False):
            triggers.append("domain_mapper")
        return triggers

    def spawn_modules(self, triggers):
        for name in triggers:
            if not any(mod.name == name for mod in self.active_modules):
                config = self.config.get("ephemeral_modules", {}).get(name, {})
                self.active_modules.append(EphemeralModule(name, config))
                self.log(f"SPAWNED: {name}")

    def run_modules(self, system_state):
        surviving = []
        for module in self.active_modules:
            delta = module.run(system_state)
            self.log(f"RAN: {module.name} | Δ: {delta:.4f}")
            if not module.should_terminate():
                surviving.append(module)
            else:
                self.log(f"TERMINATED: {module.name} after {module.cycles} cycles")
        self.active_modules = surviving

    def step(self, system_state):
        triggers = self.check_triggers(system_state)
        self.spawn_modules(triggers)
        self.run_modules(system_state)

    def log(self, message):
        entry = {
            "time": datetime.utcnow().isoformat(),
            "event": message
        }
        print("[ORCH]", message)
        self.logs.append(entry)
        with open("logs/orchestrator_log.jsonl", "a") as f:
            f.write(json.dumps(entry) + "\\n")
