class MessageBus:
    def __init__(self):
        self.agents = {}

    def register(self, agent):
        """Register an agent so it can receive messages."""
        self.agents[agent.name] = agent
        print(f"[Bus] Agent registered: {agent.name}")

    def publish(self, message):
        """Deliver a message to the correct agent."""
        receiver = message.receiver
        if receiver in self.agents:
            self.agents[receiver].handle_message(message)
        else:
            print(f"[Bus] No agent found with name: {receiver}")

    def send(self, message):
        """Alias for publish to maintain compatibility"""
        self.publish(message)
