from pydantic import BaseModel

class AgentConfig(BaseModel):
    name: str
    max_tasks: int = 5
    retry_delay: int = 2
