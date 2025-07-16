import abc
from typing import Any

class LLMClient(abc.ABC):
    @abc.abstractmethod
    def complete(self, prompt: str, **kwargs: Any) -> str:
        pass

    @abc.abstractmethod
    def chat(self, messages: list[dict], **kwargs: Any) -> str:
        pass
