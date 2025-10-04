from typing import Optional

from pydantic import BaseModel


class AgentConfig(BaseModel):
    name: str
    role: str = "default"
    goal: str = "default goal"


class Settings(BaseModel):
    agent_name: str = "TestAgent"
    agent_role: str = "default"
    agent_goal: str = "default goal"

    # Simple config without pydantic_settings dependency
    @classmethod
    def from_env(cls, env_file: Optional[str] = ".env"):
        """Load settings from environment or file"""
        import os

        if env_file and os.path.exists(env_file):
            # Simple .env file parsing
            config = {}
            with open(env_file) as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        config[key.lower()] = value
            return cls(**config)
        return cls()
