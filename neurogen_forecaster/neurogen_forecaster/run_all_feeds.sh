#!/bin/bash
while true; do
  python3 neurogen_forecaster/reddit_fetcher.py && python3 neurogen_forecaster/reddit_to_signal.py
  python3 neurogen_forecaster/twitter_fetcher.py && python3 neurogen_forecaster/twitter_to_signal.py
  python3 neurogen_forecaster/news_fetcher.py && python3 neurogen_forecaster/news_to_signal.py
  python3 neurogen_forecaster/alpha_fetcher.py && python3 neurogen_forecaster/alpha_to_signal.py
  sleep 300  # every 5 min
done
