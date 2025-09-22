# 📊 Observability Guide

## Overview

This guide covers monitoring and debugging MultiProdigy agents.

## Dashboard

Access the real-time dashboard at `http://localhost:5000` when running demos.

## Features

- **Real-time monitoring** of agent communications
- **Network visualization** of agent interactions
- **Performance metrics** and error tracking
- **Structured logging** and tracing

## Usage

```python
# Observability is automatic - no setup required
from MultiProdigy.agents.agent_base import BaseAgent

class MyAgent(BaseAgent):
    def on_message(self, message):
        # All interactions are automatically traced
        self.send("Response", message.sender)
```

## Advanced Features

For detailed observability documentation, see [Observability](../observability/).

## API Reference

See [Observability API](../api/observability.md) for programmatic access.

---

**Next Steps**: [Plugin Development](plugin_development.md) | [Observability Deep-dive](../observability/)