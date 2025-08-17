from MultiProdigy.agents.agent_base import AgentBase  # Fix import
from MultiProdigy.logging_custom.logger import setup_logger

logger = setup_logger("memory_agent")

class MemoryAgent(AgentBase):  # Fix base class
    def __init__(self, runtime=None):
        super().__init__("MemoryAgent")  # Fix initialization
        self.memory = []
        self.runtime = runtime

    def handle_message(self, message):
        """Required for MessageBus subscription"""
        logger.info(f"Received: {message}")
        content = message.get('content', str(message)) if isinstance(message, dict) else str(message)
        self.memory.append(content)
        logger.info(f"Memory stored. Total items: {len(self.memory)}")
        return {"status": "stored", "memory_size": len(self.memory)}