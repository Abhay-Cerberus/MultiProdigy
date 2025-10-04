import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set


class AgentGraphBuilder:
    """Converts agent traces into graph visualization data"""

    def __init__(self, log_file: str = "agent_traces.jsonl"):
        self.log_file = Path(log_file)

    def build_graph_data(self, time_window_minutes: int = 60) -> Dict[str, Any]:
        """Build graph data from recent traces"""
        traces = self._load_recent_traces(time_window_minutes)

        nodes = self._extract_nodes(traces)
        edges = self._extract_edges(traces)

        return {
            "nodes": list(nodes.values()),
            "edges": edges,
            "metadata": {
                "total_messages": len(edges),
                "active_agents": len(nodes),
                "time_window_minutes": time_window_minutes,
            },
        }

    def _load_recent_traces(self, time_window_minutes: int) -> List[Dict]:
        """Load traces from the specified time window"""
        if not self.log_file.exists():
            return []

        traces = []
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        trace = json.loads(line.strip())
                        traces.append(trace)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"Warning: Could not read log file {self.log_file}: {e}")
            return []

        # For now, return all traces (time filtering can be added later)
        return traces

    def _extract_nodes(self, traces: List[Dict]) -> Dict[str, Dict]:
        """Extract agent nodes from traces"""
        nodes = {}
        agent_stats = defaultdict(
            lambda: {
                "message_count": 0,
                "error_count": 0,
                "avg_duration": 0,
                "status": "idle",
                "last_seen": None,
            }
        )

        # Collect agent statistics
        for trace in traces:
            if trace.get("event_type") == "message_sent":
                sender = trace.get("sender")
                receiver = trace.get("receiver")
                timestamp = trace.get("timestamp")

                if sender:
                    agent_stats[sender]["message_count"] += 1
                    agent_stats[sender]["last_seen"] = timestamp
                if receiver:
                    agent_stats[receiver]["message_count"] += 1
                    agent_stats[receiver]["last_seen"] = timestamp

            elif trace.get("event_type") in ["message_received", "message_processing"]:
                agent_name = trace.get("agent_name")
                if agent_name:
                    if trace.get("status") == "error":
                        agent_stats[agent_name]["error_count"] += 1
                        agent_stats[agent_name]["status"] = "error"

                    duration = trace.get("duration_ms", 0)
                    if duration > 0:
                        current_avg = agent_stats[agent_name]["avg_duration"]
                        agent_stats[agent_name]["avg_duration"] = (current_avg + duration) / 2

                    # Determine status
                    if trace.get("status") == "started":
                        agent_stats[agent_name]["status"] = "processing"
                    elif (
                        trace.get("status") == "completed"
                        and agent_stats[agent_name]["status"] != "error"
                    ):
                        agent_stats[agent_name]["status"] = "active"

                    agent_stats[agent_name]["last_seen"] = trace.get("start_time") or trace.get(
                        "timestamp"
                    )

        # Create node objects
        for agent_name, stats in agent_stats.items():
            nodes[agent_name] = {
                "id": agent_name,
                "type": "agent",
                "label": agent_name,
                "status": stats["status"],
                "message_count": stats["message_count"],
                "error_count": stats["error_count"],
                "avg_duration_ms": round(stats["avg_duration"], 2),
                "size": min(20 + stats["message_count"] * 3, 60),  # Visual size based on activity
                "last_seen": stats["last_seen"],
            }

        return nodes

    def _extract_edges(self, traces: List[Dict]) -> List[Dict]:
        """Extract message edges from traces"""
        edges = []

        for trace in traces:
            if trace.get("event_type") == "message_sent":
                edge = {
                    "id": trace.get(
                        "message_id", f"{trace.get('sender')}-{trace.get('receiver')}-{len(edges)}"
                    ),
                    "source": trace.get("sender"),
                    "target": trace.get("receiver"),
                    "timestamp": trace.get("timestamp"),
                    "content_preview": trace.get("content_preview", ""),
                    "content_length": trace.get("content_length", 0),
                    "type": "message",
                }
                edges.append(edge)

        return edges

    def get_agent_details(self, agent_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific agent"""
        traces = self._load_recent_traces(60)

        agent_traces = [
            t
            for t in traces
            if t.get("agent_name") == agent_name
            or t.get("sender") == agent_name
            or t.get("receiver") == agent_name
        ]

        return {
            "agent_name": agent_name,
            "total_events": len(agent_traces),
            "recent_traces": agent_traces[-10:],  # Last 10 events
            "message_history": [t for t in agent_traces if t.get("event_type") == "message_sent"],
        }
