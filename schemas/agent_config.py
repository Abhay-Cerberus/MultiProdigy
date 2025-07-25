from pydantic import BaseSettings, Field
from typing import Optional

class OpenAISettings(BaseSettings):
    api_key: str = Field(..., env="OPENAI_API_KEY")
    endpoint: Optional[str] = "https://api.openai.com/v1"
    default_model: str = "gpt-4"

class GeminiSettings(BaseSettings):
    api_key: str = Field(..., env="GEMINI_API_KEY")
    endpoint: Optional[str] = "https://generativelanguage.googleapis.com/v1beta/models"
    default_model: str = "gemini-pro"

class HFSettings(BaseSettings):
    api_key: str = Field(..., env="HF_API_KEY")
    endpoint: Optional[str] = "https://api-inference.huggingface.co/models"
    default_model: str = "HuggingFaceModel"

class LLMSettings(BaseSettings):
    openai: OpenAISettings = OpenAISettings()
    gemini: GeminiSettings = GeminiSettings()
    huggingface: HFSettings = HFSettings()