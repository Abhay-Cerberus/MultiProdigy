# 🔌 API Reference

Complete API documentation for MultiProdigy components.

## 📁 API Documentation

- [🤖 Agents API](agents.md) - Agent classes and methods
- [🚌 Message Bus API](message_bus.md) - Communication system
- [🧠 LLM API](llm.md) - Language model integration
- [📊 Observability API](observability.md) - Monitoring and tracing

## 🚀 Quick Reference

### Core Classes
```python
from MultiProdigy.agents.agent_base import BaseAgent
from MultiProdigy.bus.message_bus import MessageBus
from MultiProdigy.llm.factory import LLMFactory
from MultiProdigy.schemas.message import Message
```

### Basic Usage
```python
# Create message bus
bus = MessageBus()

# Create agent
agent = BaseAgent("MyAgent", bus)

# Register agent
bus.register(agent)

# Send message
agent.send("Hello", "TargetAgent")
```

## 🔗 Related Documentation

- [Development Guides](../guides/) - How-to guides
- [Examples](../../demo/) - Working examples
- [Architecture](../architecture.md) - System overview