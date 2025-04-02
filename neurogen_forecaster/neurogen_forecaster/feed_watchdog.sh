#!/bin/bash
while true; do
  if ! pgrep -f run_feed_loop.sh > /dev/null; then
    echo "[⚠️] Feed loop down. Restarting..." >> logs/watchdog.log
    nohup ./neurogen_forecaster/run_feed_loop.sh > logs/feed_loop.out 2>&1 &
    echo "[⚙️] Feed loop restarted by watchdog." >> logs/watchdog.log
  fi
  sleep 30
done
