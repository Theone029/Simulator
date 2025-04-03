class Module:
    def __init__(self, config):
        self.name = "kernel_fork_best"
        self.threshold = config.get("delta_H_threshold", 0.1)

    def run(self, system_state):
        delta_H = system_state.get("kernel_delta_H", 0)
        if delta_H > self.threshold:
            print(f"[FORK] Kernel delta_H = {delta_H:.4f} > threshold. Triggering symbolic adjustment.")
            return +1.0
        return -0.1
