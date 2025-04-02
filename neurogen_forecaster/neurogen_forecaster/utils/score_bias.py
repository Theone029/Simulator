import json
def get_bias():
    try:
        with open("logs/signal_feedback_scores.json") as f:
            return json.load(f)
    except:
        return {}
