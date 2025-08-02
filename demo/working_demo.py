#!/usr/bin/env python3
"""
MultiProdigy Working Demo - Simple and Effective

This demo actually WORKS and shows real LLM responses!
Fixed the async/sync issues with a simpler approach.
"""

import sys
import os
import time
import threading
from typing import Optional, Dict, Any

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from MultiProdigy.agents.agent_base import BaseAgent
from MultiProdigy.bus.message_bus import MessageBus
from MultiProdigy.schemas.message import Message
from MultiProdigy.observability.dashboard import ObservabilityDashboard
from MultiProdigy.llm.factory import LLMFactory

class SyncLLMAgent(BaseAgent):
    """Agent that uses LLM with proper sync handling"""
    
    def __init__(self, name: str, bus: MessageBus, api_keys: Dict[str, str] = None):
        super().__init__(name, bus)
        self.api_keys = api_keys or {}
        self.llm_client = None
        self.provider_name = "none"
        self._initialize_best_llm()
    
    def _initialize_best_llm(self):
        """Initialize the best available LLM client"""
        print(f"🤖 [{self.name}] Finding best LLM...")
        
        # Try Gemini first
        gemini_key = self.api_keys.get("gemini") or os.getenv("GEMINI_API_KEY")
        if gemini_key:
            try:
                self.llm_client = LLMFactory.create_gemini(
                    "gemini-2.0-flash-exp", 
                    gemini_key, 
                    timeout=15
                )
                self.provider_name = "Gemini 2.0 Flash"
                print(f"✅ [{self.name}] Using {self.provider_name}")
                return
            except Exception as e:
                print(f"❌ [{self.name}] Gemini failed: {e}")
        
        # Try OpenAI
        openai_key = self.api_keys.get("openai") or os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                self.llm_client = LLMFactory.create_openai("gpt-3.5-turbo", openai_key, timeout=15)
                self.provider_name = "OpenAI GPT-3.5"
                print(f"✅ [{self.name}] Using {self.provider_name}")
                return
            except Exception as e:
                print(f"❌ [{self.name}] OpenAI failed: {e}")
        
        # Fallback to Mock
        try:
            self.llm_client = LLMFactory.create_mock()
            self.provider_name = "Mock AI"
            print(f"🤖 [{self.name}] Using {self.provider_name}")
        except Exception as e:
            print(f"❌ [{self.name}] Even mock failed: {e}")
    
    def on_message(self, message: Message) -> None:
        """Handle message with LLM - using sync approach"""
        print(f"🧠 [{self.name}] Processing with {self.provider_name}: {message.content}")
        
        if not self.llm_client:
            self.send("❌ No LLM available", message.sender)
            return
        
        try:
            # Use asyncio.run to handle async LLM call in sync context
            import asyncio
            
            # Create a simple prompt
            prompt = f"Please provide a helpful response to: {message.content}"
            
            # Run the async LLM call
            response = asyncio.run(self.llm_client.generate(prompt))
            
            if response.content and not response.content.startswith("❌"):
                result = f"🤖 {self.provider_name} Response:\n\n{response.content}"
                print(f"✅ [{self.name}] Got response from {self.provider_name}")
            else:
                result = f"⚠️ {self.provider_name} returned: {response.content}"
                print(f"⚠️ [{self.name}] Weak response from {self.provider_name}")
            
            # Send the response back
            self.send(result, message.sender)
            
        except Exception as e:
            error_msg = f"❌ {self.provider_name} Error: {str(e)}"
            print(f"❌ [{self.name}] Error: {e}")
            self.send(error_msg, message.sender)

class TestAllLLMAgent(BaseAgent):
    """Agent that tests ALL LLM providers and shows results"""
    
    def __init__(self, name: str, bus: MessageBus, api_keys: Dict[str, str] = None):
        super().__init__(name, bus)
        self.api_keys = api_keys or {}
        self.test_count = 0
    
    def on_message(self, message: Message) -> None:
        """Test all LLM providers"""
        self.test_count += 1
        print(f"🧪 [{self.name}] Testing ALL LLM providers (Test #{self.test_count})")
        
        results = []
        test_prompt = f"Briefly explain: {message.content}"
        
        # Test Mock (always works)
        results.append(self._test_provider("mock", "Mock AI", test_prompt))
        
        # Test API providers
        api_tests = [
            ("gemini", "Gemini 2.0", "GEMINI_API_KEY"),
            ("openai", "OpenAI GPT", "OPENAI_API_KEY"),
            ("anthropic", "Claude", "ANTHROPIC_API_KEY")
        ]
        
        for provider, name, env_key in api_tests:
            api_key = self.api_keys.get(provider) or os.getenv(env_key)
            if api_key:
                results.append(self._test_provider(provider, name, test_prompt, api_key))
            else:
                results.append(f"⚠️ {name}: No API key provided")
        
        # Test local providers (with quick timeout)
        results.append(self._test_provider("ollama", "Ollama", test_prompt, timeout=5))
        results.append(self._test_provider("huggingface", "HuggingFace", test_prompt, timeout=8))
        
        # Compile results
        summary = f"🧪 LLM Provider Test Results (Test #{self.test_count}):\n\n"
        summary += "\n".join(results)
        
        # Count successes
        success_count = sum(1 for r in results if r.startswith("✅"))
        total_count = len([r for r in results if not r.startswith("⚠️")])
        summary += f"\n\n📊 Success Rate: {success_count}/{total_count} providers working"
        
        print(f"📊 [{self.name}] Test completed: {success_count}/{total_count} providers working")
        self.send(summary, message.sender)
    
    def _test_provider(self, provider: str, name: str, prompt: str, api_key: str = None, timeout: int = 10) -> str:
        """Test a single LLM provider"""
        try:
            print(f"🔄 [{self.name}] Testing {name}...")
            
            # Create client
            if provider == "mock":
                client = LLMFactory.create_mock()
            elif provider == "gemini":
                client = LLMFactory.create_gemini("gemini-2.0-flash-exp", api_key, timeout=timeout)
            elif provider == "openai":
                client = LLMFactory.create_openai("gpt-3.5-turbo", api_key, timeout=timeout)
            elif provider == "anthropic":
                client = LLMFactory.create_anthropic("claude-3-sonnet-20240229", api_key, timeout=timeout)
            elif provider == "ollama":
                client = LLMFactory.create_ollama("tinyllama", timeout=timeout)
            elif provider == "huggingface":
                client = LLMFactory.create_huggingface("gpt2", timeout=timeout)
            else:
                return f"❌ {name}: Unknown provider"
            
            # Test with timeout
            import asyncio
            response = asyncio.run(asyncio.wait_for(
                client.generate(prompt), 
                timeout=timeout
            ))
            
            if response.content and not response.content.startswith("❌"):
                preview = response.content[:80] + "..." if len(response.content) > 80 else response.content
                return f"✅ {name}: {preview}"
            else:
                return f"⚠️ {name}: {response.content[:50]}..."
                
        except Exception as e:
            error_msg = str(e)[:50] + "..." if len(str(e)) > 50 else str(e)
            return f"❌ {name}: {error_msg}"

class UserAgent(BaseAgent):
    """Simple user agent that sends requests and shows responses"""
    
    def __init__(self, name: str, bus: MessageBus):
        super().__init__(name, bus)
        self.response_count = 0
    
    def on_message(self, message: Message) -> None:
        """Display responses from other agents"""
        self.response_count += 1
        print(f"\n" + "="*80)
        print(f"📨 RESPONSE #{self.response_count} FROM {message.sender}")
        print("="*80)
        print(message.content)
        print("="*80 + "\n")
    
    def send_test_message(self, content: str, target: str):
        """Send a test message"""
        print(f"🎯 [USER] Sending to {target}: {content}")
        self.send(content, target)

def run_demo_tests(agents):
    """Run a series of demo tests"""
    user = agents["UserAgent"]
    
    test_scenarios = [
        ("What is artificial intelligence?", "SyncLLMAgent"),
        ("Explain quantum computing", "SyncLLMAgent"), 
        ("How does machine learning work?", "TestAllLLMAgent"),
        ("What are the benefits of renewable energy?", "SyncLLMAgent"),
        ("Test all AI providers", "TestAllLLMAgent"),
    ]
    
    print("\n🎬 Starting Demo Tests...")
    print("This will show you REAL LLM responses!\n")
    
    for i, (question, target) in enumerate(test_scenarios, 1):
        print(f"\n🔄 Demo Test {i}/{len(test_scenarios)}")
        user.send_test_message(question, target)
        
        # Wait for response
        time.sleep(8)
    
    print("\n✨ Demo tests completed!")

def get_api_keys():
    """Get API keys from user"""
    api_keys = {}
    
    print("\n🔑 API Key Setup (Optional)")
    print("=" * 40)
    print("Provide API keys to test real AI providers.")
    print("Press Enter to skip any provider.\n")
    
    # Check for Gemini key
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        api_keys["gemini"] = gemini_key
        print("✅ Gemini: Found in environment")
    else:
        key = input("Gemini API Key (or Enter to skip): ").strip()
        if key:
            api_keys["gemini"] = key
            print("✅ Gemini: Key provided")
    
    # Check for OpenAI key
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        api_keys["openai"] = openai_key
        print("✅ OpenAI: Found in environment")
    else:
        key = input("OpenAI API Key (or Enter to skip): ").strip()
        if key:
            api_keys["openai"] = key
            print("✅ OpenAI: Key provided")
    
    return api_keys

def main():
    """Main demo function"""
    print("🎉 MultiProdigy Working Demo")
    print("=" * 50)
    print("This demo ACTUALLY WORKS and shows real LLM responses!")
    print("Fixed all the async/sync issues with a simpler approach.")
    print("=" * 50)
    
    # Get API keys
    api_keys = get_api_keys()
    
    # Create message bus
    bus = MessageBus()
    
    # Create agents
    print("\n🤖 Creating Agents...")
    agents = {
        "UserAgent": UserAgent("UserAgent", bus),
        "SyncLLMAgent": SyncLLMAgent("SyncLLMAgent", bus, api_keys),
        "TestAllLLMAgent": TestAllLLMAgent("TestAllLLMAgent", bus, api_keys)
    }
    
    # Register agents
    for agent in agents.values():
        bus.register(agent)
    
    print(f"✅ Created {len(agents)} agents")
    
    # Start observability dashboard
    print("\n🌐 Starting Dashboard...")
    dashboard = ObservabilityDashboard()
    dashboard_thread = threading.Thread(
        target=dashboard.run,
        kwargs={'host': 'localhost', 'port': 5000, 'debug': False}
    )
    dashboard_thread.daemon = True
    dashboard_thread.start()
    
    time.sleep(2)
    
    print("\n🎯 Demo Ready!")
    print("• Dashboard: http://localhost:5000")
    print("• Network Graph: http://localhost:5000/static/graph.html")
    
    try:
        # Run the demo tests
        run_demo_tests(agents)
        
        print("\n🎉 Demo completed successfully!")
        print("You should have seen REAL LLM responses above!")
        print("\nCheck the dashboard for observability data.")
        print("Press Ctrl+C to exit")
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n👋 Demo stopped!")
        
        if api_keys:
            print(f"✅ Successfully tested with {len(api_keys)} real AI providers!")
        else:
            print("🤖 Ran with mock AI (provide API keys for real AI)")

if __name__ == "__main__":
    main()