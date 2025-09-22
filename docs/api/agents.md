# 🤖 Agents API Reference

## BaseAgent Class

The core agent class that all agents inherit from.

### Constructor

```python
BaseAgent(name: str, bus: MessageBus)
```

**Parameters:**
- `name` (str): Unique agent identifier
- `bus` (MessageBus): Message bus instance

### Methods

#### `on_message(message: Message)`
Override this method to handle incoming messages.

**Parameters:**
- `message` (Message): Incoming message object

#### `send(content: str, recipient: str)`
Send a message to another agent.

**Parameters:**
- `content` (str): Message content
- `recipient` (str): Target agent name

#### `broadcast(content: str)`
Send a message to all registered agents.

**Parameters:**
- `content` (str): Message content

### Properties

- `name` (str): Agent name
- `bus` (MessageBus): Message bus reference
- `is_active` (bool): Agent status

## Example Usage

```python
from MultiProdigy.agents.agent_base import BaseAgent

class EchoAgent(BaseAgent):
    def on_message(self, message):
        echo = f"Echo: {message.content}"
        self.send(echo, message.sender)
```

## Related

- [Agent Development Guide](../guides/agent_development.md)
- [Message Bus API](message_bus.md)
- [Message Schema](../schemas/message.md)