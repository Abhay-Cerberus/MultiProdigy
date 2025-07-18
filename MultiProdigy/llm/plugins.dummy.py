from base import LLMClient
from typing import List

class DummyLLM(LLMClient):
    def generate(self, prompt: str, **kwargs) -> str:
        return f"Echo: {prompt}"

    def embed(self, texts: List[str], **kwargs) -> List[List[float]]:
        return [[0.1] * 5 for _ in texts]

    def chat(self, messages: List[dict], **kwargs) -> str:
        return "Hello from DummyLLM"

