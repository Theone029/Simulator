#!/bin/bash
while true; do
  echo "[⏳] Fetching Hacker News..."
  python3 neurogen_forecaster/hn_fetcher.py && python3 neurogen_forecaster/hn_to_signal.py
  sleep 600
done
