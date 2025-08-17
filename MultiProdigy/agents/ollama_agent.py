import subprocess
from MultiProdigy.agents.agent_base import AgentBase
from MultiProdigy.schemas.schemas import Message

from MultiProdigy.logging_custom.logger import setup_logger


logger = setup_logger("OllamaAgent")

class OllamaAgent(AgentBase):

    def __init__(self, runtime):
        super().__init__("OllamaAgent", runtime)

    def handle_message(self, message: Message) -> str:
        print(f"[OllamaAgent] Received: {message.content}")

        command = [
            "ollama",
            "run",
            "tinylama",
            "--quiet",
            "--prompt",
            message.content
        ]

        try:
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',    # fix here: specify utf-8 decoding
                errors='replace'     # replace undecodable chars instead of crashing
            )
            output = result.stdout.strip()

            if not output:
                output = "[OllamaAgent] No output from ollama subprocess"

            print(f"[OllamaAgent] Output: {output}")
            return output

        except Exception as e:
            error_msg = f"[OllamaAgent] Exception: {str(e)}"
            print(error_msg)
            return error_msg
        
class OllamaAgent:
    def __init__(self, message_bus, model_name="mistral"):
        self.message_bus = message_bus
        self.model_name = model_name

    def handle_message(self, message):
        logger.info(f"Received message: {message}")

        # Example Ollama call (pseudo code)
        response = {"ollama_output": f"Processed with {self.model_name}"}

        logger.info(f"Sending response: {response}")
        self.message_bus.publish("TargetAgentName", response)
