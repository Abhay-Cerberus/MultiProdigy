from MultiProdigy.agents.task_manager_agent import TaskManagerAgent
from MultiProdigy.runtime.engine import MessageBus
from MultiProdigy.schemas.agent_config import AgentConfig

# Step 1: Create message bus instance
message_bus = MessageBus()

# Step 2: Define agent config (ensure name is passed)
config = AgentConfig(name="TaskManager", max_tasks=5, retry_delay=2)

# Step 3: Create and run the agent
agent = TaskManagerAgent(config=config, bus=message_bus)
agent.run()

# Simulate sending a test message
agent.on_message("Test task message from main")
