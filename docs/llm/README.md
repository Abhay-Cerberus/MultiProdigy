# 🧠 LLM Integration

Documentation for Language Model provider integrations in MultiProdigy.

## � LContents

- [📖 LLM Overview](llm.md) - Integration concepts and architecture
- [🎯 Choosing a Model](choosing_model.md) - Provider and model selection guide
- [⚡ Performance Guide](llm_performance.md) - Benchmarks and optimization

## 🤖 Supported Providers

### Production Ready
- **Gemini** - Google's AI with multimodal capabilities
- **OpenAI** - GPT models (GPT-4, GPT-3.5)
- **Anthropic** - Claude models with strong reasoning
- **Ollama** - Local LLM runtime for privacy

### Development
- **HuggingFace** - Open source models
- **Mock Provider** - Testing without API costs

## � Quiock Start

```python
from MultiProdigy.llm.factory import LLMFactory

# Create LLM client
llm = LLMFactory.create_gemini("gemini-2.0-flash-exp", api_key)

# Generate response
response = await llm.generate("Hello, how are you?")
print(response.content)
```

## 📊 Provider Comparison

| Provider | Strengths | Best For | Cost |
|----------|-----------|----------|------|
| **Gemini** | Multimodal, Fast | General purpose, Vision | Low-Medium |
| **OpenAI** | Mature, Reliable | Production apps | Medium-High |
| **Anthropic** | Safety-focused | Complex analysis | Medium |
| **Ollama** | Local, Private | Privacy, Development | Free |

## 🔑 API Keys

Get your API keys:
- [Gemini API](https://makersuite.google.com/app/apikey)
- [OpenAI API](https://platform.openai.com/api-keys)
- [Anthropic API](https://console.anthropic.com/)

Set environment variables:
```bash
export GEMINI_API_KEY="your-gemini-key"
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
```

## 🔗 Related

- [LLM Integration Guide](../guides/llm_integration.md) - Step-by-step guide
- [LLM API Reference](../api/llm.md) - Complete API documentation
- [Agent Development](../guides/agent_development.md) - Building LLM-powered agents