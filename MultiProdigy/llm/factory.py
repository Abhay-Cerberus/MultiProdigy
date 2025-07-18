from typing import Type, Dict
from base import LLMClient

_llm_registry: Dict[str, Type[LLMClient]] = {}

def register_llm(name: str, client_cls: Type[LLMClient]):
    """Register a new LLM client class by name."""
    if name in _llm_registry:
        raise ValueError(f"LLM '{name}' is already registered.")
    _llm_registry[name] = client_cls

def get_llm(name: str, **kwargs) -> LLMClient:
    """Instantiate a registered LLM client by name."""
    if name not in _llm_registry:
        raise ValueError(f"LLM '{name}' is not registered.")
    return _llm_registry[name](**kwargs)

def list_registered_llms() -> Dict[str, Type[LLMClient]]:
    """Return a copy of the current LLM registry."""
    return _llm_registry.copy()


