import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


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
            "start_time": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
            "status": "started",
        }

        self.current_traces[trace_id] = trace_data
        self._write_log(trace_data)
        return trace_id

    def end_trace(self, trace_id: str, result: Optional[Dict] = None, error: Optional[str] = None):
        """End a trace with result or error"""
        if trace_id not in self.current_traces:
            return

        trace_data = self.current_traces[trace_id].copy()
        trace_data.update(
            {
                "end_time": datetime.now(timezone.utc).isoformat(),
                "duration_ms": self._calculate_duration(trace_data["start_time"]),
                "status": "error" if error else "completed",
                "result": result,
                "error": error,
            }
        )

        self._write_log(trace_data)
        del self.current_traces[trace_id]

    def log_message_event(self, sender: str, receiver: str, content: str, message_id: str = None):
        """Log a message passing event"""
        event_data = {
            "event_type": "message_sent",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sender": sender,
            "receiver": receiver,
            "message_id": message_id or str(uuid.uuid4()),
            "content_length": len(content),
            "content_preview": content[:100] + "..." if len(content) > 100 else content,
        }

        self._write_log(event_data)
        return event_data["message_id"]

    def _write_log(self, data: Dict[str, Any]):
        """Write log entry to file"""
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(data) + "\n")
        except Exception as e:
            print(f"Warning: Could not write to log file {self.log_file}: {e}")

    def _calculate_duration(self, start_time: str) -> float:
        """Calculate duration in milliseconds"""
        try:
            start = datetime.fromisoformat(start_time)
            end = datetime.now(timezone.utc)
            return (end - start).total_seconds() * 1000
        except Exception:
            return 0.0


# Global tracer instance
tracer = AgentTracer()
