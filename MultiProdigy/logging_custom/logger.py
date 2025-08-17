import logging
import sqlite3
import os
from datetime import datetime

class EnhancedLogger:
    """Enhanced logger with file and database logging"""
    
    def __init__(self, agent_name, log_file=None, db_path=None):
        self.agent_name = agent_name
        self.log_file = log_file or f"logs/agents/{agent_name}.log"
        self.db_path = db_path or "logs/database/multiprodigy_logs.db"
        
        # Create logs directory if it doesn't exist
        os.makedirs("logs/agents", exist_ok=True)
        os.makedirs("logs/system", exist_ok=True)
        
        # Set up Python logger
        self.logger = logging.getLogger(agent_name)
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create file handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Create formatter
        formatter = logging.Formatter(
            f'[%(levelname)s] %(asctime)s - {agent_name} - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        # Initialize database
        self._init_db()
    
    def _init_db(self):
    #Initialize SQLite database for logs
        try:
             with sqlite3.connect(self.db_path) as conn:
              conn.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT DEFAULT (datetime('now')),
                    agent_name TEXT,
                    level TEXT,
                    message TEXT
                )
            ''')
              conn.commit()
        except Exception as e:
                print(f"Warning: Could not initialize log database: {e}")

    
    def _log_to_db(self, level, message):
        """Log message to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO logs (agent_name, level, message) VALUES (?, ?, ?)",
                    (self.agent_name, level, message)
                )
                conn.commit()
        except Exception as e:
            print(f"Warning: Could not log to database: {e}")
    
    def info(self, message, extra=None):
     if extra:
        message = f"{message} | extra: {extra}"
     self.logger.info(message)
     self._log_to_db("INFO", message)

    
    def error(self, message, extra=None):
     if extra:
        message = f"{message} | extra: {extra}"
     self.logger.error(message)
     self._log_to_db("ERROR", message)

    def warning(self, message, extra=None):
     if extra:
        message = f"{message} | extra: {extra}"
     self.logger.warning(message)
     self._log_to_db("WARNING", message)

    def debug(self, message, extra=None):
     if extra:
        message = f"{message} | extra: {extra}"
     self.logger.debug(message)
     self._log_to_db("DEBUG", message)


def get_logger(agent_name, log_file=None, db_path=None):
    """Return an EnhancedLogger instance (used across the project)."""
    return EnhancedLogger(agent_name, log_file=log_file, db_path=db_path)

def setup_logger(agent_name, log_file=None, db_path=None):
    """Alias for backward compatibility."""
    return get_logger(agent_name, log_file=log_file, db_path=db_path)
