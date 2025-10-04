from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class LLMProvider(str, Enum):
    """Supported LLM providers"""

    OPENAI = "openai"
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"
    HUGGINGFACE = "huggingface"
    OLLAMA = "ollama"
    MOCK = "mock"


class LLMConfig(BaseModel):
    """Pydantic configuration for LLM clients"""

    provider: LLMProvider
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, gt=0)
    timeout: int = Field(default=30, gt=0)
    extra_params: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"use_enum_values": True}


class LLMResponse(BaseModel):
    """Standardized LLM response format"""

    content: str
    provider: str
    model: str
    usage: Optional[Dict[str, int]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseLLMClient(ABC):
    """Base class for all LLM clients using Pydantic configuration"""

    def __init__(self, config: LLMConfig):
        self.config = config
        self.provider = config.provider
        self.model = config.model

    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate text based on the given prompt"""
        pass

    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """Chat completion with message history"""
        pass

    async def embed(self, texts: List[str], **kwargs) -> List[List[float]]:
        """Generate embeddings (optional, not all providers support this)"""
        raise NotImplementedError(f"Embeddings not supported by {self.provider}")

    def get_config(self) -> LLMConfig:
        """Get the current configuration"""
        return self.config

    def update_config(self, **kwargs) -> None:
        """Update configuration parameters"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
