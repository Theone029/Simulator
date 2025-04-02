from human_signal_mapper import HumanSignalMapper
from llm_arbitrator import LLMArbitrator
from recursive_interface import RecursiveInterface

def main():
    # Test HumanSignalMapper
    mapper = HumanSignalMapper()
    message = "I observed a significant ERROR in the latest update."
    update = mapper.map_message(message)
    print("HumanSignalMapper update:", update)

    # Test LLMArbitrator
    arbitrator = LLMArbitrator()
    suggestion = arbitrator.interpret(update)
    print("LLMArbitrator suggestion:", suggestion)

    # Test RecursiveInterface
    interface = RecursiveInterface()
    beliefs = {"learning_rate": 0.001, "strategy": "conservative"}
    text = interface.beliefs_to_text(beliefs)
    print("Beliefs as text:\n", text)
    recovered = interface.text_to_beliefs(text)
    print("Recovered beliefs:", recovered)

if __name__ == "__main__":
    main()
