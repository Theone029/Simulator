# -*- coding: utf-8 -*-
import json, time
with open("logs/module_impact.jsonl", "a") as f:
    f.write(json.dumps({
        "time": time.time(),
        "event": "signal_cycle_snapshot"
    }) + "\n")
