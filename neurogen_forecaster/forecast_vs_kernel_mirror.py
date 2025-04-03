import json

def compare_entropy_trends(kernel_path="logs/kernel_beacons.jsonl", forecast_path="logs/forecast_entropy.jsonl"):
    try:
        with open(kernel_path, "r") as f1, open(forecast_path, "r") as f2:
            k_lines = f1.readlines()[-5:]
            f_lines = f2.readlines()[-5:]

        k_deltas = [json.loads(l)["delta_H"] for l in k_lines]
        f_deltas = [json.loads(l)["delta_H"] for l in f_lines]

        k_avg = sum(k_deltas) / len(k_deltas)
        f_avg = sum(f_deltas) / len(f_deltas)

        print(f"[MIRROR] Kernel ΔH: {k_avg:.2f} | Forecast ΔH: {f_avg:.2f}")

        if abs(k_avg - f_avg) > 10:
            print("[MIRROR] ⚠️ Divergence detected.")
        else:
            print("[MIRROR] ✅ Entropy coherence maintained.")

    except Exception as e:
        print("[MIRROR] Error:", str(e))

if __name__ == "__main__":
    compare_entropy_trends()
