# -*- coding: utf-8 -*-
import json, yaml, os

CANDIDATES = "logs/plank_candidates.json"
REGISTRY = "config/seed_registry.yaml"
OUTPUT = "logs/plank_mutations.jsonl"

def load_registry():
    if not os.path.exists(REGISTRY): return {}
    with open(REGISTRY) as f: return yaml.safe_load(f)

def load_candidates():
    with open(CANDIDATES) as f:
        data = json.load(f)
        return [{"content": x, "file": "unknown", "line": -1} if isinstance(x, str) else x for x in data]

def compute_savings(raw, symbol):
    return len(raw.split()) - len(symbol.split())

def propose_mutations():
    registry = load_registry()
    candidates = load_candidates()
    proposals = []

    for plank in candidates:
        for symbol, expansion in registry.items():
            if plank["content"].strip() == expansion.strip():
                saving = compute_savings(expansion, symbol)
                if saving > 0:
                    proposals.append({
                        "file": plank["file"],
                        "line": plank["line"],
                        "original": expansion,
                        "replacement": symbol,
                        "savings": saving
                    })

    with open(OUTPUT, "w") as out:
        for p in proposals:
            out.write(json.dumps(p) + "\n")
    print(f"[✓] Proposed {len(proposals)} mutations saved to {OUTPUT}")

if __name__ == "__main__":
    propose_mutations()
