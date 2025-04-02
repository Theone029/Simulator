import numpy as np
import json

class PrincipleMiner:
    """
    Extracts symbolic rules from repeating prediction patterns.
    Processes historical data and identifies recurring motifs.
    """
    def __init__(self):
        self.rules = []

    def mine_rules(self, predictions, targets):
        """
        Given predictions and targets, mine repeating patterns.
        For demonstration, if average error is high, extract a dummy rule.
        """
        error = np.mean((np.array(predictions) - np.array(targets))**2)
        if error > 50:
            rule = f"High error pattern detected: error {error:.2f}"
            self.rules.append(rule)
            return rule
        return None

    def get_rules(self):
        return self.rules

if __name__ == "__main__":
    miner = PrincipleMiner()
    rule = miner.mine_rules([[1,2,3],[4,5,6]], [[1,2,0],[4,5,7]])
    print("Mined rule:", rule)
    print("All rules:", miner.get_rules())
