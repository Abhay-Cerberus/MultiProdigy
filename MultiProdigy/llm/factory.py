"""
Unified LLM factory using Pydantic configuration
This replaces the old registry system with a cleaner, type-safe approach
"""

from typing import Any, Dict, Optional

from MultiProdigy.llm.api_client import APILLMClient
from MultiProdigy.llm.base import BaseLLMClient, LLMConfig, LLMProvider
from MultiProdigy.llm.local_client import HuggingFaceClient, MockClient, OllamaClient


class LLMFactory:
    """Factory for creating LLM clients with Pydantic configuration"""

    @staticmethod
    def create_client(
        provider: str, model: str, api_key: Optional[str] = None, **kwargs
    ) -> BaseLLMClient:
        """Create an LLM client with the specified configuration"""

        # Create Pydantic config
        config = LLMConfig(provider=provider, model=model, api_key=api_key, **kwargs)

        return LLMFactory.create_from_config(config)

    @staticmethod
    def create_from_config(config: LLMConfig) -> BaseLLMClient:
        """Create an LLM client from a Pydantic configuration"""

        if config.provider in [LLMProvider.OPENAI, LLMProvider.GEMINI, LLMProvider.ANTHROPIC]:
            return APILLMClient(config)
        elif config.provider == LLMProvider.OLLAMA:
            return OllamaClient(config)
        elif config.provider == LLMProvider.HUGGINGFACE:
            return HuggingFaceClient(config)
        elif config.provider == LLMProvider.MOCK:
            return MockClient(config)
        else:
            raise ValueError(f"Unsupported provider: {config.provider}")

    @staticmethod
    def create_openai(
        model: str = "gpt-3.5-turbo", api_key: Optional[str] = None, **kwargs
    ) -> BaseLLMClient:
        """Create OpenAI client"""
        return LLMFactory.create_client(
            provider=LLMProvider.OPENAI, model=model, api_key=api_key, **kwargs
        )

    @staticmethod
    def create_gemini(
        model: str = "gemini-2.0-flash-exp", api_key: Optional[str] = None, **kwargs
    ) -> BaseLLMClient:
        """Create Gemini client"""
        return LLMFactory.create_client(
            provider=LLMProvider.GEMINI, model=model, api_key=api_key, **kwargs
        )

    @staticmethod
    def create_anthropic(
        model: str = "claude-3-sonnet-20240229", api_key: Optional[str] = None, **kwargs
    ) -> BaseLLMClient:
        """Create Anthropic Claude client"""
        return LLMFactory.create_client(
            provider=LLMProvider.ANTHROPIC, model=model, api_key=api_key, **kwargs
        )

    @staticmethod
    def create_ollama(
        model: str = "llama2", base_url: str = "http://localhost:11434", **kwargs
    ) -> BaseLLMClient:
        """Create Ollama client"""
        return LLMFactory.create_client(
            provider=LLMProvider.OLLAMA, model=model, base_url=base_url, **kwargs
        )

    @staticmethod
    def create_huggingface(model: str = "gpt2", **kwargs) -> BaseLLMClient:
        """Create HuggingFace client"""
        return LLMFactory.create_client(provider=LLMProvider.HUGGINGFACE, model=model, **kwargs)

    @staticmethod
    def create_mock(model: str = "mock-model", **kwargs) -> BaseLLMClient:
        """Create mock client for testing"""
        return LLMFactory.create_client(provider=LLMProvider.MOCK, model=model, **kwargs)

    @staticmethod
    def get_supported_providers() -> Dict[str, Dict[str, Any]]:
        """Get information about supported providers"""
        return {
            "openai": {
                "type": "api",
                "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
                "requires_api_key": True,
                "supports_chat": True,
                "supports_embeddings": True,
            },
            "gemini": {
                "type": "api",
                "models": ["gemini-2.0-flash-exp", "gemini-pro", "gemini-pro-vision"],
                "requires_api_key": True,
                "supports_chat": True,
                "supports_embeddings": False,
            },
            "anthropic": {
                "type": "api",
                "models": ["claude-3-sonnet-20240229", "claude-3-opus-20240229"],
                "requires_api_key": True,
                "supports_chat": True,
                "supports_embeddings": False,
            },
            "ollama": {
                "type": "local",
                "models": ["llama2", "codellama", "mistral", "tinyllama"],
                "requires_api_key": False,
                "supports_chat": True,
                "supports_embeddings": False,
            },
            "huggingface": {
                "type": "local",
                "models": ["gpt2", "distilgpt2", "microsoft/DialoGPT-medium"],
                "requires_api_key": False,
                "supports_chat": True,
                "supports_embeddings": False,
            },
            "mock": {
                "type": "mock",
                "models": ["mock-model"],
                "requires_api_key": False,
                "supports_chat": True,
                "supports_embeddings": False,
            },
        }


# Convenience functions for backward compatibility
def create_llm_client(provider: str, model: str, **kwargs) -> BaseLLMClient:
    """Create LLM client (backward compatibility)"""
    return LLMFactory.create_client(provider, model, **kwargs)


def get_supported_providers() -> Dict[str, Dict[str, Any]]:
    """Get supported providers (backward compatibility)"""
    return LLMFactory.get_supported_providers()
