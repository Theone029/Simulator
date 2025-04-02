from recursive_score import RecursiveScore
from retrospective_score_optimizer import RetrospectiveScoreOptimizer

if __name__ == "__main__":
    scorer = RecursiveScore()
    optimizer = RetrospectiveScoreOptimizer(scorer)
    optimizer.run_loop(interval=300)  # Runs every 5 minutes
