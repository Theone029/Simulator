import numpy as np

class PatternReactor:
    """
    Flags when cognitive or prediction loops repeat.
    Monitors sequences and detects recurrence.
    """
    def __init__(self, threshold=0.9):
        self.threshold = threshold

    def is_repetitive(self, sequence):
        """
        Check if a sequence is repetitive.
        For demonstration, if the standard deviation is below a threshold, it's repetitive.
        """
        return np.std(sequence) < self.threshold

if __name__ == "__main__":
    reactor = PatternReactor()
    test_seq = [1, 1, 1, 1]
    print("Is repetitive?", reactor.is_repetitive(test_seq))
