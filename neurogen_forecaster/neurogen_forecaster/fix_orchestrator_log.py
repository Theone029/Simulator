import re, json

with open("logs/orchestrator_log.jsonl", "r") as f:
    raw = f.read()

entries = re.findall(r'\{.*?\}', raw.replace("\n", "\n"))
with open("logs/orchestrator_log.jsonl", "w") as out:
    for entry in entries:
        try:
            json.loads(entry)
            out.write(entry + "\n")
        except json.JSONDecodeError:
            continue
