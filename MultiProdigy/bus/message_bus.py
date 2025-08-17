import asyncio
import logging
from typing import Dict, Any, Callable, List, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid

from MultiProdigy.monitor.log_collector import log_collector

@dataclass
class Message:
    """Represents a message in the system"""
    id: str
    sender: str
    receiver: str
    content: Any
    message_type: str
    timestamp: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class MessageBus:
    """Central message bus for agent communication"""
    
    def __init__(self):
        self.logger = logging.getLogger("MessageBus")
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_history: List[Message] = []
        
    def subscribe(self, message_type: str, callback: Callable):
        """Subscribe to a message type"""
        if message_type not in self.subscribers:
            self.subscribers[message_type] = []
        self.subscribers[message_type].append(callback)
        self.logger.info(f"Subscriber registered for message type: {message_type}")
    
    def unsubscribe(self, message_type: str, callback: Callable):
        """Unsubscribe from a message type"""
        if message_type in self.subscribers:
            try:
                self.subscribers[message_type].remove(callback)
                self.logger.info(f"Subscriber removed for message type: {message_type}")
            except ValueError:
                self.logger.warning(f"Callback not found for message type: {message_type}")
    
    def publish(self, sender: str, receiver: str, content: Any, 
                message_type: str = "general", metadata: Dict[str, Any] = None) -> str:
        """Publish a message to the bus"""
        
        message = Message(
            id=str(uuid.uuid4()),
            sender=sender,
            receiver=receiver,
            content=content,
            message_type=message_type,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        
        # Store in history
        self.message_history.append(message)
        
        # Log the message
        self.logger.info(f"Message published: {sender} -> {receiver} ({message_type})", 
                        extra={
                            'sender': sender,
                            'receiver': receiver,
                            'message_type': message_type,
                            'message_id': message.id,
                            'content_preview': str(content)[:100]
                        })
        
        # Notify subscribers
        if message_type in self.subscribers:
            for callback in self.subscribers[message_type]:
                try:
                    callback(message)
                except Exception as e:
                    self.logger.error(f"Error in message callback: {e}")
        
        return message.id
    
    def get_message_history(self, limit: int = 100) -> List[Message]:
        """Get recent message history"""
        return self.message_history[-limit:]
    
    def get_messages_for_agent(self, agent_name: str, limit: int = 50) -> List[Message]:
        """Get messages sent to or from a specific agent"""
        return [msg for msg in self.message_history[-limit*2:] 
                if msg.sender == agent_name or msg.receiver == agent_name][-limit:]
    
    def clear_history(self):
        """Clear message history"""
        self.message_history.clear()
        self.logger.info("Message history cleared")

# Global message bus instance
message_bus = MessageBus()