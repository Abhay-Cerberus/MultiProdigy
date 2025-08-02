# 🎯 MultiProdigy Demo Guide

The `demo/` directory contains comprehensive examples showcasing all aspects of the **MultiProdigy** framework, from basic agent communication to advanced LLM integration with real-time observability.

## 🚀 Available Demos

### **🎯 Working Demo** (Recommended)
- **File**: `working_demo.py`
- **Runner**: `run_working_demo.py`
- **What it shows**: Real LLM responses with proper async handling
- **Features**: 
  - Tests multiple LLM providers (Gemini, OpenAI, Mock, etc.)
  - Shows actual AI responses clearly formatted
  - Includes observability dashboard
  - Fixed all async/sync issues

### **📊 Observability Demo**
- **File**: `observability_demo.py` 
- **Runner**: `run_observability_demo.py`
- **What it shows**: Real-time monitoring and visualization
- **Features**:
  - Live dashboard at http://localhost:5000
  - Interactive network graph visualization
  - Agent communication tracing
  - Performance metrics and error tracking

### **🤖 LLM System Demo**
- **File**: `llm_demo.py`
- **Runner**: `run_llm_demo.py` 
- **What it shows**: Unified LLM architecture testing
- **Features**:
  - Tests all supported LLM providers
  - Configuration flexibility demonstration
  - Provider comparison and benchmarking
  - Agent integration examples

### **🚀 Comprehensive Demo**
- **File**: `comprehensive_demo.py`
- **What it shows**: Full-featured AI-powered agents
- **Features**:
  - AI research agent with Gemini integration
  - Data analysis agent with intelligent responses
  - Project management agent with context awareness
  - Real-time observability and monitoring

## 🎯 Quick Start

### 1. Run the Working Demo
```bash
python demo/run_working_demo.py
```

### 2. Provide API Keys (Optional)
```bash
# Set environment variables for real AI responses
export GEMINI_API_KEY="your-gemini-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

### 3. Open the Dashboard
Visit http://localhost:5000 to see real-time agent monitoring!

## 📋 What You'll Experience

### **Real LLM Integration**
```
================================================================================
📨 RESPONSE #1 FROM SyncLLMAgent
================================================================================
🤖 Gemini 2.0 Flash Response:

Artificial Intelligence (AI) is a branch of computer science that aims to create 
machines capable of performing tasks that typically require human intelligence...
================================================================================
```

### **Live Observability**
- Real-time dashboard showing agent communications
- Interactive network graph visualization  
- Performance metrics and error tracking
- Timeline view of all interactions

### **Multi-Provider Testing**
```
🧪 LLM Provider Test Results:

✅ Mock AI: I understand your request about your query...
✅ Gemini 2.0: Artificial intelligence is the simulation of human intelligence...
❌ OpenAI GPT: API error 401: Incorrect API key provided
⚠️ Ollama: Ollama not found - install from https://ollama.ai

📊 Success Rate: 2/4 providers working
```

## 🔧 Custom Agent Development

### Basic Agent Example
```python
from MultiProdigy.agents.agent_base import BaseAgent
from MultiProdigy.bus.message_bus import MessageBus
from MultiProdigy.schemas.message import Message

class MyAgent(BaseAgent):
    def on_message(self, message: Message):
        print(f"[{self.name}] Received: {message.content}")
        response = f"Processed: {message.content}"
        self.send(response, message.sender)

# Usage
bus = MessageBus()
agent = MyAgent("MyAgent", bus)
bus.register(agent)
```

### LLM-Powered Agent Example
```python
from MultiProdigy.agents.agent_base import BaseAgent
from MultiProdigy.llm.factory import LLMFactory
import asyncio

class AIAgent(BaseAgent):
    def __init__(self, name: str, bus, api_key: str = None):
        super().__init__(name, bus)
        if api_key:
            self.llm = LLMFactory.create_gemini("gemini-2.0-flash-exp", api_key)
        else:
            self.llm = LLMFactory.create_mock()
    
    def on_message(self, message: Message):
        prompt = f"Please respond to: {message.content}"
        response = asyncio.run(self.llm.generate(prompt))
        self.send(response.content, message.sender)
```

## 🌐 Web Interfaces

When running demos with observability:
- **Dashboard**: http://localhost:5000
- **Network Graph**: http://localhost:5000/static/graph.html

## 🔍 Demo Comparison

| Demo | LLM Integration | Observability | Best For |
|------|----------------|---------------|----------|
| **working_demo** | ✅ Real responses | ✅ Dashboard | **First-time users** |
| **observability_demo** | ❌ No LLM | ✅ Full featured | Monitoring features |
| **llm_demo** | ✅ All providers | ❌ No dashboard | LLM testing |
| **comprehensive_demo** | ✅ AI agents | ✅ Dashboard | Advanced users |

## 🚀 Getting Started

1. **Choose your demo** based on what you want to explore
2. **Run the demo** using the provided runner scripts
3. **Explore the web interfaces** for real-time monitoring
4. **Experiment with API keys** to see real AI responses
5. **Build your own agents** using the examples above

## 🔑 API Key Setup

### Get API Keys
- **Gemini**: https://makersuite.google.com/app/apikey (Recommended)
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/

### Set Environment Variables
```bash
export GEMINI_API_KEY="your-gemini-api-key"
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

## 📌 Key Concepts Demonstrated

### **Agent Communication**
- Automatic message routing via `MessageBus`
- Built-in observability and tracing
- Error handling and recovery

### **LLM Integration**
- Unified interface for all AI providers
- Pydantic-based configuration
- Automatic fallbacks and error handling

### **Real-time Monitoring**
- Zero-configuration observability
- Live dashboard and visualization
- Performance metrics and error tracking

## 🎉 Next Steps

1. **Start with the working demo** to see everything in action
2. **Explore the web dashboard** and network visualization
3. **Try different LLM providers** with your API keys
4. **Build custom agents** using the framework
5. **Check the detailed documentation** in `docs/`

**Ready to explore?** Start with:
```bash
python demo/run_working_demo.py
```