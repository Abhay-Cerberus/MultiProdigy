# 🚌 Message Bus API Reference

## MessageBus Class

Central communication hub for all agents.

### Constructor

```python
MessageBus()
```

### Methods

#### `register(agent: BaseAgent)`
Register an agent with the message bus.

**Parameters:**
- `agent` (BaseAgent): Agent instance to register

#### `unregister(agent_name: str)`
Remove an agent from the message bus.

**Parameters:**
- `agent_name` (str): Name of agent to remove

#### `send_message(sender: str, recipient: str, content: str)`
Send a message between agents.

**Parameters:**
- `sender` (str): Sender agent name
- `recipient` (str): Recipient agent name
- `content` (str): Message content

#### `broadcast_message(sender: str, content: str)`
Send a message to all registered agents.

**Parameters:**
- `sender` (str): Sender agent name
- `content` (str): Message content

### Properties

- `agents` (Dict[str, BaseAgent]): Registered agents
- `message_count` (int): Total messages processed
- `is_active` (bool): Bus status

## Example Usage

```python
from MultiProdigy.bus.message_bus import MessageBus
from MultiProdigy.agents.agent_base import BaseAgent

# Create bus
bus = MessageBus()

# Create and register agents
agent1 = BaseAgent("Agent1", bus)
agent2 = BaseAgent("Agent2", bus)

bus.register(agent1)
bus.register(agent2)

# Send message
bus.send_message("Agent1", "Agent2", "Hello!")
```

## Related

- [Agents API](agents.md)
- [Message Schema](../schemas/message.md)
- [Observability API](observability.md)