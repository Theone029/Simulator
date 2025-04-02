import json

class RecursiveInterface:
    """
    Translates NEUROGEN's belief space (a dict) into coherent language and back.
    """
    def beliefs_to_text(self, beliefs):
        # Convert belief dict to a human-readable string.
        return json.dumps(beliefs, indent=2)

    def text_to_beliefs(self, text):
        # Parse text back to a dictionary.
        try:
            return json.loads(text)
        except Exception:
            return {}
    
if __name__ == "__main__":
    interface = RecursiveInterface()
    sample_beliefs = {"learning_rate": 0.001, "error_trend": "decreasing"}
    text = interface.beliefs_to_text(sample_beliefs)
    print("Beliefs as text:\n", text)
    recovered = interface.text_to_beliefs(text)
    print("Recovered beliefs:", recovered)
