from recursion_kernel import RecursionKernel
from kernel_mutator import mutate_kernel

class KernelLeague:
    def __init__(self, num_kernels=4):
        self.kernels = [RecursionKernel(x0=2.0 + i) for i in range(num_kernels)]
        self.fitness_history = [[] for _ in self.kernels]

    def step_all(self):
        logs = []
        for i, kernel in enumerate(self.kernels):
            metrics = kernel.step()
            self.fitness_history[i].append(metrics['C(t)'])
            logs.append((i, metrics))
        return logs

    def get_best_kernel(self):
        avg_costs = [
            (i, sum(hist[-20:]) / len(hist[-20:]) if len(hist) >= 5 else float('inf'))
            for i, hist in enumerate(self.fitness_history)
        ]
        best_idx = min(avg_costs, key=lambda x: x[1])[0]
        return self.kernels[best_idx]

    def evolve_league(self):
        ranked = sorted(
            [(i, sum(hist[-10:]) / len(hist[-10:]) if hist else float("inf"))
             for i, hist in enumerate(self.fitness_history)],
            key=lambda x: x[1]
        )
        survivors = [self.kernels[i] for i, _ in ranked[:len(ranked)//2]]
        self.kernels = survivors + [mutate_kernel(k) for k in survivors]
        self.fitness_history = [self.fitness_history[i] for i, _ in ranked[:len(ranked)//2]] + [[] for _ in survivors]
        print(f"[LEAGUE] Evolved → {len(self.kernels)} kernels total")
