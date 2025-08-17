from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    log_file_path: str = "logs/system.log"
    log_level: str = "INFO"
    log_dir: str = "logs"
    db_path: str = "MultiProdigy/logs/multiprodigy_logs.db"
    enable_ollama_agent: bool = True
    enable_echo_agent: bool = True

    class Config:
        extra = "ignore"

settings = Settings()
