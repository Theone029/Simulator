from pathlib import Path
import json, os

fetchers = {
    "reddit": "neurogen_forecaster/reddit_fetcher.py",
    "twitter": "neurogen_forecaster/twitter_fetcher.py",
    "news": "neurogen_forecaster/news_fetcher.py",
    "finance": "neurogen_forecaster/alpha_fetcher.py"
}

for name, path in fetchers.items():
    f = Path(path)
    if not f.exists(): continue
    code = f.read_text(encoding="utf-8")
    if "FREQS_PATH" not in code:
        pre = f"""
FREQS_PATH = "logs/fetch_frequencies.json"
delay = 3600
if os.path.exists(FREQS_PATH):
    try:
        with open(FREQS_PATH) as f:
            delay = json.load(f).get('{name}', 3600)
    except: pass
"""
        code = f"import os\nimport json\n{pre}\n" + code
    if "time.sleep(delay)" not in code:
        code += "\nimport time\ntime.sleep(delay)\n"
    f.write_text(code, encoding="utf-8")
