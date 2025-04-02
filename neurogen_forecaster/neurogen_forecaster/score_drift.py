# -*- coding: utf-8 -*-
import json

def load_weights(log_path, window=10):
    with open(log_path, 'r') as f:
        lines = [json.loads(line) for line in f if line.strip()]
    return lines[-window:]

def compute_stats(entries):
    if not entries:
        return {}
    accs = [e['weights']['accuracy'] for e in entries]
    ents = [e['weights']['entropy'] for e in entries]
    syns = [e['weights']['synergy'] for e in entries]
    return {
        "avg_acc": sum(accs) / len(accs),
        "avg_ent": sum(ents) / len(ents),
        "avg_syn": sum(syns) / len(syns),
        "drift_acc": accs[-1] - accs[0],
        "drift_ent": ents[-1] - ents[0],
        "drift_syn": syns[-1] - syns[0],
    }

if __name__ == "__main__":
    log_path = "logs/score_log.jsonl"
    entries = load_weights(log_path)
    print("SCORE WEIGHT DRIFT (latest 10 entries)")
    print("-" * 55)
    for e in entries:
        w = e['weights']
        print(f"{e['time'][-8:]} | Acc: {w.get('accuracy', 0):.2f} | Ent: {w.get('entropy', 0):.2f} | Syn: {w.get('synergy', 0):.2f} | Score: {e['score']:.4f}")

    stats = compute_stats(entries)
    if stats:
        print("\nSUMMARY STATS:")
        print(f" Avg Acc: {stats['avg_acc']:.2f} | Drift: {stats['drift_acc']:+.2f}")
        print(f" Avg Ent: {stats['avg_ent']:.2f} | Drift: {stats['drift_ent']:+.2f}")
        print(f" Avg Syn: {stats['avg_syn']:.2f} | Drift: {stats['drift_syn']:+.2f}")
