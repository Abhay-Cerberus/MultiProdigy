# 🔧 Installation & Setup

Complete installation guide for MultiProdigy with all dependencies and optional components.

## 📋 System Requirements

### **Minimum**
- **Python**: 3.9+
- **OS**: Windows, macOS, Linux
- **RAM**: 4GB (8GB recommended)
- **Storage**: 1GB free space

### **Recommended**
- **Python**: 3.11+ for best performance
- **RAM**: 16GB for large deployments
- **GPU**: Optional for local LLM inference

## ⚡ Quick Installation

### **1. Clone & Setup**
```bash
git clone https://github.com/Abhay-Cerberus/MultiProdigy.git
cd MultiProdigy
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### **2. Install Dependencies**
```bash
# Install all dependencies
pip install -r requirements.txt
```

### **3. Verify Installation**
```bash
# Quick test
python demo/test_llm_quick.py

# Full demo
python demo/run_working_demo.py
```

## 📦 Dependencies

### **Dependencies** (`requirements.txt`)
All dependencies are in a single requirements.txt file including:
- Core framework dependencies (pydantic, aiohttp, flask)
- LLM integration libraries (transformers, torch)
- Development and testing tools (pytest, black, mypy)
- Documentation tools (mkdocs)

### **Development** (Optional)
```bash
pip install pytest black isort flake8 mypy pre-commit
```

## 🔑 API Key Setup

### **Environment Variables** (Recommended)
```bash
# Create .env file
cp .env.example .env

# Add your keys
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

### **Get API Keys**
- **Gemini**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **OpenAI**: [OpenAI Platform](https://platform.openai.com/api-keys)
- **Anthropic**: [Anthropic Console](https://console.anthropic.com/)

### **System Environment**
```bash
# Linux/macOS
export GEMINI_API_KEY="your_key"

# Windows CMD
set GEMINI_API_KEY=your_key

# Windows PowerShell
$env:GEMINI_API_KEY="your_key"
```

## 🔧 Optional Components

### **Local LLM (Ollama)**
```bash
# Install Ollama (visit https://ollama.ai)
ollama pull llama2
ollama pull codellama
```

### **HuggingFace Transformers**
```bash
pip install transformers torch
```

### **Development Tools**
```bash
pip install black isort flake8 mypy pytest pre-commit
pre-commit install
```

## 🐳 Docker Alternative

### **Docker Compose**
```bash
git clone https://github.com/Abhay-Cerberus/MultiProdigy.git
cd MultiProdigy
docker-compose up --build
```

### **Manual Docker**
```bash
docker build -t multiprodigy .
docker run -p 5000:5000 -e GEMINI_API_KEY=your_key multiprodigy
```

## 🔍 Troubleshooting

### **Common Issues**

#### **Import Errors**
```bash
# Error: ModuleNotFoundError
# Solution: Run from project root
cd /path/to/MultiProdigy
python demo/run_working_demo.py
```

#### **API Key Issues**
```bash
# Check environment variables
python -c "import os; print('GEMINI_API_KEY:', os.getenv('GEMINI_API_KEY'))"
```

#### **Port Conflicts**
```bash
# Use different port
export FLASK_PORT=5001
python demo/run_working_demo.py
```

#### **Permission Errors**
```bash
# Use virtual environment or --user flag
pip install --user -r requirements.txt
```

### **Platform-Specific**

#### **Windows**
- Use `python` instead of `python3`
- Use `venv\Scripts\activate`
- Consider PowerShell over CMD

#### **macOS**
- Install Xcode tools: `xcode-select --install`
- Use `python3` if multiple versions installed

#### **Linux**
- Install python3-venv: `sudo apt install python3-venv`
- Update pip: `python3 -m pip install --upgrade pip`

## ✅ Verification

### **Test Installation**
```bash
# Core
python -c "from MultiProdigy.agents.agent_base import BaseAgent; print('✅ Core OK')"

# LLM
python -c "from MultiProdigy.llm.factory import LLMFactory; print('✅ LLM OK')"

# Observability
python -c "from MultiProdigy.observability.dashboard import ObservabilityDashboard; print('✅ Dashboard OK')"

# Quick test
python demo/test_llm_quick.py

# Full demo
python demo/run_working_demo.py
# Visit: http://localhost:5000
```

## 🚀 Next Steps

After installation:

1. **Run demo**: `python demo/run_working_demo.py`
2. **Explore dashboard**: http://localhost:5000
3. **Quick start**: [Getting Started](getting_started.md)
4. **Build agents**: [Agent Development](guides/agent_development.md)
5. **Join community**: [GitHub Discussions](https://github.com/Abhay-Cerberus/MultiProdigy/discussions)

## 📞 Getting Help

Need assistance?

1. **Check troubleshooting** above
2. **Search issues**: [GitHub Issues](https://github.com/Abhay-Cerberus/MultiProdigy/issues)
3. **Ask questions**: [GitHub Discussions](https://github.com/Abhay-Cerberus/MultiProdigy/discussions)
4. **Report bugs**: Include OS, Python version, error messages

## 🔗 Related Documentation

- [⚙️ Configuration](configuration.md) - Settings and environment setup
- [🚀 Getting Started](getting_started.md) - Quick start guide
- [🏗️ Architecture](architecture.md) - System overview
- [🤖 Agent Development](guides/agent_development.md) - Building custom agents

**Installation complete?** Continue with [🚀 Getting Started](getting_started.md)!