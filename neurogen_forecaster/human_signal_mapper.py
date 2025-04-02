import json

class HumanSignalMapper:
    """
    Maps human interactions into symbolic updates.
    For demo, converts a human message into a simple update dict.
    """
    def map_message(self, message):
        # Simple mapping: if "error" in message, flag for reduction.
        update = {"reduce_error": "error" in message.lower(), "message": message}
        return update

if __name__ == "__main__":
    mapper = HumanSignalMapper()
    print("Mapping result:", mapper.map_message("There is an ERROR in the system"))
