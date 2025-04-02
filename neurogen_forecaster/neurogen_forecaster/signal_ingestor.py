import json

def should_ingest(signal, baseline_score=0.1):
    # Placeholder: ingest signals with delta_accuracy > 0.02.
    return signal.get("delta_accuracy", 0) > 0.02

def ingest(input_path="logs/signal_stream.jsonl", output_path="logs/accepted_signals.jsonl"):
    accepted = []
    try:
        with open(input_path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    for line in lines:
        if not line.strip():
            continue
        try:
            signal = json.loads(line)
            if should_ingest(signal):
                accepted.append(signal)
        except Exception:
            continue
    if accepted:
        with open(output_path, "a") as out:
            for sig in accepted:
                out.write(json.dumps(sig) + "\n")

if __name__ == "__main__":
    ingest()
