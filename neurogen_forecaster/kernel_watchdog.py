import traceback
import time

class KernelWatchdog:
    def __init__(self):
        self.error_log = []
        self.history = []

    def safe_step(self, kernel):
        try:
            metrics = kernel.step()
            metrics['timestamp'] = time.time()
            self.history.append(metrics)
            return metrics
        except Exception as e:
            err = {
                'error': str(e),
                'trace': traceback.format_exc(),
                'timestamp': time.time()
            }
            self.error_log.append(err)
            print("[WATCHDOG] Kernel failure:", err['error'])
            return None

    def get_beacons(self):
        return [{
            't': m['timestamp'],
            'C': m['C(t)'],
            'ΔH': m['ΔH'],
            'CR': m['compression']['compression_ratio']
        } for m in self.history]

    def report(self):
        return {
            'errors': self.error_log,
            'beacons': self.get_beacons()
        }
