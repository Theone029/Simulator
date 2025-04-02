import numpy as np

class TaskRewardEstimator:
    """
    Estimates long-term reward from agent tasks.
    """
    def __init__(self):
        pass

    def estimate_reward(self, task_results):
        """
        Given a list of task results (dictionaries), compute a reward value.
        For demo, reward is the average exploration_score.
        """
        if not task_results:
            return 0.0
        reward = np.mean([r.get("exploration_score", 0) for r in task_results])
        return reward

if __name__ == "__main__":
    estimator = TaskRewardEstimator()
    dummy_results = [{"exploration_score": 0.5}, {"exploration_score": 0.7}]
    reward = estimator.estimate_reward(dummy_results)
    print("Estimated reward:", reward)
