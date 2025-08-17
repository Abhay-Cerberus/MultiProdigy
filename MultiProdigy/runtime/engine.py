from MultiProdigy.agents.ollama_agent import OllamaAgent
from MultiProdigy.agents.echo_agent import EchoAgent
from MultiProdigy.bus.message_bus import MessageBus
from MultiProdigy.logging_custom import setup_logger
from MultiProdigy.config import settings


class RuntimeEngine:
    def __init__(self):
        # Logger setup
        self.logger = setup_logger(self.__class__.__name__)
        self.logger.info("Initializing Runtime Engine...")

        # Message bus init
        self.bus = MessageBus()

        # Agents registry
        self.agents = {}

        # Load agents based on settings
        self._load_agents()

    def _load_agents(self):
        try:
            if settings.enable_ollama_agent:
                self.agents["ollama_agent"] = OllamaAgent(message_bus=self.bus)
                self.logger.info("OllamaAgent loaded successfully.")

            if settings.enable_echo_agent:
                self.agents["echo_agent"] = EchoAgent(message_bus=self.bus)
                self.logger.info("EchoAgent loaded successfully.")

            # Subscribe all agents to the bus
            for name, agent in self.agents.items():
                self.bus.subscribe(name, agent.handle_message)

            self.logger.info(f"Loaded agents: {list(self.agents.keys())}")

        except Exception as e:
            self.logger.error(f"Error loading agents: {e}")

    def send_message(self, agent_name: str, message: dict):
        """Send a message to the message bus."""
        self.logger.debug(f"Sending message to {agent_name}: {message}")
        self.bus.publish(agent_name, message)


if __name__ == "__main__":
    engine = RuntimeEngine()
