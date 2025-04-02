import random, json, time
from datetime import datetime

def generate_mock_signal():
    return {
        "delta_accuracy": round(random.uniform(0.01, 0.15), 3),
        "delta_entropy": round(random.uniform(0.01, 0.05), 3),
        "token_cost": round(random.uniform(0.005, 0.02), 3),
        "time_cost": round(random.uniform(0.005, 0.02), 3)
    }

if __name__ == "__main__":
    while True:
        signal = generate_mock_signal()
        with open("logs/signal_stream.jsonl", "a") as f:
            f.write(json.dumps(signal) + "\n")
        print(f"[+] Emitted mock signal at {datetime.utcnow().isoformat()}")
        time.sleep(8)
