from recursion_kernel import RecursionKernel
from kernel_watchdog import KernelWatchdog
from kernel_mutator import mutate_kernel
from kernel_league import KernelLeague
import time

kernel_league = KernelLeague(num_kernels=4)
watchdogs = [KernelWatchdog() for _ in kernel_league.kernels]

def run_kernel_league_loop(steps=50):
    print("=== NEUROGEN SYMBOLIC KERNEL LOOP ===")
    for step in range(steps):
        for i, kernel in enumerate(kernel_league.kernels):
            metrics = watchdogs[i].safe_step(kernel)
            if metrics:
                print(f"[KERNEL {i}] Step {step} | x_t={metrics['x_t']:.4f} | C={metrics['C(t)']:.4f} | ΔH={metrics['delta_H']:.4f} | CR={metrics['compression']['compression_ratio']:.3f}")
        if step % 10 == 0:
            print("--- League Evolution ---")
            kernel_league.evolve_league()
        time.sleep(0.25)
    print("=== END LOOP ===")

if __name__ == "__main__":
    run_kernel_league_loop()

import json

def emit_best_kernel_config(path="logs/best_kernel.json"):
    best = kernel_league.get_best_kernel()
    refs = best.get_internal_refs()
    config = {
        "x_t": best.env.x,
        "noise_std": best.env.noise_std,
        "learning_rate": refs["optimizer"].param_groups[0]['lr'],
        "controller_arch": str(refs["mu"])
    }
    with open(path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"[EXPORT] Best kernel config written to {path}")

def log_best_kernel_beacon(path="logs/kernel_beacons.jsonl"):
    best = kernel_league.get_best_kernel()
    metrics = best.get_metrics()
    beacon = {
        "t": time.time(),
        "x_t": metrics["x_t"],
        "C": metrics["C(t)"],
        "delta_H": metrics["delta_H"],
        "CR": metrics["compression"]["compression_ratio"]
    }
    with open(path, "a") as f:
        f.write(json.dumps(beacon) + "\n")
    print("[BEACON] Logged:", beacon)

# === PATCH: Full Loop w/ Export + Beacon ===
def run_kernel_league_loop(steps=50):
    print("=== NEUROGEN SYMBOLIC KERNEL LOOP ===")
    for step in range(steps):
        for i, kernel in enumerate(kernel_league.kernels):
            metrics = watchdogs[i].safe_step(kernel)
            if metrics:
                print(f"[KERNEL {i}] Step {step} | x_t={metrics['x_t']:.4f} | C={metrics['C(t)']:.4f} | ΔH={metrics['delta_H']:.4f} | CR={metrics['compression']['compression_ratio']:.3f}")
        if step % 10 == 0:
            print("--- League Evolution ---")
            kernel_league.evolve_league()
            emit_best_kernel_config()
        log_best_kernel_beacon()
        time.sleep(0.25)
    print("=== END LOOP ===")
