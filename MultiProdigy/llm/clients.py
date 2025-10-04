"""
Legacy client compatibility layer
This file maintains backward compatibility while redirecting to the new unified system
"""

import warnings

from MultiProdigy.llm.base import BaseLLMClient
from MultiProdigy.llm.factory import LLMFactory

# Deprecation warning for old imports
warnings.warn(
    "MultiProdigy.llm.clients is deprecated. Use MultiProdigy.llm.factory.LLMFactory instead.",
    DeprecationWarning,
    stacklevel=2,
)


class OpenAIClient(BaseLLMClient):
    """Legacy OpenAI client - redirects to unified system"""

    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo", **kwargs):
        warnings.warn(
            "OpenAIClient is deprecated. Use LLMFactory.create_openai() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self._client = LLMFactory.create_openai(model=model, api_key=api_key, **kwargs)

    async def generate(self, prompt: str) -> str:
        """Legacy generate method"""
        response = await self._client.generate(prompt)
        return response.content


class GeminiClient(BaseLLMClient):
    """Legacy Gemini client - redirects to unified system"""

    def __init__(self, api_key: str = None, model: str = "gemini-2.0-flash-exp", **kwargs):
        warnings.warn(
            "GeminiClient is deprecated. Use LLMFactory.create_gemini() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self._client = LLMFactory.create_gemini(model=model, api_key=api_key, **kwargs)

    async def generate(self, prompt: str) -> str:
        """Legacy generate method"""
        response = await self._client.generate(prompt)
        return response.content


class OllamaClient(BaseLLMClient):
    """Legacy Ollama client - redirects to unified system"""

    def __init__(self, model: str = "tinyllama", **kwargs):
        warnings.warn(
            "OllamaClient is deprecated. Use LLMFactory.create_ollama() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self._client = LLMFactory.create_ollama(model=model, **kwargs)

    async def generate(self, prompt: str) -> str:
        """Legacy generate method"""
        response = await self._client.generate(prompt)
        return response.content
