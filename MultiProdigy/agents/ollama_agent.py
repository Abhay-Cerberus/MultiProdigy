import shlex
import subprocess  # nosec B404 - subprocess is needed for ollama integration
from MultiProdigy.agents.agent_base import BaseAgent
from MultiProdigy.schemas.schemas import Message

class OllamaAgent(BaseAgent):
    def __init__(self, runtime):
        super().__init__("OllamaAgent", runtime)

    def handle_message(self, message: Message) -> str:
        print(f"[OllamaAgent] Received: {message.content}")

        # Sanitize input to prevent command injection
        safe_content = shlex.quote(message.content)
        command = [
            "ollama",
            "run",
            "tinylama",
            "--quiet",
            "--prompt",
            safe_content
        ]

        try:
            # nosec B603 - command is constructed safely with shlex.quote
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30,  # Add timeout for security
                check=False  # Don't raise on non-zero exit
            )
            output = result.stdout.strip()

            if not output:
                output = "[OllamaAgent] No output from ollama subprocess"

            print(f"[OllamaAgent] Output: {output}")
            return output

        except subprocess.TimeoutExpired:
            error_msg = "[OllamaAgent] Timeout: ollama command took too long"
            print(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"[OllamaAgent] Exception: {str(e)}"
            print(error_msg)
            return error_msg

