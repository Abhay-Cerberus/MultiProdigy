# 🚀 MultiProdigy Complete Setup & Run Guide

## ⚡ Super Quick Start (1 Command)

```bash
python demo/run_working_demo.py
```

That's it! This single command will:
- ✅ Check and install missing dependencies automatically
- ✅ Set up Python paths correctly
- ✅ Start the working demo with real LLM responses
- ✅ Launch the web dashboard at http://localhost:5000
- ✅ Show actual AI responses from Gemini, OpenAI, or other providers

## 🎯 What You'll See

When you run `python demo/run_working_demo.py`, you'll get:

```
🚀 MultiProdigy Observability Demo Launcher
==================================================
📦 Loading MultiProdigy components...
✅ All components loaded successfully!
🎬 Starting demo...

🚀 Starting MultiProdigy Observability Demo
==================================================
✅ Created demo agents:
   - UserAgent
   - TaskManagerAgent
   - WorkerAgent

🌐 Dashboard starting at http://localhost:5000
📊 Graph view at http://localhost:5000/static/graph.html

🎬 Starting agent activity simulation...
   (This will run for 60 seconds)

[UserAgent] Sending: Process task #1
[TaskManagerAgent] Processing: Process task #1
[TaskManagerAgent] Completed: Process task #1
```

## 🌐 Web Interfaces

Once running, open these URLs in your browser:

### 📊 Main Dashboard: http://localhost:5000
- **Live Metrics**: Message count, processing times, error rates
- **Agent Timeline**: Real-time chronological view of all interactions
- **Auto-refresh**: Updates every 5 seconds
- **Error Tracking**: Highlights failed operations in red

### 🕸️ Network Graph: http://localhost:5000/static/graph.html
- **Interactive Visualization**: Drag nodes, zoom, pan
- **Real-time Updates**: Live graph updates as agents communicate
- **Status Colors**:
  - 🟢 **Green** = Active agent (recently processed messages)
  - 🟡 **Yellow** = Currently processing a message
  - 🔴 **Red** = Recent error occurred
  - ⚫ **Gray** = Idle (no recent activity)
- **Message Flow**: Arrows show communication direction
- **Node Details**: Click nodes for detailed information

## 🔧 Alternative Methods

### Method 1: Manual Dependency Installation
```bash
pip install flask pydantic aiohttp
python demo/run_working_demo.py
```

### Method 2: Direct Demo Run
```bash
# From the project root directory
python demo/working_demo.py
```

### Method 3: Other Demos
```bash
# Observability-only demo
python demo/run_observability_demo.py

# LLM system testing
python demo/run_llm_demo.py

# Quick system test
python demo/test_llm_quick.py
```

## 🛠️ Custom Agent Development

Create your own agents with automatic observability:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from MultiProdigy.agents.agent_base import BaseAgent
from MultiProdigy.bus.message_bus import MessageBus
from MultiProdigy.observability.dashboard import ObservabilityDashboard
import threading

class MyCustomAgent(BaseAgent):
    def on_message(self, message):
        print(f"[{self.name}] Processing: {message.content}")
        # Your custom logic here
        return f"Processed: {message.content}"

# Setup
bus = MessageBus()
agent1 = MyCustomAgent("Agent1", bus)
agent2 = MyCustomAgent("Agent2", bus)

bus.register(agent1)
bus.register(agent2)

# Start observability dashboard
dashboard = ObservabilityDashboard()
threading.Thread(target=dashboard.run, daemon=True).start()

# Send messages (automatically traced!)
agent1.send("Hello from Agent1", "Agent2")
agent2.send("Hello back!", "Agent1")

input("Press Enter to exit...")
```

## 🔍 Troubleshooting

### Common Issues & Solutions

**❌ "No module named 'MultiProdigy'"**
- **Solution**: Make sure you're in the project root directory
- **Check**: Run `ls` and verify you see the `MultiProdigy/` folder

**❌ "Dashboard shows no data"**
- **Solution**: Wait 10-15 seconds for agents to start communicating
- **Check**: Look for `agent_traces.jsonl` file in your directory
- **Fix**: Refresh the browser page

**❌ "Graph visualization is empty"**
- **Solution**: Agents need to send at least one message first
- **Check**: Console output should show "[Agent] Sending:" messages
- **Fix**: Wait for the demo to start sending messages

**❌ "Port 5000 already in use"**
- **Solution**: Kill the process using port 5000 or change the port
- **Windows**: `netstat -ano | findstr :5000` then `taskkill /PID <PID> /F`
- **Mac/Linux**: `lsof -ti:5000 | xargs kill -9`

**❌ "Flask not available"**
- **Solution**: The `run_demo.py` should auto-install it, but if not:
```bash
pip install flask
python run_demo.py
```

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
# Then run your script
```

## 📁 Project Structure

```
MultiProdigy/
├── agents/
│   ├── agent_base.py          # ✅ Base agent with automatic tracing
│   └── ...
├── bus/
│   └── message_bus.py         # ✅ Message routing system
├── observability/             # ✅ Complete observability suite
│   ├── tracer.py              # Core tracing and logging
│   ├── dashboard.py           # Web dashboard backend
│   ├── graph_builder.py       # Graph data generator
│   └── static/
│       └── graph.html         # Interactive D3.js visualization
├── schemas/
│   └── message.py             # Message format definitions
└── ...

demo/
└── observability_demo.py      # ✅ Complete working demo

run_demo.py                     # ✅ Smart launcher script
```

## 🎯 Key Features You Get

### ✅ **Zero Configuration Observability**
- Every agent interaction is automatically logged
- No code changes needed for basic tracing
- Works out of the box with any BaseAgent

### ✅ **Real-time Monitoring**
- Live web dashboard with metrics and timeline
- Interactive network graph showing agent relationships
- Automatic error detection and highlighting

### ✅ **LangSmith-inspired Interface**
- Timeline view of agent interactions
- Trace inspection and debugging
- Performance metrics and error tracking

### ✅ **LangGraph-style Visualization**
- Interactive network graph of agent communications
- Real-time updates as messages flow
- Drag, zoom, and explore agent relationships

## 🚀 Advanced Usage

### Custom Tracing
Add your own trace points:
```python
from MultiProdigy.observability.tracer import tracer

def my_complex_function():
    trace_id = tracer.start_trace("MyAgent", "custom_processing")
    try:
        # Your logic here
        result = do_something()
        tracer.end_trace(trace_id, result={"success": True})
        return result
    except Exception as e:
        tracer.end_trace(trace_id, error=str(e))
        raise
```

### Export Data
```python
from MultiProdigy.observability.dashboard import ObservabilityDashboard

dashboard = ObservabilityDashboard()
traces = dashboard._load_traces()

# Export to JSON, CSV, send to external monitoring, etc.
import json
with open('agent_traces_export.json', 'w') as f:
    json.dump(traces, f, indent=2)
```

### API Access
Access raw data programmatically:
- `GET http://localhost:5000/api/traces` - All trace data
- `GET http://localhost:5000/api/timeline` - Timeline events
- `GET http://localhost:5000/api/metrics` - Performance metrics
- `GET http://localhost:5000/api/graph` - Graph visualization data

## 🎉 Next Steps

1. **Run the working demo**: `python demo/run_working_demo.py`
2. **Explore the interfaces**: Open both the dashboard and graph views
3. **Watch real LLM responses**: See actual AI responses from Gemini/OpenAI
4. **Build your own agents**: Use the custom agent example above
5. **Check the documentation**: Explore `docs/observability/` and `demo/README.md`

## 💡 Pro Tips

- **Provide API keys**: Get real AI responses by setting GEMINI_API_KEY or OPENAI_API_KEY
- **Try different demos**: Each demo in `demo/` showcases different features
- **Explore interactivity**: Click nodes, drag them around, zoom in/out
- **Check the timeline**: See the chronological flow of all agent interactions
- **Monitor performance**: Watch the metrics update in real-time

## 🎯 Available Demos

- **🎯 Working Demo**: `python demo/run_working_demo.py` - Shows real LLM responses (recommended)
- **📊 Observability Demo**: `python demo/run_observability_demo.py` - Dashboard and monitoring
- **🤖 LLM System Demo**: `python demo/run_llm_demo.py` - Tests all LLM providers
- **⚡ Quick Test**: `python demo/test_llm_quick.py` - Verify system setup

---

**Ready to start?** Just run:
```bash
python demo/run_working_demo.py
```

And open http://localhost:5000 in your browser! 🎉