# MultiProdigy Observability User Guide

## Quick Start

### 1. Enable Observability in Your Agents

The observability system is automatically enabled when you use `BaseAgent`. No additional setup required!

```python
from MultiProdigy.agents.agent_base import BaseAgent
from MultiProdigy.bus.message_bus import MessageBus

# Your agents automatically get tracing
class MyAgent(BaseAgent):
    def on_message(self, message):
        # This will be automatically traced
        return f"Processed: {message.content}"

# Usage
bus = MessageBus()
agent = MyAgent("MyAgent", bus)
```

### 2. Start the Observability Dashboard

```python
from MultiProdigy.observability.dashboard import ObservabilityDashboard

# Start the dashboard server
dashboard = ObservabilityDashboard()
dashboard.run(host='localhost', port=5000)
```

Then open http://localhost:5000 in your browser.

### 3. View the Agent Network Graph

Open the graph visualization at http://localhost:5000/static/graph.html

## Features Overview

### 📊 Dashboard Features

**Timeline View**: See chronological flow of agent messages
- Message sending and receiving events
- Processing duration for each agent
- Error tracking and status indicators

**Metrics Panel**: Key performance indicators
- Total messages processed
- Average processing duration
- Error rates and counts
- Active agent status

**Trace Details**: Drill down into specific interactions
- Individual message content
- Processing metadata
- Error details and stack traces

### 🕸️ Network Graph Features

**Interactive Visualization**: 
- Drag nodes to rearrange the graph
- Zoom and pan for large networks
- Click nodes for detailed information

**Real-time Updates**:
- Live graph updates every 5 seconds
- Animation of message flows
- Status color coding (active, processing, error, idle)

**Agent Status Indicators**:
- 🟢 Active: Recently processed messages
- 🟡 Processing: Currently handling a message
- 🔴 Error: Recent error occurred
- ⚫ Idle: No recent activity

## Configuration Options

### Custom Log File Location

```python
from MultiProdigy.observability.tracer import AgentTracer

# Use custom log file
tracer = AgentTracer(log_file="my_custom_traces.jsonl")
```

### Dashboard Configuration

```python
from MultiProdigy.observability.dashboard import ObservabilityDashboard

# Custom configuration
dashboard = ObservabilityDashboard(log_file="my_custom_traces.jsonl")
dashboard.run(host='0.0.0.0', port=8080, debug=False)
```

### Graph Time Window

```python
from MultiProdigy.observability.graph_builder import AgentGraphBuilder

builder = AgentGraphBuilder()
# Show only last 30 minutes of activity
graph_data = builder.build_graph_data(time_window_minutes=30)
```

## Advanced Usage

### Custom Tracing

Add custom trace points in your agent logic:

```python
from MultiProdigy.observability.tracer import tracer

class MyAgent(BaseAgent):
    def on_message(self, message):
        # Start custom trace
        trace_id = tracer.start_trace(
            agent_name=self.name,
            event_type="custom_processing",
            metadata={"input_type": type(message.content).__name__}
        )
        
        try:
            # Your processing logic
            result = self.complex_processing(message.content)
            
            # End trace with success
            tracer.end_trace(trace_id, result={"output_length": len(result)})
            return result
            
        except Exception as e:
            # End trace with error
            tracer.end_trace(trace_id, error=str(e))
            raise
```

### Filtering and Search

The dashboard supports URL parameters for filtering:

```
http://localhost:5000/api/traces?agent=TaskManager
http://localhost:5000/api/timeline?status=error
http://localhost:5000/api/metrics?time_window=3600
```

### Export Data

Access raw trace data programmatically:

```python
from MultiProdigy.observability.dashboard import ObservabilityDashboard

dashboard = ObservabilityDashboard()
traces = dashboard._load_traces()

# Export to CSV, send to external monitoring, etc.
```

## Troubleshooting

### Common Issues

**Dashboard shows no data**:
- Ensure agents are sending messages (traces are only created during activity)
- Check that the log file path is correct
- Verify agents are using the instrumented `BaseAgent`

**Graph visualization is empty**:
- Make sure agents have communicated recently (default 60-minute window)
- Check browser console for JavaScript errors
- Verify the `/api/graph` endpoint returns data

**Performance issues**:
- Large log files can slow down the dashboard
- Consider rotating log files or filtering by time window
- Disable animation in the graph for better performance

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from MultiProdigy.observability.dashboard import ObservabilityDashboard
dashboard = ObservabilityDashboard()
dashboard.run(debug=True)
```

### Log File Format

Traces are stored in JSONL format (one JSON object per line):

```json
{"trace_id": "abc123", "timestamp": "2025-01-22T10:30:00Z", "event_type": "message_sent", "sender": "UserAgent", "receiver": "TaskManager", "content_preview": "Hello"}
{"trace_id": "def456", "agent_name": "TaskManager", "event_type": "message_received", "start_time": "2025-01-22T10:30:01Z", "duration_ms": 150, "status": "completed"}
```

## Integration with External Tools

### Prometheus Metrics

Export metrics to Prometheus:

```python
from prometheus_client import Counter, Histogram, start_http_server

# Custom metrics
message_counter = Counter('multiprodigy_messages_total', 'Total messages', ['sender', 'receiver'])
processing_time = Histogram('multiprodigy_processing_seconds', 'Processing time', ['agent'])

# Start Prometheus metrics server
start_http_server(8000)
```

### ELK Stack Integration

Forward logs to Elasticsearch:

```python
import json
from elasticsearch import Elasticsearch

es = Elasticsearch(['localhost:9200'])

def forward_to_elk(trace_data):
    es.index(index='multiprodigy-traces', body=trace_data)
```

### Grafana Dashboards

Create Grafana dashboards using the metrics API:
- Configure Prometheus as data source
- Import MultiProdigy dashboard templates
- Set up alerts for error rates and performance thresholds

## Best Practices

1. **Monitor Resource Usage**: Observability adds ~5% overhead
2. **Rotate Log Files**: Prevent disk space issues with large deployments
3. **Use Time Windows**: Filter data for better performance
4. **Custom Metrics**: Add domain-specific tracing for your use case
5. **Error Handling**: Always handle tracing errors gracefully

## API Reference

### Tracer Methods

- `start_trace(agent_name, event_type, metadata=None)` → trace_id
- `end_trace(trace_id, result=None, error=None)` → None
- `log_message_event(sender, receiver, content, message_id=None)` → message_id

### Dashboard Endpoints

- `GET /api/traces` - List all traces
- `GET /api/traces/<trace_id>` - Get trace details
- `GET /api/timeline` - Timeline view data
- `GET /api/metrics` - Performance metrics
- `GET /api/graph` - Graph visualization data

### Graph Builder Methods

- `build_graph_data(time_window_minutes=60)` → graph_data
- `get_agent_details(agent_name)` → agent_details