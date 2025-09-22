# 🧠 LLM API Reference

## LLMFactory Class

Factory for creating LLM client instances.

### Static Methods

#### `create_gemini(model: str, api_key: str)`
Create a Gemini LLM client.

**Parameters:**
- `model` (str): Model name (e.g., "gemini-2.0-flash-exp")
- `api_key` (str): Gemini API key

**Returns:** `GeminiLLM` instance

#### `create_openai(model: str, api_key: str)`
Create an OpenAI LLM client.

**Parameters:**
- `model` (str): Model name (e.g., "gpt-4")
- `api_key` (str): OpenAI API key

**Returns:** `OpenAILLM` instance

#### `create_mock()`
Create a mock LLM client for testing.

**Returns:** `MockLLM` instance

## BaseLLM Interface

Base interface for all LLM implementations.

### Methods

#### `async generate(prompt: str) -> LLMResponse`
Generate a response from the LLM.

**Parameters:**
- `prompt` (str): Input prompt

**Returns:** `LLMResponse` object

#### `get_model_info() -> Dict`
Get information about the model.

**Returns:** Dictionary with model details

## LLMResponse Class

Response object from LLM generation.

### Properties

- `content` (str): Generated text
- `model` (str): Model used
- `usage` (Dict): Token usage information
- `metadata` (Dict): Additional response metadata

## Example Usage

```python
from MultiProdigy.llm.factory import LLMFactory
import asyncio

# Create LLM client
llm = LLMFactory.create_gemini("gemini-2.0-flash-exp", api_key)

# Generate response
async def generate_response():
    response = await llm.generate("Hello, how are you?")
    print(f"Response: {response.content}")
    print(f"Model: {response.model}")

asyncio.run(generate_response())
```

## Related

- [LLM Integration Guide](../guides/llm_integration.md)
- [LLM Providers](../llm/)
- [Agent Development](../guides/agent_development.md)