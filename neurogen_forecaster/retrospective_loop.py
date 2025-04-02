import json
import os
import numpy as np

def evaluate_config_upgrade(current_predictions, actuals, current_config):
    print("⚙️  Retrospective loop triggered")
    error = np.mean((np.array(current_predictions) - np.array(actuals)) ** 2)
    new_config = current_config.copy()
    new_config['model']['learning_rate'] *= 1.1
    decision = "accepted"
    final_config = new_config
    os.makedirs("logs", exist_ok=True)
    log_entry = {
        "error": float(error),
        "decision": decision,
        "new_config": new_config,
        "final_config": final_config
    }
    with open("logs/config_history.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    return final_config
