# 🎯 MultiProdigy Demo Collection

This directory contains all the demos and examples for MultiProdigy. Each demo showcases different aspects of the framework.

## 🚀 **Quick Start - Run the Working Demo**

```bash
# The best demo that actually works and shows real LLM responses
python demo/run_working_demo.py
```

## 📋 **Available Demos**

### **1. Working Demo** ⭐ **RECOMMENDED**
- **File**: `working_demo.py`
- **Runner**: `run_working_demo.py`
- **What it does**: Shows real LLM responses with proper async handling
- **Features**: 
  - Tests multiple LLM providers (Gemini, OpenAI, Mock, etc.)
  - Shows actual AI responses clearly formatted
  - Includes observability dashboard
  - Fixed all async/sync issues

### **2. Observability Demo**
- **File**: `observability_demo.py` 
- **Runner**: `run_observability_demo.py`
- **What it does**: Focuses on the monitoring and visualization features
- **Features**:
  - Real-time dashboard at http://localhost:5000
  - Network graph visualization
  - Agent communication tracing
  - Performance metrics

### **3. LLM System Demo**
- **File**: `llm_demo.py`
- **Runner**: `run_llm_demo.py` 
- **What it does**: Tests the unified LLM architecture
- **Features**:
  - Tests all LLM providers
  - Shows configuration flexibility
  - Demonstrates agent integration
  - Provider comparison

### **4. Comprehensive Demo**
- **File**: `comprehensive_demo.py`
- **What it does**: Full-featured demo with AI-powered agents
- **Features**:
  - AI research agent
  - Data analysis agent  
  - Project management agent
  - Real Gemini API integration

### **5. Quick LLM Test**
- **File**: `test_llm_quick.py`
- **What it does**: Quick test to verify LLM system works
- **Use**: Run this first to check if everything is set up correctly

## 🎯 **Which Demo Should You Run?**

### **For First-Time Users**
```bash
python demo/run_working_demo.py
```
This is the most reliable demo that shows real LLM responses.

### **For Observability Features**
```bash
python demo/run_observability_demo.py
```
Then open http://localhost:5000 to see the dashboard.

### **For LLM Testing**
```bash
python demo/run_llm_demo.py
```
Tests all available LLM providers.

### **For Quick Verification**
```bash
python demo/test_llm_quick.py
```
Quick test to make sure everything works.

## 🔑 **API Key Setup**

To test real AI providers, set environment variables:

```bash
# For Gemini (recommended)
export GEMINI_API_KEY="your-gemini-api-key"

# For OpenAI
export OPENAI_API_KEY="your-openai-api-key"

# For Anthropic
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

Or the demos will prompt you for keys when you run them.

## 🌐 **Web Interfaces**

When running demos with observability:
- **Dashboard**: http://localhost:5000
- **Network Graph**: http://localhost:5000/static/graph.html

## 🛠️ **Dependencies**

Make sure you have the required packages:
```bash
pip install flask pydantic aiohttp
```

## 📊 **What You'll See**

### **Working Demo Output Example**:
```
================================================================================
📨 RESPONSE #1 FROM SyncLLMAgent
================================================================================
🤖 Gemini 2.0 Flash Response:

Artificial Intelligence (AI) is a branch of computer science that aims to create 
machines capable of performing tasks that typically require human intelligence...
================================================================================
```

### **LLM Test Results Example**:
```
🧪 LLM Provider Test Results:

✅ Mock AI: I understand your request about your query...
✅ Gemini 2.0: Artificial intelligence is the simulation of human intelligence...
❌ OpenAI GPT: API error 401: Incorrect API key provided
⚠️ Ollama: Ollama not found - install from https://ollama.ai

📊 Success Rate: 2/4 providers working
```

## 🎉 **Troubleshooting**

### **"No module named 'MultiProdigy'"**
Make sure you're running from the project root directory.

### **"Cannot run the event loop while another loop is running"**
Use the `working_demo.py` - it fixes this issue.

### **"No LLM responses"**
1. Check your API keys
2. Try the mock provider first
3. Run `test_llm_quick.py` to verify setup

### **Dashboard shows no data**
Wait 10-15 seconds for agents to start communicating, then refresh the page.

## 🎯 **Demo Comparison**

| Demo | LLM Integration | Observability | Async Issues | Best For |
|------|----------------|---------------|--------------|----------|
| **working_demo** | ✅ Real responses | ✅ Dashboard | ✅ Fixed | **First-time users** |
| **observability_demo** | ❌ No LLM | ✅ Full featured | ✅ No issues | Monitoring features |
| **llm_demo** | ✅ All providers | ❌ No dashboard | ⚠️ Some timeouts | LLM testing |
| **comprehensive_demo** | ✅ AI agents | ✅ Dashboard | ⚠️ Complex setup | Advanced users |

## 🚀 **Get Started Now**

```bash
# Run the best demo
python demo/run_working_demo.py

# Then explore the dashboard
# Open http://localhost:5000 in your browser
```

Happy exploring! 🎉