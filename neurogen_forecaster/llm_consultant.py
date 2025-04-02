import json

class LLMConsultant:
    """
    Simulates LLM-based config suggestions.
    Only triggered on system stagnation or contradictory signals.
    """
    def __init__(self, token_cost=0.01):
        self.token_cost = token_cost
        self.cache = {}

    def consult(self, query):
        if query in self.cache:
            return self.cache[query]
        # Dummy simulation: propose to multiply learning rate by 0.9
        suggestion = {"model": {"learning_rate": 0.9}}
        self.cache[query] = suggestion
        return suggestion

    def apply_suggestion(self, current_config, suggestion):
        new_config = current_config.copy()
        new_config["model"]["learning_rate"] *= suggestion["model"]["learning_rate"]
        return new_config
