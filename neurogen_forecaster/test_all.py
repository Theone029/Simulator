import numpy as np
from entropy_tracker import EntropyTracker
from external_signal_bridge import ExternalSignalBridge
from flatline_detector import FlatlineDetector
from config_rollback import load_last_stable_config, rollback_config
from llm_consultant import LLMConsultant

def main():
    # Test EntropyTracker
    print("Testing EntropyTracker...")
    et = EntropyTracker(initial_entropy=1.0)
    data = np.random.randn(100)
    updated = et.update_entropy(data)
    simulated = et.simulate_with(data)
    print("Updated entropy:", updated)
    print("Simulated entropy:", simulated)

    # Test ExternalSignalBridge
    print("\nTesting ExternalSignalBridge...")
    es = ExternalSignalBridge(entropy_tracker=et, threshold=0.5)
    accepted = es.evaluate_signals()
    print("Accepted signals:", accepted)

    # Test FlatlineDetector
    print("\nTesting FlatlineDetector...")
    fd = FlatlineDetector(window_size=3, improvement_threshold=0.1)
    losses = [100, 99.5, 99.4, 99.3, 99.2]
    for loss in losses:
        is_flat = fd.update(loss)
        print(f"Loss: {loss}, Flatline: {is_flat}")

    # Test Config Rollback (dummy test, expects to load last config if exists)
    print("\nTesting Config Rollback...")
    current_config = {"model": {"learning_rate": 0.001}}
    rolled_back = rollback_config(current_config)
    print("Rolled back config:", rolled_back)

    # Test LLMConsultant
    print("\nTesting LLMConsultant...")
    llm = LLMConsultant(token_cost=0.01)
    suggestion = llm.consult("test query")
    print("LLM Suggestion:", suggestion)
    new_config = llm.apply_suggestion(current_config, suggestion)
    print("New config after LLM suggestion:", new_config)

if __name__ == "__main__":
    main()
