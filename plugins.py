from .base import LLMClient

class DummyLLM(LLMClient):
    def __init__(self, **kwargs):
        self.config = kwargs

    def complete(self, prompt: str, **kwargs) -> str:
        return f"Completed: {prompt}"

    def chat(self, messages: list[dict], **kwargs) -> str:
        return "Chat response"
