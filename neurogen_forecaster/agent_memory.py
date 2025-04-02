import json
import os

class AgentMemory:
    """
    Stores agent history and maps results to beliefs.
    """
    def __init__(self, memory_path="logs/agent_memory.jsonl"):
        self.memory_path = memory_path
        os.makedirs("logs", exist_ok=True)

    def log_agent_result(self, agent_result):
        """
        Log a single agent result to the memory file.
        """
        with open(self.memory_path, "a") as f:
            f.write(json.dumps(agent_result) + "\n")

    def load_memory(self):
        """
        Load all logged agent results.
        """
        if not os.path.exists(self.memory_path):
            return []
        memory = []
        with open(self.memory_path, "r") as f:
            for line in f:
                try:
                    memory.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return memory

if __name__ == "__main__":
    mem = AgentMemory()
    mem.log_agent_result({"agent_id": 0, "result": "test"})
    print("Agent memory:", mem.load_memory())
