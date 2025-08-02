from abc import ABC, abstractmethod
from MultiProdigy.bus.message_bus import MessageBus
from MultiProdigy.schemas.message import Message
from MultiProdigy.observability.tracer import tracer  # Already importing the tracer

class BaseAgent(ABC):
    def __init__(self, name: str, bus: MessageBus):
        self.name = name
        self.bus = bus

    def send(self, content: str, to: str) -> None:
        """Helper to publish a Message to another agent."""
        msg = Message(sender=self.name, receiver=to, content=content)
        
        # Log the message event
        message_id = tracer.log_message_event(
            sender=self.name,
            receiver=to,
            content=content
        )
        msg.metadata["message_id"] = message_id
        
        self.bus.publish(msg)

    def handle_message(self, message: Message) -> None:
        """Handle incoming message with tracing"""
        trace_id = tracer.start_trace(
            agent_name=self.name,
            event_type="message_received",
            metadata={
                "sender": message.sender,
                "message_id": message.metadata.get("message_id"),
                "content_length": len(message.content)
            }
        )

        try:
            result = self.on_message(message)
            tracer.end_trace(trace_id, result={"status": "processed"})
        except Exception as e:
            tracer.end_trace(trace_id, error=str(e))
            raise

    @abstractmethod
    def on_message(self, message: Message) -> None:
        """Called by the bus when a message arrives."""
        ...
