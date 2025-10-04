"""
MultiProdigy Unified LLM Module

This module provides a consistent, Pydantic-based interface for all LLM providers.
All providers (OpenAI, Gemini, Anthropic, Ollama, HuggingFace) use the same API.

Example Usage:
    from MultiProdigy.llm import LLMFactory

    # Create any provider with consistent interface
    client = LLMFactory.create_openai("gpt-4", api_key="...")
    client = LLMFactory.create_gemini("gemini-pro", api_key="...")
    client = LLMFactory.create_ollama("llama2")

    # All clients have the same methods
    response = await client.generate("Your prompt here")
    chat_response = await client.chat(messages)
"""

from .api_client import APILLMClient
from .base import BaseLLMClient, LLMConfig, LLMProvider, LLMResponse

# Main exports - new unified system
from .factory import LLMFactory, create_llm_client, get_supported_providers
from .local_client import HuggingFaceClient, MockClient, OllamaClient

# Legacy clients are deprecated - use LLMFactory instead

__all__ = [
    # New unified system (recommended)
    "LLMFactory",
    "BaseLLMClient",
    "LLMConfig",
    "LLMResponse",
    "LLMProvider",
    "APILLMClient",
    "OllamaClient",
    "HuggingFaceClient",
    "MockClient",
    "create_llm_client",
    "get_supported_providers",
    # Legacy compatibility removed - use LLMFactory instead
]

# Version info
__version__ = "2.1.0"
__description__ = "Unified LLM interface with Pydantic configuration"
