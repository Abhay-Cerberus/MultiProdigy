## 📦 MultiProdigy AI Agents Framework

**MultiProdigy** is a modular, schema-driven, multi-agent framework built with Pydantic. It enables scalable and orchestrated communication between autonomous agents with a shared message bus, runtime engine, and support infrastructure.

------

## ✨ Key Features

- **🤖 Unified LLM Integration**: Support for OpenAI, Gemini, Anthropic, Ollama, HuggingFace with consistent API
- **📊 Real-time Observability**: Dashboard and network visualization for agent monitoring
- **🔧 Plugin-based Architecture**: Modular design with easy extensibility
- **✅ Schema Validation**: Pydantic-based type safety and validation
- **🌐 Multi-Agent Communication**: Scalable message bus for agent coordination
- **📈 Performance Monitoring**: Structured logging and tracing
- **🛡️ Error Handling**: Comprehensive error tracking and recovery

## 🚀 Quick Start

```bash
# Run the working demo with real LLM responses
python demo/run_working_demo.py

# Then open the dashboard
# http://localhost:5000
```

## 📋 Available Demos

- **🎯 Working Demo**: `python demo/run_working_demo.py` - Shows real LLM responses (recommended)
- **📊 Observability Demo**: `python demo/run_observability_demo.py` - Dashboard and monitoring
- **🤖 LLM System Demo**: `python demo/run_llm_demo.py` - Tests all LLM providers
- **⚡ Quick Test**: `python demo/test_llm_quick.py` - Verify system setup

See [demo/README.md](demo/README.md) for detailed demo descriptions.

-------

## 📚 Documentation

- [📚 **Documentation Hub**](docs/README.md) - Complete documentation index
- [🚀 **Getting Started**](docs/getting_started.md) - Quick start guide  
- [🔧 **Installation**](docs/installation.md) - Detailed setup instructions
- [🏗️ **Architecture**](docs/architecture.md) - System design overview
- [🗂️ **API Reference**](docs/modules_reference.md) - Complete module reference
- [🎯 **Demo Guide**](docs/sample_agent_demo.md) - Explore all demos
- [📊 **Observability**](docs/observability/user_guide.md) - Monitoring and debugging 

## 🔑 API Key Setup

To experience real AI responses, set up your API keys:

```bash
# Recommended: Gemini 2.0 Flash (fast and capable)
export GEMINI_API_KEY="your-gemini-api-key"

# Alternative: OpenAI GPT models
export OPENAI_API_KEY="your-openai-api-key"

# Get keys from:
# Gemini: https://makersuite.google.com/app/apikey
# OpenAI: https://platform.openai.com/api-keys
```

## 🎯 What You'll Experience

### **Real AI Responses**
```
🤖 Gemini 2.0 Flash Response:

Artificial Intelligence (AI) is a branch of computer science that aims to create 
machines capable of performing tasks that typically require human intelligence,
such as learning, reasoning, problem-solving, and language understanding...
```

### **Live Monitoring Dashboard**
- Real-time agent communication tracking
- Interactive network graph visualization
- Performance metrics and error monitoring
- Timeline view of all interactions

### **Multi-Provider Support**
- **API Providers**: OpenAI, Gemini, Anthropic
- **Local Models**: Ollama, HuggingFace Transformers
- **Testing**: Mock AI for development
- **Unified Interface**: Same code works with any provider

## 🏗️ Architecture Highlights

- **🤖 Agent-Based**: Modular agents with automatic observability
- **🔄 Message Bus**: Scalable communication with built-in tracing
- **🧠 LLM Integration**: Unified interface for all AI providers
- **📊 Real-time Monitoring**: Zero-config dashboard and visualization
- **✅ Type Safety**: Pydantic models throughout
- **🛡️ Error Handling**: Graceful degradation and recovery

## 🚀 Use Cases

- **🔬 Research**: AI-powered research agents with real-time collaboration
- **📊 Analysis**: Data analysis agents with intelligent insights
- **🤖 Automation**: Task automation with LLM-powered decision making
- **💬 Chatbots**: Multi-agent conversational systems
- **🔍 Monitoring**: Real-time system observability and debugging
- **🧪 Testing**: LLM provider comparison and benchmarking

--------

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

**🎉 Ready to build intelligent agents?** Start with:
```bash
python demo/run_working_demo.py
```
