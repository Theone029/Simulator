from agent_launcher import AgentLauncher
from task_reward_estimator import TaskRewardEstimator
from agent_memory import AgentMemory

def main():
    launcher = AgentLauncher(num_agents=3)
    results = launcher.launch_agents()
    print("Agent Launcher results:", results)

    estimator = TaskRewardEstimator()
    reward = estimator.estimate_reward(results)
    print("Estimated Task Reward:", reward)

    memory = AgentMemory()
    for res in results:
        memory.log_agent_result(res)
    print("Loaded Agent Memory:", memory.load_memory())

if __name__ == "__main__":
    main()
