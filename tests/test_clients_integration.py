import pytest
import asyncio
import warnings

from MultiProdigy.llm.factory import LLMFactory
from MultiProdigy.llm.base import BaseLLMClient

@pytest.mark.asyncio
@pytest.mark.parametrize("provider, model, prompt", [
    ("mock", "mock-model", "Test mock prompt"),
    # Note: Real API tests are disabled to avoid long test times and API costs
    # To test real APIs, set environment variables and uncomment these lines:
    # ("openai", "gpt-3.5-turbo", "Test OpenAI prompt"),
    # ("gemini", "gemini-2.0-flash-exp", "Test Gemini prompt"),
    # ("ollama", "tinyllama", "Test Ollama prompt"),
    # ("huggingface", "distilgpt2", "Test HF prompt"),
])
async def test_llm_factory_clients(provider, model, prompt):
    """Test LLM clients created through the factory"""
    # Suppress deprecation warnings for cleaner test output
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        
        client = LLMFactory.create_client(provider=provider, model=model)
        assert isinstance(client, BaseLLMClient)
        
        # Test generation
        response = await client.generate(prompt)
        assert hasattr(response, 'content')
        assert isinstance(response.content, str)
        assert len(response.content) > 0

def test_factory_convenience_methods():
    """Test factory convenience methods (mock client only for speed)"""
    # Only test mock client to avoid network calls and long test times
    mock_client = LLMFactory.create_mock()
    assert isinstance(mock_client, BaseLLMClient)
    assert mock_client.config.provider == "mock"
    assert mock_client.config.model == "mock-model"

def test_supported_providers():
    """Test getting supported providers information"""
    providers = LLMFactory.get_supported_providers()
    
    assert isinstance(providers, dict)
    assert "openai" in providers
    assert "gemini" in providers
    assert "anthropic" in providers
    assert "ollama" in providers
    assert "huggingface" in providers
    assert "mock" in providers
    
    # Check provider structure
    for provider_name, provider_info in providers.items():
        assert "type" in provider_info
        assert "models" in provider_info
        assert "requires_api_key" in provider_info
        assert isinstance(provider_info["models"], list)
        assert isinstance(provider_info["requires_api_key"], bool)

@pytest.mark.asyncio
async def test_mock_client_functionality():
    """Test mock client specifically for reliable testing"""
    mock_client = LLMFactory.create_mock()
    
    test_prompt = "Hello, world!"
    response = await mock_client.generate(test_prompt)
    
    assert hasattr(response, 'content')
    assert isinstance(response.content, str)
    assert len(response.content) > 0
    assert hasattr(response, 'model')
    assert response.model == "mock-model"
