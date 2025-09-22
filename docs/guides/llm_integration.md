# 🧠 LLM Integration Guide

## Overview

This guide covers integrating Language Models with MultiProdigy agents.

## Supported Providers

- **Gemini** - Google's AI platform
- **OpenAI** - GPT models
- **Anthropic** - Claude models
- **Ollama** - Local LLM runtime
- **HuggingFace** - Open source models
- **Mock** - Testing and development

## Basic Usage

```python
from MultiProdigy.llm.factory import LLMFactory

# Create LLM client
llm = LLMFactory.create_gemini("gemini-2.0-flash-exp", api_key)

# Generate response
response = await llm.generate("Hello, how are you?")
print(response.content)
```

## Provider-Specific Guides

For detailed provider documentation, see [LLM Providers](../llm/).

## API Reference

See [LLM API](../api/llm.md) for complete API documentation.

---

**Next Steps**: [Observability](observability.md) | [LLM Providers](../llm/)