#!/usr/bin/env python3
"""
MultiProdigy Observability Demo

This demo shows how to use the observability features:
1. Agents with automatic tracing
2. Dashboard for monitoring
3. Graph visualization

Run this script and then open:
- Dashboard: http://localhost:5000
- Graph: http://localhost:5000/static/graph.html
"""

import sys
import os
import time
import threading

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from MultiProdigy.agents.agent_base import BaseAgent
from MultiProdigy.bus.message_bus import MessageBus
from MultiProdigy.schemas.message import Message
from MultiProdigy.observability.dashboard import ObservabilityDashboard

class DemoUserAgent(BaseAgent):
    """Simulates a user sending tasks"""
    
    def __init__(self, name: str, bus: MessageBus):
        super().__init__(name, bus)
        self.task_count = 0
    
    def on_message(self, message: Message) -> None:
        print(f"[{self.name}] Received response: {message.content}")
    
    def send_task(self):
        """Send a task to the task manager"""
        self.task_count += 1
        task = f"Process task #{self.task_count}"
        print(f"[{self.name}] Sending: {task}")
        self.send(task, "TaskManagerAgent")

class DemoTaskManagerAgent(BaseAgent):
    """Simulates a task manager processing requests"""
    
    def on_message(self, message: Message) -> None:
        print(f"[{self.name}] Processing: {message.content}")
        
        # Simulate processing time
        time.sleep(0.5)
        
        # Sometimes forward to worker
        if "complex" in message.content.lower():
            self.send(f"Handle: {message.content}", "WorkerAgent")
        else:
            # Send response back
            response = f"Completed: {message.content}"
            self.send(response, message.sender)

class DemoWorkerAgent(BaseAgent):
    """Simulates a worker handling complex tasks"""
    
    def on_message(self, message: Message) -> None:
        print(f"[{self.name}] Working on: {message.content}")
        
        # Simulate longer processing
        time.sleep(1.0)
        
        # Sometimes fail to demonstrate error tracking
        if "error" in message.content.lower():
            raise Exception("Simulated processing error")
        
        # Send result back to task manager
        result = f"Worker completed: {message.content}"
        self.send(result, "TaskManagerAgent")

def simulate_agent_activity(agents, duration_seconds=60):
    """Simulate agent activity for demo purposes"""
    user_agent = agents["UserAgent"]
    
    tasks = [
        "Simple task",
        "Complex data processing",
        "Generate report", 
        "Complex error task",  # This will cause an error
        "Backup database",
        "Complex analysis task"
    ]
    
    start_time = time.time()
    task_index = 0
    
    while time.time() - start_time < duration_seconds:
        # Send a task every 3-5 seconds
        task = tasks[task_index % len(tasks)]
        user_agent.send_task()
        
        task_index += 1
        time.sleep(3)
    
    print("Demo activity simulation completed!")

def main():
    print("🚀 Starting MultiProdigy Observability Demo")
    print("=" * 50)
    
    # Create message bus
    bus = MessageBus()
    
    # Create demo agents
    agents = {
        "UserAgent": DemoUserAgent("UserAgent", bus),
        "TaskManagerAgent": DemoTaskManagerAgent("TaskManagerAgent", bus),
        "WorkerAgent": DemoWorkerAgent("WorkerAgent", bus)
    }
    
    # Register agents with bus
    for agent in agents.values():
        bus.register(agent)
    
    print("✅ Created demo agents:")
    for name in agents.keys():
        print(f"   - {name}")
    
    # Start dashboard in background thread
    dashboard = ObservabilityDashboard()
    dashboard_thread = threading.Thread(
        target=dashboard.run,
        kwargs={'host': 'localhost', 'port': 5000, 'debug': False}
    )
    dashboard_thread.daemon = True
    dashboard_thread.start()
    
    print("\n🌐 Dashboard starting at http://localhost:5000")
    print("📊 Graph view at http://localhost:5000/static/graph.html")
    
    # Wait for dashboard to start
    time.sleep(2)
    
    print("\n🎬 Starting agent activity simulation...")
    print("   (This will run for 60 seconds)")
    
    # Start activity simulation in background
    activity_thread = threading.Thread(
        target=simulate_agent_activity,
        args=(agents, 60)
    )
    activity_thread.start()
    
    print("\n" + "=" * 50)
    print("DEMO INSTRUCTIONS:")
    print("1. Open http://localhost:5000 to see the dashboard")
    print("2. Open http://localhost:5000/static/graph.html for the network graph")
    print("3. Watch the real-time updates as agents communicate")
    print("4. Look for error events when 'error task' is processed")
    print("5. Press Ctrl+C to stop the demo")
    print("=" * 50)
    
    try:
        # Keep main thread alive
        activity_thread.join()
        
        print("\n✨ Demo completed! Dashboard is still running.")
        print("   Press Ctrl+C to exit")
        
        # Keep dashboard running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n👋 Demo stopped. Thanks for trying MultiProdigy Observability!")

if __name__ == "__main__":
    main()