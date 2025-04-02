import numpy as np

class StrategyKernel:
    """
    Assigns energy and mutation to high-value domains.
    Prioritizes domains based on the average exploration_score.
    """
    def __init__(self):
        self.domain_scores = {}

    def update_domain_score(self, domain, signals):
        if not signals:
            return 0
        avg_score = np.mean([s.get("exploration_score", 0) for s in signals])
        self.domain_scores[domain] = avg_score
        return avg_score

    def prioritize_domains(self, domain_mapping):
        priorities = {}
        for domain, signals in domain_mapping.items():
            avg_score = self.update_domain_score(domain, signals)
            priorities[domain] = avg_score
        sorted_domains = sorted(priorities.items(), key=lambda x: x[1], reverse=True)
        return sorted_domains

if __name__ == "__main__":
    from domain_mapper import DomainMapper
    mapper = DomainMapper()
    test_signals = [
      {"agent_id": 0, "exploration_score": 0.3},
      {"agent_id": 1, "exploration_score": 0.55},
      {"agent_id": 2, "exploration_score": 0.8}
    ]
    for sig in test_signals:
        mapper.map_signal(sig)
    kernel = StrategyKernel()
    priorities = kernel.prioritize_domains(mapper.get_domains())
    print("Domain priorities:", priorities)
