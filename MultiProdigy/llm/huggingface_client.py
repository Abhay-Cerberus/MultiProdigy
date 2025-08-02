"""
Legacy HuggingFace client compatibility layer
This file maintains backward compatibility while redirecting to the new unified system
"""

import warnings
from MultiProdigy.llm.factory import LLMFactory

warnings.warn(
    "MultiProdigy.llm.huggingface_client is deprecated. Use MultiProdigy.llm.factory.LLMFactory instead.",
    DeprecationWarning,
    stacklevel=2
)

class HuggingFaceClient:
    """Legacy HuggingFace client - redirects to unified system"""
    
    def __init__(self, model_name: str = "gpt2", **kwargs):
        warnings.warn(
            "HuggingFaceClient is deprecated. Use LLMFactory.create_huggingface() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        self._client = LLMFactory.create_huggingface(model=model_name, **kwargs)
    
    async def generate(self, prompt: str) -> str:
        """Legacy generate method"""
        response = await self._client.generate(prompt)
        return response.content