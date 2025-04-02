# -*- coding: utf-8 -*-
import requests, json, time

def fetch_top_hn():
    ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()[:10]
    posts = []
    for i in ids:
        item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{i}.json").json()
        posts.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "score": item.get("score", 0),
            "comments": item.get("descendants", 0),
            "time": item.get("time", time.time())
        })
    return posts

if __name__ == "__main__":
    results = fetch_top_hn()
    with open("logs/hn_raw.json", "w") as f:
        json.dump(results, f, indent=2)
    print("[✓] Fetched top HN posts.")
