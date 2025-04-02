from domain_mapper import DomainMapper
from strategy_kernel import StrategyKernel
from dominance_tracker import DominanceTracker

def main():
    # Test domain mapping
    mapper = DomainMapper()
    signals = [
        {"agent_id": 0, "exploration_score": 0.3},
        {"agent_id": 1, "exploration_score": 0.55},
        {"agent_id": 2, "exploration_score": 0.8}
    ]
    for sig in signals:
        mapper.map_signal(sig)
    domains = mapper.get_domains()
    print("Mapped domains:", domains)

    # Test strategy kernel
    kernel = StrategyKernel()
    priorities = kernel.prioritize_domains(domains)
    print("Domain priorities:", priorities)

    # Test dominance tracker
    tracker = DominanceTracker()
    for domain, score in priorities:
        tracker.log_dominance(domain, improvement_rate=score * 0.1, 
                                entropy_compression=score * 0.2, 
                                influence_gain=score * 0.3)

if __name__ == "__main__":
    main()
