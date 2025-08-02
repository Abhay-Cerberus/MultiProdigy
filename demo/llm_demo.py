#!/usr/bin/env python3
"""
MultiProdigy Unified LLM Demo

This demo shows the new Pydantic-based LLM architecture that works
consistently across all providers (OpenAI, Gemini, Anthropic, Ollama, etc.)
"""

import sys
import os
import asyncio

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from MultiProdigy.llm.factory import LLMFactory
from MultiProdigy.llm.base import LLMConfig, LLMProvider

async def demo_provider(provider_name: str, model: str, api_key: str = None):
    """Demo a specific LLM provider"""
    print(f"\n🤖 Testing {provider_name.upper()} with model: {model}")
    print("-" * 50)
    
    try:
        # Create client using factory with shorter timeout for demo
        client = LLMFactory.create_client(
            provider=provider_name,
            model=model,
            api_key=api_key,
            temperature=0.7,
            max_tokens=100,
            timeout=10  # Shorter timeout for demo
        )
        
        # Test single generation
        print("📝 Single Generation Test:")
        response = await client.generate("Explain what artificial intelligence is in one sentence.")
        print(f"Response: {response.content}")
        print(f"Provider: {response.provider}, Model: {response.model}")
        
        # Test chat completion
        print("\n💬 Chat Completion Test:")
        messages = [
            {"role": "user", "content": "What is the capital of France?"},
            {"role": "assistant", "content": "The capital of France is Paris."},
            {"role": "user", "content": "What's the population?"}
        ]
        
        chat_response = await client.chat(messages)
        print(f"Chat Response: {chat_response.content}")
        
        # Show configuration
        print(f"\n⚙️ Configuration: {client.get_config().model_dump()}")
        
        # Close client if it has async cleanup
        if hasattr(client, 'close'):
            await client.close()
            
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error testing {provider_name}: {e}")

async def demo_all_providers():
    """Demo all available providers"""
    print("🚀 MultiProdigy Unified LLM System Demo")
    print("=" * 60)
    
    # Show supported providers
    providers = LLMFactory.get_supported_providers()
    print("\n📋 Supported Providers:")
    for name, info in providers.items():
        print(f"  • {name.upper()}: {info['type']} - {len(info['models'])} models")
    
    # Demo each provider
    test_cases = [
        # Mock provider (always works)
        ("mock", "mock-model", None),
        
        # API providers (require keys)
        ("openai", "gpt-3.5-turbo", os.getenv("OPENAI_API_KEY")),
        ("gemini", "gemini-2.0-flash-exp", os.getenv("GEMINI_API_KEY")),
        ("anthropic", "claude-3-sonnet-20240229", os.getenv("ANTHROPIC_API_KEY")),
        
        # Local providers (require installation)
        ("ollama", "tinyllama", None),
        ("huggingface", "gpt2", None),
    ]
    
    for provider, model, api_key in test_cases:
        if provider in ["openai", "gemini", "anthropic"] and not api_key:
            print(f"\n⚠️  Skipping {provider.upper()} - no API key found")
            print(f"   Set {provider.upper()}_API_KEY environment variable to test")
            continue
            
        await demo_provider(provider, model, api_key)

async def demo_configuration_flexibility():
    """Demo the flexible Pydantic configuration system"""
    print("\n🔧 Configuration Flexibility Demo")
    print("=" * 50)
    
    # Create config with Pydantic validation
    config = LLMConfig(
        provider=LLMProvider.MOCK,
        model="advanced-mock",
        temperature=0.9,
        max_tokens=200,
        timeout=60,
        extra_params={"custom_param": "value"}
    )
    
    print(f"📋 Created config: {config.model_dump()}")
    
    # Create client from config
    client = LLMFactory.create_from_config(config)
    
    # Test with custom parameters
    response = await client.generate("Create a creative story about robots.")
    print(f"🎨 Creative response: {response.content}")
    
    # Update configuration dynamically
    client.update_config(temperature=0.1, max_tokens=50)
    print(f"🔄 Updated config: {client.get_config().model_dump()}")
    
    # Test with updated config
    response2 = await client.generate("Explain quantum computing.")
    print(f"🔬 Technical response: {response2.content}")

async def demo_agent_integration():
    """Demo how agents can use the unified LLM system"""
    print("\n🤝 Agent Integration Demo")
    print("=" * 50)
    
    # Simulate an agent that needs LLM capabilities
    class IntelligentAgent:
        def __init__(self, llm_provider: str = "mock", model: str = "mock-model"):
            self.llm = LLMFactory.create_client(
                provider=llm_provider,
                model=model,
                temperature=0.7
            )
        
        async def analyze_task(self, task: str) -> str:
            """Analyze a task using LLM"""
            prompt = f"Analyze this task and provide recommendations: {task}"
            response = await self.llm.generate(prompt)
            return response.content
        
        async def chat_with_user(self, user_message: str, context: list = None) -> str:
            """Chat with user using conversation context"""
            messages = context or []
            messages.append({"role": "user", "content": user_message})
            
            response = await self.llm.chat(messages)
            return response.content
    
    # Create intelligent agent
    agent = IntelligentAgent()
    
    # Test task analysis
    task_analysis = await agent.analyze_task("Implement a new user authentication system")
    print(f"🎯 Task Analysis: {task_analysis}")
    
    # Test conversational capability
    conversation = [
        {"role": "user", "content": "Hello, I need help with my project"},
        {"role": "assistant", "content": "I'd be happy to help! What kind of project are you working on?"}
    ]
    
    response = await agent.chat_with_user("It's a web application for task management", conversation)
    print(f"💬 Agent Response: {response}")

def main():
    """Main demo function"""
    print("🎉 Welcome to MultiProdigy Unified LLM System!")
    print("\nThis demo shows how all LLM providers now use a consistent")
    print("Pydantic-based architecture instead of separate client files.\n")
    
    # Run all demos
    asyncio.run(demo_all_providers())
    asyncio.run(demo_configuration_flexibility())
    asyncio.run(demo_agent_integration())
    
    print("\n" + "=" * 60)
    print("✨ Demo completed!")
    print("\n🔑 Key Benefits of the New Architecture:")
    print("  • Consistent API across all providers")
    print("  • Pydantic validation and type safety")
    print("  • Easy configuration management")
    print("  • Unified response format")
    print("  • Async support throughout")
    print("  • Easy to extend with new providers")
    
    print("\n📚 Usage Examples:")
    print("  # Create any provider with same interface")
    print("  client = LLMFactory.create_openai('gpt-4', api_key='...')")
    print("  client = LLMFactory.create_gemini('gemini-pro', api_key='...')")
    print("  client = LLMFactory.create_ollama('llama2')")
    print("  ")
    print("  # All clients have same methods")
    print("  response = await client.generate('Your prompt here')")
    print("  chat_response = await client.chat(messages)")

if __name__ == "__main__":
    main()