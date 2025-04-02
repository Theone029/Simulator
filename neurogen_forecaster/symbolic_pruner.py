import json

class SymbolicPruner:
    """
    Deletes unused or ineffective symbolic rules.
    Maintains a pruned set of rules.
    """
    def __init__(self, rules=None):
        if rules is None:
            rules = []
        self.rules = rules

    def prune_rules(self):
        """
        Prune rules that are less than a threshold length (dummy criterion).
        """
        pruned = [rule for rule in self.rules if len(rule) > 10]
        self.rules = pruned
        return self.rules

    def add_rule(self, rule):
        self.rules.append(rule)

if __name__ == "__main__":
    pruner = SymbolicPruner()
    pruner.add_rule("Short")
    pruner.add_rule("This is a valid rule.")
    pruned = pruner.prune_rules()
    print("Pruned rules:", pruned)
