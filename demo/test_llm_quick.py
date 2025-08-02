#!/usr/bin/env python3
"""
Quick LLM test to verify the system works
"""

import sys
import os
import asyncio

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from MultiProdigy.llm.factory import LLMFactory

async def quick_test():
    """Quick test of the LLM system"""
    print("🧪 Quick LLM System Test")
    print("=" * 30)
    
    # Test mock client (should always work)
    print("🤖 Testing Mock Client...")
    try:
        client = LLMFactory.create_mock()
        response = await client.generate("Hello, how are you?")
        print(f"✅ Mock Response: {response.content}")
        print(f"   Provider: {response.provider}, Model: {response.model}")
    except Exception as e:
        print(f"❌ Mock test failed: {e}")
        return False
    
    # Test Gemini if API key is available
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        print("\n🚀 Testing Gemini Client...")
        try:
            client = LLMFactory.create_gemini(api_key=gemini_key, timeout=10)
            response = await client.generate("What is artificial intelligence?")
            print(f"✅ Gemini Response: {response.content[:100]}...")
            print(f"   Provider: {response.provider}, Model: {response.model}")
        except Exception as e:
            print(f"❌ Gemini test failed: {e}")
    else:
        print("\n⚠️  No GEMINI_API_KEY found - skipping Gemini test")
    
    print("\n✅ LLM system is working!")
    return True

if __name__ == "__main__":
    success = asyncio.run(quick_test())
    if success:
        print("\n🎉 Ready to run the comprehensive demo!")
        print("Run: python demo/run_working_demo.py")
    else:
        print("\n❌ LLM system has issues - check the errors above")