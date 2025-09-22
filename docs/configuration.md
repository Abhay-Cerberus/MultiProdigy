# ⚙️ Configuration Guide

Complete configuration reference for MultiProdigy's layered configuration system.

## 🔧 Configuration Layers

1. **Default values** → 2. **Config files** → 3. **Environment variables** → 4. **Runtime parameters**

## 📁 Configuration Files

### **Main Config** (`config.yaml`)
```yaml
app:
  debug: false
  log_level: "INFO"

server:
  host: "localhost"
  port: 5000

agents:
  default_timeout: 30
  max_retries: 3

llm:
  default_provider: "gemini"
  timeout: 30
  max_tokens: 1000
  temperature: 0.7
  
  providers:
    gemini:
      model: "gemini-2.0-flash-exp"
    openai:
      model: "gpt-3.5-turbo"
    anthropic:
      model: "claude-3-sonnet-20240229"

observability:
  enabled: true
  dashboard_port: 5000
  trace_storage: "memory"
```

### **Environment Variables** (`.env`)
```bash
# API Keys
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Application
MULTIPRODIGY_DEBUG=false
MULTIPRODIGY_PORT=5000
DEFAULT_LLM_PROVIDER=gemini

# Local LLM (optional)
OLLAMA_BASE_URL=http://localhost:11434
```

## 🔑 API Key Setup

### **Get API Keys**
- **Gemini**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **OpenAI**: [OpenAI Platform](https://platform.openai.com/api-keys)
- **Anthropic**: [Anthropic Console](https://console.anthropic.com/)

### **Provider Support**
| Provider | Variable | Required | Notes |
|----------|----------|----------|-------|
| Gemini | `GEMINI_API_KEY` | No | Recommended |
| OpenAI | `OPENAI_API_KEY` | No | GPT models |
| Anthropic | `ANTHROPIC_API_KEY` | No | Claude models |
| Ollama | `OLLAMA_BASE_URL` | No | Local models |

## ⚙️ Runtime Configuration

### **Programmatic Config**
```python
from MultiProdigy.config.config import Config
from MultiProdigy.llm.factory import LLMFactory

# Load and override
config = Config.load("config.yaml")
config.llm.temperature = 0.9

# Custom LLM client
llm = LLMFactory.create_openai(
    model="gpt-4",
    temperature=0.5,
    max_tokens=2000
)
```

### **Agent Configuration**
```python
class CustomAgent(BaseAgent):
    def __init__(self, name, bus, **config):
        super().__init__(name, bus)
        self.timeout = config.get('timeout', 30)
        self.max_retries = config.get('max_retries', 3)

# Usage
agent = CustomAgent("MyAgent", bus, timeout=60, max_retries=5)
```

## 🌐 Environment Variables Reference

### **Core Settings**
```bash
MULTIPRODIGY_DEBUG=true|false
MULTIPRODIGY_LOG_LEVEL=DEBUG|INFO|WARN|ERROR
MULTIPRODIGY_PORT=5000
MULTIPRODIGY_HOST=localhost
```

### **LLM Settings**
```bash
DEFAULT_LLM_PROVIDER=gemini|openai|anthropic|ollama|mock
LLM_TIMEOUT=30
LLM_MAX_TOKENS=1000
LLM_TEMPERATURE=0.7
```

### **Observability Settings**
```bash
OBSERVABILITY_ENABLED=true|false
DASHBOARD_PORT=5000
TRACE_STORAGE=memory|file|database
```

## 🔧 Advanced Configuration

### **Custom Config Classes**
```python
from pydantic import BaseModel

class CustomAgentConfig(BaseModel):
    name: str
    timeout: int = 30
    max_retries: int = 3
    custom_parameter: str = None

# Usage
config = CustomAgentConfig(name="MyAgent", timeout=60)
```

### **Configuration Validation**
```python
from MultiProdigy.config.config import Config, ConfigError

try:
    config = Config.load("config.yaml")
    config.validate()
    print("✅ Configuration valid")
except ConfigError as e:
    print(f"❌ Config error: {e}")
```

## 🔍 Debugging Configuration

### **View Current Config**
```python
config = Config.load()
print(config.to_dict())
```

### **Check Environment Variables**
```python
import os

env_vars = {k: v for k, v in os.environ.items() 
           if k.startswith('MULTIPRODIGY_') or k.endswith('_API_KEY')}

for key, value in env_vars.items():
    if 'API_KEY' in key:
        value = f"{value[:8]}..." if value else "Not set"
    print(f"{key}: {value}")
```

## 📝 Best Practices

### **Security**
- Store API keys in environment variables
- Never commit secrets to version control
- Use different keys for dev/prod
- Rotate keys regularly

### **Organization**
- Keep config files in version control (without secrets)
- Use separate configs for different environments
- Document all options
- Validate on startup

### **Performance**
- Set appropriate timeouts
- Configure caching
- Monitor resource usage
- Use local models for development

## 🔍 Troubleshooting

### **Common Issues**
- **API Key Errors**: Check environment variables and validity
- **Port Conflicts**: Use `MULTIPRODIGY_PORT=5001`
- **Config Not Found**: Verify file paths and permissions
- **Invalid Values**: Check data types and ranges

### **Debug Mode**
```bash
export MULTIPRODIGY_DEBUG=true
python demo/run_working_demo.py
```

## 🔗 Related Documentation

- [🔧 Installation Guide](installation.md) - Setup and dependencies
- [🚀 Getting Started](getting_started.md) - Quick start guide
- [🧠 LLM Integration](guides/llm_integration.md) - AI provider setup
- [📊 Observability](guides/observability.md) - Monitoring configuration

**Configuration ready?** Continue with [🚀 Getting Started](getting_started.md)!