#!/bin/bash
while true; do
  python3 neurogen_forecaster/weighted_signal_ingestor.py
  python3 neurogen_forecaster/signal_module_injector.py
python3 neurogen_forecaster/llm_mutation_engine.py
python3 neurogen_forecaster/signal_feedback_loop.py
python3 neurogen_forecaster/llm_mutation_engine.py
  sleep 5
done
