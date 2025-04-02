#!/bin/bash
while true; do
  echo '[⟳] Feed loop tick'
  python3 neurogen_forecaster/reddit_fetcher.py && python3 neurogen_forecaster/reddit_to_signal.py
  sleep 450
  python3 neurogen_forecaster/news_fetcher.py && python3 neurogen_forecaster/news_to_signal.py
  sleep 867
  python3 neurogen_forecaster/alpha_fetcher.py && python3 neurogen_forecaster/alpha_to_signal.py
  sleep 3600
  python3 neurogen_forecaster/twitter_fetcher.py && python3 neurogen_forecaster/twitter_to_signal.py
  sleep 3600
  python3 neurogen_forecaster/signal_ingestor.py
  python3 neurogen_forecaster/signal_module_injector.py
done
