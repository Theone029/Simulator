import numpy as np

class FlatlineDetector:
    """
    Detects flatline in performance over consecutive epochs.
    Returns True if no significant improvement is observed over the window.
    """
    def __init__(self, window_size=5, improvement_threshold=0.01):
        self.window_size = window_size
        self.improvement_threshold = improvement_threshold
        self.history = []

    def update(self, loss):
        self.history.append(loss)
        if len(self.history) > self.window_size:
            self.history.pop(0)
            improvement = self.history[0] - self.history[-1]
            return improvement < self.improvement_threshold
        return False
