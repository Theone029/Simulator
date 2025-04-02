from utils.event_logger import log_event
from datetime import datetime
import time, random

def run_bridge():
    while True:
        now = datetime.utcnow().isoformat()
        with open("logs/signal_bridge.out", "a") as f:
            f.write(f"[{now}] Signal bridge heartbeat. No signal passed.\n")
        time.sleep(5)

if __name__ == "__main__":
    run_bridge()
