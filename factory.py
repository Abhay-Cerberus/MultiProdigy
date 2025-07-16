from typing import Type, Dict, Any
from .base import LLMClient


_llm_registry: Dict[str, Type[LLMClient]] = {}

def register_llm(name: str, client_cls: Type[LLMClient]):
    """
    Register a new LLM client class by name.
    """
    if name in _llm_registry:
        raise ValueError(f"LLM client '{name}' is already registered.")
    if not issubclass(client_cls, LLMClient):
        raise TypeError("client_cls must be a subclass of LLMClient")
    _llm_registry[name] = client_cls

def get_llm_client(name: str, **kwargs: Any) -> LLMClient:
    """
    Instantiate a registered LLM client by name with given kwargs.
    """
    if name not in _llm_registry:
        raise ValueError(f"LLM client '{name}' is not registered.")
    return _llm_registry[name](**kwargs)