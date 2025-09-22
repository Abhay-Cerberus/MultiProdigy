# 🤖 Agent Development Guide

## Overview

This guide covers building custom agents in MultiProdigy.

## Basic Agent Structure

```python
from MultiProdigy.agents.agent_base import BaseAgent
from MultiProdigy.schemas.message import Message

class MyAgent(BaseAgent):
    def on_message(self, message: Message):
        # Your agent logic here
        response = f"Processed: {message.content}"
        self.send(response, message.sender)
```

## Advanced Topics

- **LLM Integration**: See [LLM Integration Guide](llm_integration.md)
- **Observability**: See [Observability Guide](observability.md)
- **API Reference**: See [Agents API](../api/agents.md)

## Examples

For working examples, see the [demo directory](../../demo/).

---

**Next Steps**: [LLM Integration](llm_integration.md) | [API Reference](../api/agents.md)