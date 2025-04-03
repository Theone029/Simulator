from recursion_kernel import RecursionKernel
from kernel_mutator import mutate_kernel

class KernelAnchor:
    def __init__(self):
        self.kernel = RecursionKernel()
        self.step_count = 0

    def cycle(self):
        metrics = self.kernel.step()
        self.step_count += 1

        log_entry = {
            'cycle': self.step_count,
            'x_t': metrics['x_t'],
            'u_t': metrics['u_t'],
            'C(t)': metrics['C(t)'],
            'H(x)': metrics['H(x)'],
            'ΔH': metrics['ΔH'],
            'compression_ratio': metrics['compression']['compression_ratio']
        }
        self.last_metrics = metrics
        return log_entry

    def evaluate(self, neurogen_score):
        if self.last_metrics['C(t)'] < neurogen_score:
            print(f"[ANCHOR Δ] Kernel superior. ΔC = {neurogen_score - self.last_metrics['C(t)']:.4f}")
            return 'IMPORT_KERNEL_LOGIC'
        else:
            return 'NO_ACTION'

    def mutate_if_needed(self):
        ΔH = self.last_metrics.get('ΔH', 0)
        if abs(ΔH) > 0.2 or abs(ΔH) < 0.01:
            self.kernel = mutate_kernel(self.kernel)
            print("[ANCHOR] Kernel mutated due to ΔH:", ΔH)

def adopt_kernel_controller(kernel_league, neurogen_agent):
    μ = kernel_league.get_best_kernel().get_internal_refs()['μ']
    with torch.no_grad():
        for p_target, p_source in zip(neurogen_agent.parameters(), μ.parameters()):
            p_target.copy_(p_source)
    print("[NEUROGEN] Controller μ replaced from league winner.")

def bias_neurogen_from_kernel(tokens):
    if tokens['ΔH'] > 0.3:
        print("[PLANNER] Kernel chaos detected. Increase exploration rate.")
        return {'explore_boost': True}
    elif tokens['ΔH'] < -0.2:
        print("[PLANNER] High compression kernel. Prioritize its structure.")
        return {'copy_structure': True}
    return {}

def shape_neurogen_from_beacons(beacons):
    last = beacons[-1] if beacons else None
    if not last:
        return {}

    ΔH = last['ΔH']
    CR = last['CR']
    C = last['C']

    plan = {}

    if ΔH > 0.25:
        print("[PLANNER] High entropy delta → escalate exploration.")
        plan['explore'] = True
    if CR < 0.5:
        print("[PLANNER] High compressibility → prioritize compression strategies.")
        plan['compress'] = True
    if C < 0.1 and ΔH < 0:
        print("[PLANNER] Kernel reaching equilibrium → test freeze or fork.")
        plan['clone_kernel'] = True

    return plan
