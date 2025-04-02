import numpy as np

class DataIngestor:
    """
    Mock data ingestor to simulate time-series data for x(t).
    Replace this with actual API calls or file reading for real-world signals.
    """
    def __init__(self, config):
        self.config = config
        self.t = 0
        self.state_dim = config["model"]["input_dim"]
        self.current_state = np.zeros(self.state_dim)

    def get_next(self):
        """
        Simulate and return the next time-step state vector.
        """
        # Simulate a random walk update.
        step = np.random.normal(loc=0.0, scale=1.0, size=self.state_dim)
        self.current_state += step
        self.t += 1
        return self.current_state.copy()

    def get_historical_batch(self, length=64):
        """
        Generate a batch of historical states for training.
        Returns an array of shape (length, state_dim).
        """
        data = []
        s = np.zeros(self.state_dim)
        for _ in range(length):
            step = np.random.normal(0.0, 1.0, self.state_dim)
            s += step
            data.append(s.copy())
        return np.array(data)
