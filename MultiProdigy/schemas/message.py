from pydantic import BaseModel
from typing import Any, Optional, Dict

class Message(BaseModel):
    """
    A standard message format for communication between agents via the MessageBus.
    """

    sender: str                     # Name or ID of the sending agent
    recipient: str                  # Name or ID of the recipient agent
    content: Any                     # Actual payload (text, dict, object, etc.)
    type: Optional[str] = "text"     # Type of message: 'text', 'command', 'data', etc.
    metadata: Optional[Dict[str, Any]] = None  # Additional info (timestamp, tags, etc.)
