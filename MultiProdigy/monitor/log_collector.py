# MultiProdigy/monitor/log_collector.py

import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import threading
import time

class DatabaseManager:
    """Manages SQLite database operations for log storage"""
    
    def __init__(self, db_path: str = "multiprodigy_logs.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with proper schema"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Drop existing table if it has wrong schema
                cursor.execute("DROP TABLE IF EXISTS logs")
                
                # Create logs table with correct schema
                cursor.execute("""
                    CREATE TABLE logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        agent_name TEXT NOT NULL,
                        level TEXT NOT NULL DEFAULT 'INFO',
                        message TEXT NOT NULL,
                        extra_data TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create indexes for better performance
                cursor.execute("CREATE INDEX idx_timestamp ON logs(timestamp)")
                cursor.execute("CREATE INDEX idx_agent_name ON logs(agent_name)")
                cursor.execute("CREATE INDEX idx_level ON logs(level)")
                
                conn.commit()
                print("[INFO] Database initialized successfully")
                
        except Exception as e:
            print(f"[ERROR] Database initialization failed: {e}")
    
    def insert_log(self, log_data: Dict[str, Any]) -> bool:
        """Insert a log entry into the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Ensure all required fields are present
                timestamp = log_data.get('timestamp') or datetime.now().isoformat()
                agent_name = log_data.get('agent_name', 'Unknown')
                level = log_data.get('level', 'INFO')
                message = log_data.get('message', '')
                extra_data = json.dumps(log_data.get('extra_data', {}))
                
                cursor.execute("""
                    INSERT INTO logs (timestamp, agent_name, level, message, extra_data)
                    VALUES (?, ?, ?, ?, ?)
                """, (timestamp, agent_name, level, message, extra_data))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"[ERROR] Failed to insert log: {e}")
            return False
    
    def get_logs(self, limit: int = 100, agent_filter: Optional[str] = None, 
                 level_filter: Optional[str] = None) -> List[Dict]:
        """Retrieve logs from database with optional filtering"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM logs WHERE 1=1"
                params = []
                
                if agent_filter:
                    query += " AND agent_name = ?"
                    params.append(agent_filter)
                
                if level_filter:
                    query += " AND level = ?"
                    params.append(level_filter)
                
                query += " ORDER BY created_at DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                
                columns = [desc[0] for desc in cursor.description]
                logs = []
                
                for row in cursor.fetchall():
                    log_dict = dict(zip(columns, row))
                    # Parse extra_data JSON
                    try:
                        log_dict['extra_data'] = json.loads(log_dict['extra_data'] or '{}')
                    except:
                        log_dict['extra_data'] = {}
                    logs.append(log_dict)
                
                return logs
                
        except Exception as e:
            print(f"[ERROR] Failed to retrieve logs: {e}")
            return []

class LogCollector:
    """Collects and processes logs from the MultiProdigy system"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.handlers = []
        self.running = False
        self.setup_logging_handler()
    
    def setup_logging_handler(self):
        """Setup custom logging handler to capture all logs"""
        
        class MultiProdigyLogHandler(logging.Handler):
            def __init__(self, collector):
                super().__init__()
                self.collector = collector
            
            def emit(self, record):
                try:
                    # Extract information from log record
                    log_data = {
                        'timestamp': datetime.fromtimestamp(record.created).isoformat(),
                        'agent_name': record.name,
                        'level': record.levelname,
                        'message': record.getMessage(),
                        'extra_data': {
                            'module': record.module,
                            'funcName': record.funcName,
                            'lineno': record.lineno,
                            'pathname': record.pathname
                        }
                    }
                    
                    # Add any extra fields from the record
                    if hasattr(record, 'extra'):
                        log_data['extra_data'].update(record.extra)
                    
                    self.collector.store_log(log_data)
                    
                except Exception as e:
                    print(f"Log collection error: {e}")
        
        # Add our custom handler to the root logger
        handler = MultiProdigyLogHandler(self)
        handler.setLevel(logging.INFO)
        
        # Get the root logger and add our handler
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.INFO)
    
    def store_log(self, log_data: Dict[str, Any]):
        """Store log data in database"""
        success = self.db.insert_log(log_data)
        if not success:
            print(f"Failed to store log: {log_data.get('message', 'Unknown message')}")
    
    def get_logs(self, limit: int = 100, agent_filter: str = None, 
                 level_filter: str = None) -> List[Dict]:
        """Retrieve logs with optional filtering"""
        return self.db.get_logs(limit, agent_filter, level_filter)
    
    def get_agents(self) -> List[str]:
        """Get list of unique agent names"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT agent_name FROM logs ORDER BY agent_name")
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting agents: {e}")
            return []
    
    def get_log_levels(self) -> List[str]:
        """Get list of unique log levels"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT level FROM logs ORDER BY level")
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting log levels: {e}")
            return []
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get system metrics and statistics"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Total log count
                cursor.execute("SELECT COUNT(*) FROM logs")
                total_logs = cursor.fetchone()[0]
                
                # Logs by level
                cursor.execute("SELECT level, COUNT(*) FROM logs GROUP BY level")
                logs_by_level = dict(cursor.fetchall())
                
                # Logs by agent
                cursor.execute("SELECT agent_name, COUNT(*) FROM logs GROUP BY agent_name")
                logs_by_agent = dict(cursor.fetchall())
                
                # Recent activity (last hour)
                cursor.execute("""
                    SELECT COUNT(*) FROM logs 
                    WHERE datetime(created_at) > datetime('now', '-1 hour')
                """)
                recent_activity = cursor.fetchone()[0]
                
                return {
                    'total_logs': total_logs,
                    'logs_by_level': logs_by_level,
                    'logs_by_agent': logs_by_agent,
                    'recent_activity': recent_activity,
                    'active_agents': len(logs_by_agent)
                }
                
        except Exception as e:
            print(f"Error getting metrics: {e}")
            return {
                'total_logs': 0,
                'logs_by_level': {},
                'logs_by_agent': {},
                'recent_activity': 0,
                'active_agents': 0
            }
    
    def start(self):
        """Start the log collector"""
        self.running = True
        print("[INFO] Log collector started")
    
    def stop(self):
        """Stop the log collector"""
        self.running = False
        print("[INFO] Log collector stopped")
    
    def generate_sample_data(self):
        """Generate sample log data for testing"""
        sample_logs = [
            {
                'timestamp': datetime.now().isoformat(),
                'agent_name': 'TestAgent',
                'level': 'INFO',
                'message': 'Sample log entry for testing dashboard',
                'extra_data': {'test': True, 'sample_id': 1}
            },
            {
                'timestamp': datetime.now().isoformat(),
                'agent_name': 'DataAgent',
                'level': 'WARNING',
                'message': 'Sample warning message',
                'extra_data': {'warning_type': 'performance', 'sample_id': 2}
            },
            {
                'timestamp': datetime.now().isoformat(),
                'agent_name': 'NetworkAgent',
                'level': 'ERROR',
                'message': 'Sample error for visualization',
                'extra_data': {'error_code': 500, 'sample_id': 3}
            }
        ]
        
        for log_data in sample_logs:
            self.store_log(log_data)
        
        print("[INFO] Sample log data generated")

# Global log collector instance
log_collector = LogCollector()
