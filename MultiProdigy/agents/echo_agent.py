from MultiProdigy.agents.agent_base import AgentBase

class EchoAgent(AgentBase):  
    def __init__(self, message_bus=None):
     super().__init__("EchoAgent")
     self.message_bus = message_bus
     self.logger.info("Echo agent ready for message processing")

    def handle_message(self, message):
        """Required for MessageBus subscription"""
        return self.process_message(message)

    def process_message(self, message):
        self.logger.debug(
            f"Received message for processing",
            {
                'message_length': len(message),
                'message_type': type(message).__name__
            }
        )
        try:
            echo_response = f"Echo: {message}"
            self.logger.info(
                f"Message echoed successfully",
                {
                    'original_length': len(message),
                    'echo_length': len(echo_response)
                }
            )
            return echo_response
        except Exception as e:
            self.logger.error(
                f"Echo processing failed",
                {
                    'message': message,
                    'error': str(e)
                }
            )
            raise
