from recursive_score import RecursiveScore
scorer = RecursiveScore()
score = scorer.compute(delta_accuracy=0.05, delta_entropy=0.02, delta_synergy=0.01, cost=0.1)
print("SCORE =", score)
