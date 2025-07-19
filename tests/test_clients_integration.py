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
    start = time.monotonic()
    resp = await client.generate(prompt)
    duration = time.monotonic() - start

    assert isinstance(resp, str)
    assert prompt in resp or len(resp) > 0

    # record duration for benchmark
    pytest.benchmark_data.setdefault(client_cls.__name__, []).append(duration)

def test_factory_registration_and_lookup():
    class Dummy:
        async def generate(self, prompt): return "ok"
    # ensure dummy not already present
    if "dummy" in list_registered_llms():
        pytest.skip("dummy already registered")
    register_llm("dummy", Dummy)
    assert "dummy" in list_registered_llms()
    inst = get_llm("dummy")
    assert asyncio.run(inst.generate("foo")) == "ok"
