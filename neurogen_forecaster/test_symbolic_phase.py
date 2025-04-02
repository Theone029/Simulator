import numpy as np
from principle_miner import PrincipleMiner
from pattern_reactor import PatternReactor
from symbolic_pruner import SymbolicPruner

def main():
    # Test PrincipleMiner
    miner = PrincipleMiner()
    predictions = [[1, 2, 3], [4, 5, 6]]
    targets = [[1, 2, 0], [4, 5, 7]]
    rule = miner.mine_rules(predictions, targets)
    print("Mined rule:", rule)
    print("All mined rules:", miner.get_rules())

    # Test PatternReactor
    reactor = PatternReactor(threshold=0.5)
    repetitive_seq = [1, 1, 1, 1]
    non_repetitive_seq = [1, 2, 3, 4]
    print("Repetitive detected (should be True):", reactor.is_repetitive(repetitive_seq))
    print("Repetitive detected (should be False):", reactor.is_repetitive(non_repetitive_seq))

    # Test SymbolicPruner
    pruner = SymbolicPruner()
    pruner.add_rule("Short")
    pruner.add_rule("This is a valid rule.")
    pruned = pruner.prune_rules()
    print("Pruned rules:", pruned)

if __name__ == "__main__":
    main()
