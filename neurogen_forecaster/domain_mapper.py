import numpy as np

class DomainMapper:
    """
    Tracks which signals belong to which domain clusters.
    For demonstration, assigns signals to domains based on exploration_score.
    """
    def __init__(self):
        self.domains = {}

    def map_signal(self, signal):
        score = signal.get("exploration_score", 0)
        if score < 0.4:
            domain = "low"
        elif score < 0.7:
            domain = "medium"
        else:
            domain = "high"
        if domain not in self.domains:
            self.domains[domain] = []
        self.domains[domain].append(signal)
        return domain

    def get_domains(self):
        return self.domains

if __name__ == "__main__":
    mapper = DomainMapper()
    test_signals = [
      {"agent_id": 0, "exploration_score": 0.3},
      {"agent_id": 1, "exploration_score": 0.5},
      {"agent_id": 2, "exploration_score": 0.8}
    ]
    for sig in test_signals:
        domain = mapper.map_signal(sig)
        print(f"Signal from agent {sig['agent_id']} mapped to domain: {domain}")
    print("Domain mapping:", mapper.get_domains())
