from recursive_score import RecursiveScore

scorer = RecursiveScore()
scorer.compute(delta_accuracy=0.03, delta_entropy=0.02, delta_synergy=0.01, cost=0.1)
