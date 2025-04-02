#!/bin/bash
while true; do
  python3 neurogen_forecaster/reddit_fetcher.py
  python3 neurogen_forecaster/twitter_fetcher.py
  python3 neurogen_forecaster/news_fetcher.py
  python3 neurogen_forecaster/alpha_fetcher.py
  sleep 120
done
