#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os, time

SCORES_PATH = "logs/signal_feedback_scores.json"
SH_PATH = "neurogen_forecaster/run_feed_loop.sh"
BASE_FREQ = 3600  # seconds

def calc_delay(score):
    return int(BASE_FREQ / max(score, 1.0))

while True:
    if not os.path.exists(SCORES_PATH):
        time.sleep(60); continue
    with open(SCORES_PATH) as f: scores = json.load(f)

    reddit_d = calc_delay(scores.get("reddit", 1))
    news_d   = calc_delay(scores.get("news", 1))
    alpha_d  = calc_delay(scores.get("finance", 1))
    twitter_d= calc_delay(scores.get("twitter", 1))

    with open(SH_PATH, "w") as sh:
        sh.write("#!/bin/bash\n")
        sh.write("while true; do\n")
        sh.write("  echo '[⟳] Feed loop tick'\n")
        sh.write("  python3 neurogen_forecaster/reddit_fetcher.py && python3 neurogen_forecaster/reddit_to_signal.py\n")
        sh.write(f"  sleep {reddit_d}\n")
        sh.write("  python3 neurogen_forecaster/news_fetcher.py && python3 neurogen_forecaster/news_to_signal.py\n")
        sh.write(f"  sleep {news_d}\n")
        sh.write("  python3 neurogen_forecaster/alpha_fetcher.py && python3 neurogen_forecaster/alpha_to_signal.py\n")
        sh.write(f"  sleep {alpha_d}\n")
        sh.write("  python3 neurogen_forecaster/twitter_fetcher.py && python3 neurogen_forecaster/twitter_to_signal.py\n")
        sh.write(f"  sleep {twitter_d}\n")
        sh.write("  python3 neurogen_forecaster/signal_ingestor.py\n")
        sh.write("  python3 neurogen_forecaster/signal_module_injector.py\n")
        sh.write("done\n")

    print(f"[⚙️] Feed loop mutated based on scores: reddit={reddit_d}s, news={news_d}s, alpha={alpha_d}s, twitter={twitter_d}s")
    time.sleep(300)
