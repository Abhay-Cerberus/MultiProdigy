import json
import time
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
import psutil  # ✅ Added for system metrics

class AgentTracer:
    """Structured logging and tracing for MultiProdigy agents"""
    
    def __init__(self, log_file: str = "agent_traces.jsonl"):
        self.log_file = Path(log_file)
        self.current_traces: Dict[str, Dict] = {}
        
    def start_trace(self, agent_name: str, event_type: str, metadata: Optional[Dict] = None) -> str:
        """Start a new trace for an agent event"""
        trace_id = str(uuid.uuid4())
        
        trace_data = {
            "trace_id": trace_id,
            "agent_name": agent_name,
            "event_type": event_type,
            "start_time": datetime.utcnow().isoformat(),
            "metadata": metadata or {},
            "status": "started"
        }
        
        self.current_traces[trace_id] = trace_data
        self._write_log(trace_data)
        return trace_id
    
    def end_trace(self, trace_id: str, result: Optional[Dict] = None, error: Optional[str] = None):
        """End a trace with result or error"""
        if trace_id not in self.current_traces:
            return
            
        trace_data = self.current_traces[trace_id].copy()
        trace_data.update({
            "end_time": datetime.utcnow().isoformat(),
            "duration_ms": self._calculate_duration(trace_data["start_time"]),
            "status": "error" if error else "completed",
            "result": result,
            "error": error
        })
        
        self._write_log(trace_data)
        del self.current_traces[trace_id]
    
    def log_message_event(self, sender: str, receiver: str, content: str, message_id: str = None):
        """Log a message passing event"""
        event_data = {
            "event_type": "message_sent",
            "timestamp": datetime.utcnow().isoformat(),
            "sender": sender,
            "receiver": receiver,
            "message_id": message_id or str(uuid.uuid4()),
            "content_length": len(content),
            "content_preview": content[:100] + "..." if len(content) > 100 else content
        }
        
        self._write_log(event_data)
        return event_data["message_id"]

    def log_system_metrics(self):
        """Log current CPU and memory usage"""
        mem = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=0.1)

        metrics_data = {
            "event_type": "system_metrics",
            "timestamp": datetime.utcnow().isoformat(),
            "cpu_percent": cpu,
            "memory_percent": mem.percent,
            "available_memory_mb": round(mem.available / (1024 * 1024), 2),
        }

        self._write_log(metrics_data)
    
    def _write_log(self, data: Dict[str, Any]):
        """Write log entry to file"""
        with open(self.log_file, "a") as f:
            f.write(json.dumps(data) + "\n")
    
    def _calculate_duration(self, start_time: str) -> float:
        """Calculate duration in milliseconds"""
        start = datetime.fromisoformat(start_time)
        end = datetime.utcnow()
        return (end - start).total_seconds() * 1000

# Global tracer instance
tracer = AgentTracer()
