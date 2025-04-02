#!/bin/bash
pkill -f signal_bridge.py
sleep 1
nohup python3 neurogen_forecaster/external_signal_bridge.py > logs/signal_bridge.out 2>&1 &
echo "[· âœ”] Signal Bridge running in background. Logs: tail -f logs/signal_bridge.out"
