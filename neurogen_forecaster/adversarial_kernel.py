from recursion_kernel import RecursionKernel

class AdversarialKernel(RecursionKernel):
    def step(self):
        metrics = super().step()
        metrics['C(t)'] *= -1
        metrics['delta_H'] *= -1
        return metrics
