# 📊 Observability API Reference

## ObservabilityManager Class

Central manager for observability features.

### Constructor

```python
ObservabilityManager(config: ObservabilityConfig = None)
```

### Methods

#### `start_dashboard(port: int = 5000)`
Start the observability dashboard.

**Parameters:**
- `port` (int): Dashboard port (default: 5000)

#### `log_message(sender: str, recipient: str, content: str)`
Log a message interaction.

**Parameters:**
- `sender` (str): Sender agent name
- `recipient` (str): Recipient agent name
- `content` (str): Message content

#### `get_metrics() -> Dict`
Get current system metrics.

**Returns:** Dictionary with performance metrics

#### `get_agent_stats(agent_name: str) -> Dict`
Get statistics for a specific agent.

**Parameters:**
- `agent_name` (str): Agent name

**Returns:** Dictionary with agent statistics

## Dashboard API

### Endpoints

#### `GET /api/agents`
Get list of all agents and their status.

#### `GET /api/messages`
Get recent message history.

#### `GET /api/metrics`
Get system performance metrics.

#### `GET /api/network`
Get network graph data for visualization.

## Example Usage

```python
from MultiProdigy.observability.manager import ObservabilityManager

# Create observability manager
obs = ObservabilityManager()

# Start dashboard
obs.start_dashboard(port=5000)

# Log custom event
obs.log_message("Agent1", "Agent2", "Custom message")

# Get metrics
metrics = obs.get_metrics()
print(f"Total messages: {metrics['total_messages']}")
```

## Related

- [Observability Guide](../guides/observability.md)
- [Observability Features](../observability/)
- [Dashboard User Guide](../observability/user_guide.md)