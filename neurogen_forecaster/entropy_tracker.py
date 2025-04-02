import numpy as np

class EntropyTracker:
    """
    Tracks and simulates entropy (surprise measure) over time.
    """
    def __init__(self, initial_entropy=1.0):
        self.current_entropy = initial_entropy

    def update_entropy(self, data):
        """
        Update the current entropy based on new data.
        For demonstration, we use the standard deviation as a proxy.
        """
        self.current_entropy = np.std(data)
        return self.current_entropy

    def simulate_with(self, data):
        """
        Simulate new entropy if the given data is ingested.
        Decreases entropy based on data variability.
        """
        simulated = self.current_entropy - (np.std(data) * 0.1)
        return simulated
