# 🚀 Getting Started with MultiProdigy

## ⚡ Quick Start (30 seconds)

### 1. Install Dependencies
```bash
pip install flask pydantic aiohttp
```

### 2. Run the Working Demo
```bash
python demo/run_working_demo.py
```

### 3. Open the Dashboard
Visit http://localhost:5000 to see real-time agent monitoring!

---

## 🎯 What You'll Experience

### **Real LLM Integration**
- Provide your Gemini API key to see actual AI responses
- Fallback to mock AI if no API key provided
- Support for OpenAI, Anthropic, Ollama, HuggingFace

### **Live Observability**
- Real-time dashboard showing agent communications
- Interactive network graph visualization
- Performance metrics and error tracking

### **Multi-Agent Communication**
- Agents automatically communicate through message bus
- All interactions are traced and logged
- Zero configuration required

---

## 🔧 Custom Agent Development

### Basic Agent Example
```python
from MultiProdigy.agents.agent_base import BaseAgent
from MultiProdigy.bus.message_bus import MessageBus
from MultiProdigy.schemas.message import Message

class MyAgent(BaseAgent):
    def on_message(self, message: Message):
        print(f"[{self.name}] Received: {message.content}")
        # Your custom logic here
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
        # Initialize LLM client
        if api_key:
            self.llm = LLMFactory.create_gemini("gemini-2.0-flash-exp", api_key)
        else:
            self.llm = LLMFactory.create_mock()
    
    def on_message(self, message: Message):
        # Use LLM to generate intelligent response
        prompt = f"Please respond to: {message.content}"
        response = asyncio.run(self.llm.generate(prompt))
        self.send(response.content, message.sender)
```

---

## 🎯 Available Demos

### **🎯 Working Demo** (Recommended)
```bash
python demo/run_working_demo.py
```
- Shows real LLM responses with proper async handling
- Tests multiple providers (Gemini, OpenAI, Mock)
- Includes observability dashboard

### **📊 Observability Demo**
```bash
python demo/run_observability_demo.py
```
- Focuses on monitoring and visualization features
- Real-time dashboard and network graph
- Agent communication tracing

### **🤖 LLM System Demo**
```bash
python demo/run_llm_demo.py
```
- Tests all LLM providers systematically
- Shows configuration flexibility
- Provider comparison and benchmarking

### **⚡ Quick Test**
```bash
python demo/test_llm_quick.py
```
- Verify system setup and dependencies
- Quick LLM connectivity test

---

## 🔑 API Key Setup

### Environment Variables (Recommended)
```bash
export GEMINI_API_KEY="your-gemini-api-key"
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

### Get API Keys
- **Gemini**: https://makersuite.google.com/app/apikey
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/

---

## 📌 Key Concepts

### **Agents**
- Inherit from `BaseAgent`
- Implement `on_message(message)` method
- Automatically get observability tracing
- Can use LLM clients for AI-powered responses

### **Message Bus**
- Central communication hub for all agents
- Automatic message routing by agent name
- Built-in observability and logging
- Supports both sync and async operations

### **LLM Integration**
- Unified interface for all AI providers
- Pydantic-based configuration
- Automatic error handling and fallbacks
- Consistent response format

### **Observability**
- Zero-configuration monitoring
- Real-time dashboard and visualization
- Structured logging and tracing
- Performance metrics and error tracking

---

## 🚀 Next Steps

1. **Run the working demo** to see everything in action
2. **Explore the web dashboard** at http://localhost:5000
3. **Check out the network graph** visualization
4. **Build your own agents** using the examples above
5. **Read the detailed guides** in `docs/` and `demo/README.md`

---

## 🔍 Troubleshooting

### Common Issues
- **"No module named 'MultiProdigy'"**: Run from project root directory
- **"No LLM responses"**: Check API keys or use mock provider
- **"Dashboard empty"**: Wait for agents to communicate, then refresh

### Getting Help
- Check `demo/README.md` for detailed demo information
- See `docs/observability/user_guide.md` for monitoring features
- Review `RUN_GUIDE.md` for comprehensive setup instructions

**Ready to build intelligent agents?** Start with:
```bash
python demo/run_working_demo.py
```
