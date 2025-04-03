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

from adversarial_kernel import AdversarialKernel

adversarial_kernels = [AdversarialKernel(x0=5.0 + i) for i in range(2)]

def run_adversarial_kernels(steps=50):
    print("=== ADVERSARIAL KERNELS ===")
    for step in range(steps):
        for i, k in enumerate(adversarial_kernels):
            metrics = k.step()
            print(f"[ADVERSARY {i}] Step {step} | x_t={metrics['x_t']:.4f} | C={-metrics['C(t)']:.4f} | ΔH={-metrics['delta_H']:.4f}")

from adversarial_kernel import AdversarialKernel
adversarial_kernels = [AdversarialKernel(x0=5.0 + i) for i in range(2)]

def run_adversarial_kernels(step):
    for i, k in enumerate(adversarial_kernels):
        metrics = k.step()
        print(f"[ADVERSARY {i}] Step {step} | x_t={metrics['x_t']:.4f} | C={-metrics['C(t)']:.4f} | ΔH={-metrics['delta_H']:.4f}")

# PATCH: Adversary injection into kernel loop
old_loop = run_kernel_league_loop
def run_kernel_league_loop(steps=50):
    print("=== NEUROGEN DUAL-LEAGUE KERNEL LOOP ===")
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
        if step % 10 == 5:
            run_adversarial_kernels(step)
        time.sleep(0.25)
    print("=== END LOOP ===")

# ✅ REPLACE any existing log_best_kernel_beacon
def log_best_kernel_beacon(path="logs/kernel_beacons.jsonl"):
    import json, os, time
    try:
        os.makedirs("logs", exist_ok=True)
        best = kernel_league.get_best_kernel()
        metrics = best.get_metrics()
        beacon = {
            "t": time.time(),
            "x_t": metrics.get("x_t", 0),
            "C": metrics.get("C(t)", 0),
            "delta_H": metrics.get("delta_H", 0),
            "CR": metrics.get("compression", {}).get("compression_ratio", 1.0)
        }
        with open(path, "a") as f:
            f.write(json.dumps(beacon) + "\n")
        print("[BEACON] Logged:", beacon)
    except Exception as e:
        print("[BEACON ERROR]", e)
