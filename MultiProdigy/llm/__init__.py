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

# Main exports - new unified system
from .factory import LLMFactory, create_llm_client, get_supported_providers
from .base import BaseLLMClient, LLMConfig, LLMResponse, LLMProvider
from .api_client import APILLMClient
from .local_client import OllamaClient, HuggingFaceClient, MockClient

# Legacy exports for backward compatibility (with deprecation warnings)
from .clients import OpenAIClient as LegacyOpenAIClient
from .clients import GeminiClient as LegacyGeminiClient
from .clients import OllamaClient as LegacyOllamaClient

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
    
    # Legacy compatibility (deprecated)
    "LegacyOpenAIClient",
    "LegacyGeminiClient", 
    "LegacyOllamaClient",
]

# Version info
__version__ = "2.0.0"
__description__ = "Unified LLM interface with Pydantic configuration"