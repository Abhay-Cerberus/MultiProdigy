# main.py
from MultiProdigy.agents.task_manager_agent import TaskManagerAgent
from MultiProdigy.schemas.agent_config import AgentConfig

if __name__ == "__main__":
    config = AgentConfig(name="TaskManagerAgent", role="manager", goal="Manage all tasks")
    agent = TaskManagerAgent(config=config)
    agent.run()
