# 📊 Observability

Documentation for MultiProdigy's monitoring and observability features.

## 📁 Contents

- [📊 User Guide](user_guide.md) - Complete dashboard and monitoring guide
- [📈 Graph Visualization](graph_visualization.md) - Network graph features
- [🔍 Feature Specification](feature_spec.md) - Technical specifications
- [📝 Logging Research](logging_research.md) - Logging approaches and research
- [🔗 LangSmith Features](langsmith_features.md) - LangSmith integration

## 🚀 Quick Start

### Access the Dashboard
```bash
# Run any demo to start the dashboard
python demo/run_working_demo.py

# Open browser: http://localhost:5000
```

### Key Features
- **Real-time monitoring** of agent communications
- **Interactive network graph** visualization
- **Performance metrics** and error tracking
- **Message history** with search and filtering
- **Agent statistics** and health monitoring

## 📊 Dashboard Views

- **Main Dashboard** (`/`) - Live agent activity and metrics
- **Network Graph** (`/network`) - Interactive agent communication visualization
- **Agents View** (`/agents`) - Detailed agent statistics
- **Messages View** (`/messages`) - Complete message history
- **Metrics View** (`/metrics`) - Performance dashboards

## 🔧 Configuration

```python
from MultiProdigy.observability.manager import ObservabilityManager

# Basic setup (automatic in demos)
obs = ObservabilityManager()
obs.start_dashboard(port=5000)

# Custom configuration
config = ObservabilityConfig(
    dashboard_port=8080,
    enable_metrics=True,
    log_level="INFO"
)
obs = ObservabilityManager(config)
```

## 🔗 Related

- [Observability Guide](../guides/observability.md) - Development guide
- [Observability API](../api/observability.md) - API reference
- [Agent Development](../guides/agent_development.md) - Building observable agents