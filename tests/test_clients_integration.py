import pytest
import time
import asyncio

from MultiProdigy.llm.clients import OpenAIClient, GeminiClient, OllamaClient
from MultiProdigy.llm.huggingface_client import HuggingFaceClient
from MultiProdigy.llm.factory import list_registered_llms, register_llm, get_llm

@pytest.mark.asyncio
@pytest.mark.parametrize("client_cls, kwargs, prompt", [
    (OpenAIClient, {}, "Test OpenAI prompt"),
    (GeminiClient, {}, "Test Gemini prompt"),
    (OllamaClient, {"model": "tinyllama"}, "Test Ollama prompt"),
    (HuggingFaceClient, {"model_name": "distilgpt2"}, "Test HF prompt"),
])
async def test_builtin_llm_clients(client_cls, kwargs, prompt):
    client = client_cls(**kwargs)
    resp = await client.generate(prompt)

    # Basic response checks
    assert isinstance(resp, str)
    assert prompt in resp or len(resp) > 0

def test_factory_registration_and_lookup():
    class Dummy:
        async def generate(self, prompt): return "ok"

    # ensure dummy is not registered yet
    if "dummy" in list_registered_llms():
        pytest.skip("dummy already registered")

    register_llm("dummy", Dummy)
    assert "dummy" in list_registered_llms()

    inst = get_llm("dummy")
    result = asyncio.run(inst.generate("foo"))
    assert result == "ok"
