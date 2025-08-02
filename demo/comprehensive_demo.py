#!/usr/bin/env python3
"""
MultiProdigy Comprehensive Demo

This demo showcases EVERYTHING MultiProdigy has to offer:
1. Unified LLM system with Gemini API integration
2. Multi-agent communication with observability
3. Real-time dashboard and network visualization
4. Structured logging and tracing
5. Error handling and recovery

Run this demo and provide your Gemini API key to see the full system in action!
"""

import sys
import os
import time
import asyncio
import threading
from typing import Optional

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from MultiProdigy.agents.agent_base import BaseAgent
from MultiProdigy.bus.message_bus import MessageBus
from MultiProdigy.schemas.message import Message
from MultiProdigy.observability.dashboard import ObservabilityDashboard
from MultiProdigy.llm.factory import LLMFactory
from MultiProdigy.llm.base import LLMProvider

class AIResearchAgent(BaseAgent):
    """AI-powered research agent using Gemini API"""
    
    def __init__(self, name: str, bus: MessageBus, gemini_api_key: Optional[str] = None):
        super().__init__(name, bus)
        
        # Initialize LLM client
        if gemini_api_key:
            print(f"🚀 [{self.name}] Initializing with real Gemini API")
            self.llm = LLMFactory.create_gemini(
                model="gemini-2.0-flash-exp",
                api_key=gemini_api_key,
                temperature=0.7,
                max_tokens=300
            )
            self.use_real_ai = True
        else:
            print(f"🤖 [{self.name}] Using mock AI (no API key provided)")
            self.llm = LLMFactory.create_mock(model="mock-research-ai")
            self.use_real_ai = False
    
    async def on_message(self, message: Message) -> None:
        """Process research requests using AI"""
        print(f"🔬 [{self.name}] Researching: {message.content}")
        
        try:
            # Use AI to generate research response
            prompt = f"""
            You are an expert research assistant. Please provide a comprehensive but concise response to this research request:
            
            Request: {message.content}
            
            Please provide:
            1. Key insights
            2. Important considerations
            3. Recommended next steps
            
            Keep your response informative but under 200 words.
            """
            
            # Generate AI response
            response = await self.llm.generate(prompt)
            ai_content = response.content
            
            # Add metadata about the AI response
            if self.use_real_ai:
                result = f"🧠 AI Research Results (Gemini 2.0):\n\n{ai_content}"
            else:
                result = f"🤖 Mock AI Research Results:\n\n{ai_content}"
            
            # Send results back
            self.send(result, message.sender)
            
        except Exception as e:
            error_msg = f"❌ Research failed: {str(e)}"
            print(f"🚨 [{self.name}] {error_msg}")
            self.send(error_msg, message.sender)

class DataAnalysisAgent(BaseAgent):
    """AI-powered data analysis agent"""
    
    def __init__(self, name: str, bus: MessageBus, gemini_api_key: Optional[str] = None):
        super().__init__(name, bus)
        
        if gemini_api_key:
            print(f"📊 [{self.name}] Initializing with real Gemini API")
            self.llm = LLMFactory.create_gemini(
                model="gemini-2.0-flash-exp",
                api_key=gemini_api_key,
                temperature=0.3,  # Lower temperature for analysis
                max_tokens=400
            )
            self.use_real_ai = True
        else:
            print(f"📈 [{self.name}] Using mock AI (no API key provided)")
            self.llm = LLMFactory.create_mock(model="mock-analysis-ai")
            self.use_real_ai = False
    
    async def on_message(self, message: Message) -> None:
        """Analyze data using AI"""
        print(f"📊 [{self.name}] Analyzing: {message.content}")
        
        try:
            prompt = f"""
            You are a data analysis expert. Please analyze the following request and provide insights:
            
            Analysis Request: {message.content}
            
            Please provide:
            1. Data interpretation
            2. Key patterns or trends
            3. Statistical insights
            4. Actionable recommendations
            
            Be specific and data-driven in your response.
            """
            
            response = await self.llm.generate(prompt)
            ai_content = response.content
            
            if self.use_real_ai:
                result = f"📈 AI Data Analysis (Gemini 2.0):\n\n{ai_content}"
            else:
                result = f"📊 Mock Data Analysis:\n\n{ai_content}"
            
            self.send(result, message.sender)
            
        except Exception as e:
            error_msg = f"❌ Analysis failed: {str(e)}"
            print(f"🚨 [{self.name}] {error_msg}")
            self.send(error_msg, message.sender)

class ProjectManagerAgent(BaseAgent):
    """AI-powered project management agent"""
    
    def __init__(self, name: str, bus: MessageBus, gemini_api_key: Optional[str] = None):
        super().__init__(name, bus)
        
        if gemini_api_key:
            print(f"📋 [{self.name}] Initializing with real Gemini API")
            self.llm = LLMFactory.create_gemini(
                model="gemini-2.0-flash-exp",
                api_key=gemini_api_key,
                temperature=0.5,
                max_tokens=350
            )
            self.use_real_ai = True
        else:
            print(f"📝 [{self.name}] Using mock AI (no API key provided)")
            self.llm = LLMFactory.create_mock(model="mock-pm-ai")
            self.use_real_ai = False
        
        self.project_context = []
    
    async def on_message(self, message: Message) -> None:
        """Manage projects using AI"""
        print(f"📋 [{self.name}] Managing: {message.content}")
        
        try:
            # Add to project context
            self.project_context.append(message.content)
            
            # Create context-aware prompt
            context = "\n".join(self.project_context[-5:])  # Last 5 messages
            
            prompt = f"""
            You are an experienced project manager. Based on the following project context, provide management guidance:
            
            Recent Context:
            {context}
            
            Current Request: {message.content}
            
            Please provide:
            1. Project status assessment
            2. Risk analysis
            3. Resource recommendations
            4. Next action items
            
            Be practical and actionable in your response.
            """
            
            response = await self.llm.generate(prompt)
            ai_content = response.content
            
            if self.use_real_ai:
                result = f"📋 AI Project Management (Gemini 2.0):\n\n{ai_content}"
            else:
                result = f"📝 Mock Project Management:\n\n{ai_content}"
            
            self.send(result, message.sender)
            
        except Exception as e:
            error_msg = f"❌ Project management failed: {str(e)}"
            print(f"🚨 [{self.name}] {error_msg}")
            self.send(error_msg, message.sender)

class UserAgent(BaseAgent):
    """User agent that coordinates with AI agents"""
    
    def __init__(self, name: str, bus: MessageBus):
        super().__init__(name, bus)
        self.task_count = 0
        self.responses_received = 0
    
    def on_message(self, message: Message) -> None:
        """Receive responses from AI agents"""
        self.responses_received += 1
        print(f"👤 [{self.name}] Received response #{self.responses_received}:")
        print(f"   From: {message.sender}")
        print(f"   Content: {message.content[:100]}...")
        print()
    
    def send_research_request(self):
        """Send a research request"""
        self.task_count += 1
        requests = [
            "Research the latest trends in artificial intelligence and machine learning",
            "Investigate the impact of quantum computing on cybersecurity",
            "Analyze the future of renewable energy technologies",
            "Study the effects of remote work on productivity and collaboration",
            "Research emerging technologies in healthcare and biotechnology"
        ]
        
        request = requests[(self.task_count - 1) % len(requests)]
        print(f"👤 [{self.name}] Sending research request #{self.task_count}: {request}")
        self.send(request, "AIResearchAgent")
    
    def send_analysis_request(self):
        """Send a data analysis request"""
        self.task_count += 1
        requests = [
            "Analyze user engagement metrics for our mobile application",
            "Examine sales performance trends over the last quarter",
            "Evaluate the effectiveness of our marketing campaigns",
            "Study customer satisfaction survey results",
            "Analyze website traffic patterns and user behavior"
        ]
        
        request = requests[(self.task_count - 1) % len(requests)]
        print(f"👤 [{self.name}] Sending analysis request #{self.task_count}: {request}")
        self.send(request, "DataAnalysisAgent")
    
    def send_project_request(self):
        """Send a project management request"""
        self.task_count += 1
        requests = [
            "Plan the development timeline for our new product launch",
            "Assess risks for the upcoming software migration project",
            "Coordinate resources for the Q2 marketing campaign",
            "Manage the integration of new team members",
            "Oversee the implementation of new security protocols"
        ]
        
        request = requests[(self.task_count - 1) % len(requests)]
        print(f"👤 [{self.name}] Sending project request #{self.task_count}: {request}")
        self.send(request, "ProjectManagerAgent")

async def simulate_intelligent_activity(agents, gemini_api_key: Optional[str], duration_seconds=120):
    """Simulate realistic AI-powered agent interactions"""
    user_agent = agents["UserAgent"]
    
    print(f"🎬 Starting intelligent agent simulation for {duration_seconds} seconds...")
    if gemini_api_key:
        print("🚀 Using REAL Gemini API - you'll see actual AI responses!")
    else:
        print("🤖 Using mock AI - provide GEMINI_API_KEY for real AI responses")
    
    start_time = time.time()
    request_count = 0
    
    while time.time() - start_time < duration_seconds:
        request_count += 1
        
        # Rotate between different types of requests
        if request_count % 3 == 1:
            user_agent.send_research_request()
        elif request_count % 3 == 2:
            user_agent.send_analysis_request()
        else:
            user_agent.send_project_request()
        
        # Wait between requests (shorter for more activity)
        await asyncio.sleep(8)
    
    print(f"✨ Simulation completed! Sent {request_count} intelligent requests.")

def get_gemini_api_key():
    """Get Gemini API key from user or environment"""
    # First check environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print(f"✅ Found Gemini API key in environment variable")
        return api_key
    
    # Ask user for API key
    print("\n🔑 Gemini API Key Setup")
    print("=" * 40)
    print("To see REAL AI responses, please provide your Gemini API key.")
    print("You can get one free at: https://makersuite.google.com/app/apikey")
    print("\nOptions:")
    print("1. Enter your API key now")
    print("2. Set GEMINI_API_KEY environment variable")
    print("3. Skip (use mock AI responses)")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == "1":
        api_key = input("Enter your Gemini API key: ").strip()
        if api_key:
            return api_key
    elif choice == "2":
        print("Set the environment variable and restart the demo:")
        print("export GEMINI_API_KEY='your-api-key-here'")
        return None
    
    print("🤖 Proceeding with mock AI responses")
    return None

def main():
    """Main comprehensive demo function"""
    print("🎉 MultiProdigy Comprehensive Demo")
    print("=" * 60)
    print("This demo showcases EVERYTHING MultiProdigy offers:")
    print("• Unified LLM system with Gemini 2.0 integration")
    print("• Multi-agent AI communication")
    print("• Real-time observability dashboard")
    print("• Network visualization")
    print("• Structured logging and tracing")
    print("• Error handling and recovery")
    print("=" * 60)
    
    # Get Gemini API key
    gemini_api_key = get_gemini_api_key()
    
    # Create message bus
    bus = MessageBus()
    
    # Create AI-powered agents
    print("\n🤖 Initializing AI-Powered Agents...")
    agents = {
        "UserAgent": UserAgent("UserAgent", bus),
        "AIResearchAgent": AIResearchAgent("AIResearchAgent", bus, gemini_api_key),
        "DataAnalysisAgent": DataAnalysisAgent("DataAnalysisAgent", bus, gemini_api_key),
        "ProjectManagerAgent": ProjectManagerAgent("ProjectManagerAgent", bus, gemini_api_key)
    }
    
    # Register agents with bus
    for agent in agents.values():
        bus.register(agent)
    
    print("\n✅ Created AI-powered agents:")
    for name in agents.keys():
        print(f"   • {name}")
    
    # Start observability dashboard
    print("\n🌐 Starting Observability Dashboard...")
    dashboard = ObservabilityDashboard()
    dashboard_thread = threading.Thread(
        target=dashboard.run,
        kwargs={'host': 'localhost', 'port': 5000, 'debug': False}
    )
    dashboard_thread.daemon = True
    dashboard_thread.start()
    
    # Wait for dashboard to start
    time.sleep(2)
    
    print("\n🎬 Starting AI Agent Simulation...")
    print("=" * 60)
    print("DEMO FEATURES:")
    print("1. 🌐 Dashboard: http://localhost:5000")
    print("2. 🕸️ Network Graph: http://localhost:5000/static/graph.html")
    print("3. 🤖 AI-powered agent responses (real or mock)")
    print("4. 📊 Real-time metrics and timeline")
    print("5. 🔍 Structured logging and tracing")
    print("6. ⚡ Live network visualization")
    print("=" * 60)
    
    # Start intelligent activity simulation
    try:
        asyncio.run(simulate_intelligent_activity(agents, gemini_api_key, 120))
        
        print("\n✨ Demo completed! Dashboard is still running.")
        print("🌐 Explore the web interfaces:")
        print("   • Dashboard: http://localhost:5000")
        print("   • Network Graph: http://localhost:5000/static/graph.html")
        print("\n📊 Check the agent_traces.jsonl file for detailed logs")
        print("Press Ctrl+C to exit")
        
        # Keep dashboard running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n👋 Demo stopped. Thanks for exploring MultiProdigy!")
        print("\n🎯 What you experienced:")
        print("✅ Unified LLM architecture with Pydantic configuration")
        print("✅ Real-time agent communication with AI integration")
        print("✅ Complete observability with dashboard and graphs")
        print("✅ Structured logging and performance tracing")
        print("✅ Error handling and recovery mechanisms")
        
        if gemini_api_key:
            print("✅ Real Gemini 2.0 AI responses!")
        else:
            print("🤖 Mock AI responses (provide API key for real AI)")

if __name__ == "__main__":
    main()