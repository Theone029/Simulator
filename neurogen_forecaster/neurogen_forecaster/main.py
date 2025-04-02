
# --- Recursive Score Optimizer Integration ---
from recursive_score import RecursiveScore
from retrospective_score_optimizer import RetrospectiveScoreOptimizer

scorer = RecursiveScore()
optimizer = RetrospectiveScoreOptimizer(scorer)

# Call this after config mutation or flatline detection
def maybe_tune_scoring(error_history, threshold=0.0005):
    if len(error_history) < 10:
        return
    recent = error_history[-5:]
    delta = abs(recent[-1] - recent[0])
    if delta < threshold:
        print("[OPTIMIZER] Flatline detected. Retuning scoring weights.")
        optimizer.run_once()
