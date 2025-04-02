#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, json
from collections import defaultdict

THRESHOLD = 3  # Lowered to find common patterns
PLANKS = defaultdict(int)
EXTENSIONS = (".py",)

def extract_ngrams(code, n=3):
    tokens = re.findall(r"[a-zA-Z_][a-zA-Z_0-9]*|\S", code)
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def scan_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()
            ngrams = extract_ngrams(code)
            for gram in ngrams:
                key = " ".join(gram)
                PLANKS[key] += 1
    except Exception as e:
        print(f"Error reading {path}: {e}")

def main():
    print("[] Scanning for frequent planks...")
    for root, dirs, files in os.walk("neurogen_forecaster"):
        for file in files:
            if file.endswith(EXTENSIONS):
                scan_file(os.path.join(root, file))

    filtered = {k: v for k, v in PLANKS.items() if v >= THRESHOLD}
    sorted_ = dict(sorted(filtered.items(), key=lambda x: -x[1]))
    
    with open("logs/plank_candidates.json", "w") as f:
        json.dump(sorted_, f, indent=2)

    print(f"[✓] {len(sorted_)} planks saved to logs/plank_candidates.json")

if __name__ == "__main__":
    main()
