"""
Legacy dummy/mock client compatibility layer
This file maintains backward compatibility while redirecting to the new unified system
"""

import warnings
from typing import List

from MultiProdigy.llm.factory import LLMFactory

warnings.warn(
    "MultiProdigy.llm.plugins.dummy is deprecated. Use MultiProdigy.llm.factory.LLMFactory.create_mock() instead.",
    DeprecationWarning,
    stacklevel=2,
)


class DummyLLM:
    """Legacy dummy client - redirects to unified system"""

    def __init__(self, **kwargs):
        warnings.warn(
            "DummyLLM is deprecated. Use LLMFactory.create_mock() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self._client = LLMFactory.create_mock(**kwargs)

    def generate(self, prompt: str, **kwargs) -> str:
        """Legacy sync generate method"""
        import asyncio

        response = asyncio.run(self._client.generate(prompt, **kwargs))
        return response.content

    def embed(self, texts: List[str], **kwargs) -> List[List[float]]:
        """Legacy embed method"""
        # Return dummy embeddings
        return [[0.1] * 5 for _ in texts]

    def chat(self, messages: List[dict], **kwargs) -> str:
        """Legacy chat method"""
        import asyncio

        response = asyncio.run(self._client.chat(messages, **kwargs))
        return response.content
