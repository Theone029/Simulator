import os
import json

FREQS_PATH = "logs/fetch_frequencies.json"
delay = 3600
if os.path.exists(FREQS_PATH):
    try:
        with open(FREQS_PATH) as f:
            delay = json.load(f).get('reddit', 3600)
    except: pass

# -*- coding: utf-8 -*-
import praw, os, json
# Initialize PRAW with environment variables
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_SECRET")
user_agent = "neurogen"
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
posts = []
for post in reddit.subreddit("all").hot(limit=25):
    posts.append({
        "title": post.title,
        "score": post.score,
        "time": post.created_utc
    })
os.makedirs("logs", exist_ok=True)
with open("logs/reddit_raw.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, indent=2)
print(f"[✓] Pulled {len(posts)} Reddit posts.")

import time
time.sleep(delay)
