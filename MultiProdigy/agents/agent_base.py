import sys
import os
import time
from datetime import datetime

# Add root directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from MultiProdigy.logging_custom.logger import get_logger


class AgentBase:
    """Base class for all agents with enhanced logging and task tracking."""
    
    def __init__(self, agent_name=None):
        self.agent_name = agent_name or self.__class__.__name__
        self.logger = get_logger(self.agent_name)
        self.task_counter = 0
        self.start_time = datetime.now()

        self.logger.info(
            f"Agent {self.agent_name} initialized",
            {
                'agent_type': self.__class__.__name__,
                'start_time': self.start_time.isoformat()
            }
        )

    def execute_task(self, task):
        """Execute a task with logging and timing."""
        self.task_counter += 1
        task_id = f"{self.agent_name}_task_{self.task_counter}"
        
        self.logger.info(
            f"Starting task execution",
            {
                'task_id': task_id,
                'task_type': type(task).__name__
            }
        )
        
        start_time = time.time()
        
        try:
            result = self._execute_task_internal(task)
            execution_time = time.time() - start_time
            
            self.logger.info(
                f"Task completed successfully",
                {
                    'task_id': task_id,
                    'execution_time': execution_time,
                    'result_type': type(result).__name__
                }
            )
            return result
        
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(
                f"Task execution failed",
                {
                    'task_id': task_id,
                    'error': str(e),
                    'execution_time': execution_time,
                    'error_type': type(e).__name__
                }
            )
            raise

    def _execute_task_internal(self, task):
        """Override this in specific agents."""
        pass

    def log_agent_status(self):
        """Log the agent's current status."""
        uptime = (datetime.now() - self.start_time).total_seconds()
        self.logger.info(
            f"Agent status report",
            {
                'uptime_seconds': uptime,
                'tasks_completed': self.task_counter,
                'status': 'active'
            }
        )
