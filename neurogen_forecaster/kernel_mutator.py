from recursion_kernel import RecursionKernel

def mutate_kernel(base_kernel, strategy='entropy_spike'):
    metrics = base_kernel.get_metrics()
    H = metrics.get('H(x)', 0)
    delta_H = metrics.get('delta_H', 0)
    new_x0 = base_kernel.env.x
    new_noise = base_kernel.env.noise_std
    new_lr = base_kernel.optimizer.param_groups[0]['lr']

    if strategy == 'entropy_spike' and delta_H > 0.2:
        new_noise *= 0.9
        new_lr *= 0.95
    elif strategy == 'flatline' and abs(delta_H) < 0.01:
        new_noise *= 1.2
        new_lr *= 1.1

    return base_kernel.clone_with(x0=new_x0, noise_std=new_noise, lr=new_lr)
