#!/bin/bash
# Kill any existing processes first
pkill -f external_signal_bridge.py
pkill -f signal_ingestor.py
pkill -f signal_module_injector.py
sleep 1

# Launch the external signal bridge (assumes it's already created and working)
nohup python3 neurogen_forecaster/external_signal_bridge.py > logs/signal_bridge.out 2>&1 &
echo "Signal Bridge started in background."

# Launch the signal ingestor (runs once and exits; you can schedule it via cron if needed)
nohup python3 neurogen_forecaster/signal_ingestor.py > logs/signal_ingestor.out 2>&1 &
echo "Signal Ingestor executed in background."

# Launch the signal module injector to monitor accepted signals continuously
nohup python3 neurogen_forecaster/signal_module_injector.py > logs/signal_injector.out 2>&1 &
echo "Signal Module Injector started in background."

