import pytest
import json
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock, patch

from MultiProdigy.observability.tracer import AgentTracer
from MultiProdigy.observability.dashboard import ObservabilityDashboard
from MultiProdigy.observability.graph_builder import AgentGraphBuilder
from MultiProdigy.agents.agent_base import BaseAgent
from MultiProdigy.bus.message_bus import MessageBus
from MultiProdigy.schemas.message import Message

class TestAgentTracer:
    """Test the core tracing functionality"""
    
    def setup_method(self):
        """Setup test environment"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl')
        self.temp_file.close()
        self.tracer = AgentTracer(log_file=self.temp_file.name)
    
    def teardown_method(self):
        """Cleanup test environment"""
        Path(self.temp_file.name).unlink(missing_ok=True)
    
    def test_start_trace(self):
        """Test trace creation"""
        trace_id = self.tracer.start_trace("TestAgent", "test_event", {"key": "value"})
        
        assert trace_id is not None
        assert trace_id in self.tracer.current_traces
        
        trace_data = self.tracer.current_traces[trace_id]
        assert trace_data["agent_name"] == "TestAgent"
        assert trace_data["event_type"] == "test_event"
        assert trace_data["metadata"]["key"] == "value"
        assert trace_data["status"] == "started"
    
    def test_end_trace_success(self):
        """Test successful trace completion"""
        trace_id = self.tracer.start_trace("TestAgent", "test_event")
        time.sleep(0.01)  # Small delay to test duration calculation
        
        self.tracer.end_trace(trace_id, result={"output": "success"})
        
        assert trace_id not in self.tracer.current_traces
        
        # Check log file
        with open(self.temp_file.name, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 2  # Start and end events
            
            end_event = json.loads(lines[1])
            assert end_event["status"] == "completed"
            assert end_event["result"]["output"] == "success"
            assert end_event["duration_ms"] > 0
    
    def test_end_trace_error(self):
        """Test trace completion with error"""
        trace_id = self.tracer.start_trace("TestAgent", "test_event")
        
        self.tracer.end_trace(trace_id, error="Something went wrong")
        
        # Check log file
        with open(self.temp_file.name, 'r') as f:
            lines = f.readlines()
            end_event = json.loads(lines[1])
            assert end_event["status"] == "error"
            assert end_event["error"] == "Something went wrong"
    
    def test_log_message_event(self):
        """Test message logging"""
        message_id = self.tracer.log_message_event(
            sender="AgentA",
            receiver="AgentB", 
            content="Test message content"
        )
        
        assert message_id is not None
        
        # Check log file
        with open(self.temp_file.name, 'r') as f:
            event = json.loads(f.read().strip())
            assert event["event_type"] == "message_sent"
            assert event["sender"] == "AgentA"
            assert event["receiver"] == "AgentB"
            assert event["content_length"] == len("Test message content")
            assert event["message_id"] == message_id

class TestAgentInstrumentation:
    """Test that agents are properly instrumented with tracing"""
    
    def setup_method(self):
        """Setup test environment"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl')
        self.temp_file.close()
        
        # Mock the global tracer
        self.mock_tracer = Mock()
        
    def teardown_method(self):
        """Cleanup test environment"""
        Path(self.temp_file.name).unlink(missing_ok=True)
    
    @patch('MultiProdigy.agents.agent_base.tracer')
    def test_agent_send_logging(self, mock_tracer):
        """Test that agent.send() logs messages"""
        from MultiProdigy.agents.echo_agent import EchoAgent
        bus = Mock()
        agent = EchoAgent("TestAgent", bus)
        
        agent.send("Hello", "TargetAgent")
        
        # Verify tracer was called
        mock_tracer.log_message_event.assert_called_once_with(
            sender="TestAgent",
            receiver="TargetAgent",
            content="Hello"
        )
        
        # Verify bus.publish was called
        bus.publish.assert_called_once()
    
    @patch('MultiProdigy.agents.agent_base.tracer')
    def test_agent_handle_message_tracing(self, mock_tracer):
        """Test that message handling is traced"""
        bus = Mock()
        
        class TestAgent(BaseAgent):
            def on_message(self, message):
                return "processed"
        
        agent = TestAgent("TestAgent", bus)
        message = Message(sender="Sender", receiver="TestAgent", content="Test")
        
        mock_tracer.start_trace.return_value = "trace_123"
        
        agent.handle_message(message)
        
        # Verify tracing calls
        mock_tracer.start_trace.assert_called_once_with(
            agent_name="TestAgent",
            event_type="message_received",
            metadata={
                "sender": "Sender",
                "message_id": message.metadata.get("message_id"),
                "content_length": len("Test")
            }
        )
        
        mock_tracer.end_trace.assert_called_once_with(
            "trace_123", 
            result={"status": "processed"}
        )

class TestGraphBuilder:
    """Test graph data generation"""
    
    def setup_method(self):
        """Setup test environment with sample data"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl')
        
        # Write sample trace data
        sample_traces = [
            {
                "event_type": "message_sent",
                "timestamp": "2025-01-22T10:30:00Z",
                "sender": "UserAgent",
                "receiver": "TaskManager",
                "message_id": "msg_1",
                "content_preview": "Process this task",
                "content_length": 17
            },
            {
                "trace_id": "trace_1",
                "agent_name": "TaskManager",
                "event_type": "message_received",
                "start_time": "2025-01-22T10:30:01Z",
                "end_time": "2025-01-22T10:30:03Z",
                "duration_ms": 2000,
                "status": "completed"
            }
        ]
        
        for trace in sample_traces:
            self.temp_file.write(json.dumps(trace) + '\n')
        self.temp_file.close()
        
        self.graph_builder = AgentGraphBuilder(log_file=self.temp_file.name)
    
    def teardown_method(self):
        """Cleanup test environment"""
        Path(self.temp_file.name).unlink(missing_ok=True)
    
    def test_build_graph_data(self):
        """Test graph data generation"""
        graph_data = self.graph_builder.build_graph_data()
        
        assert "nodes" in graph_data
        assert "edges" in graph_data
        assert "metadata" in graph_data
        
        # Check nodes
        nodes = {node["id"]: node for node in graph_data["nodes"]}
        assert "UserAgent" in nodes
        assert "TaskManager" in nodes
        
        task_manager = nodes["TaskManager"]
        assert task_manager["status"] == "active"
        assert task_manager["message_count"] == 1  # Only received message in test data
        assert task_manager["avg_duration_ms"] == 1000.0  # Average of the durations in test data
        
        # Check edges
        assert len(graph_data["edges"]) == 1
        edge = graph_data["edges"][0]
        assert edge["source"] == "UserAgent"
        assert edge["target"] == "TaskManager"
        assert edge["content_preview"] == "Process this task"

class TestDashboardIntegration:
    """Test dashboard API integration"""
    
    def setup_method(self):
        """Setup test environment"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl')
        self.temp_file.close()
        self.dashboard = ObservabilityDashboard(log_file=self.temp_file.name)
        self.client = self.dashboard.app.test_client()
    
    def teardown_method(self):
        """Cleanup test environment"""
        Path(self.temp_file.name).unlink(missing_ok=True)
    
    def test_api_traces_endpoint(self):
        """Test /api/traces endpoint"""
        response = self.client.get('/api/traces')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
    
    def test_api_metrics_endpoint(self):
        """Test /api/metrics endpoint"""
        response = self.client.get('/api/metrics')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert "total_messages" in data
        assert "average_duration_ms" in data
        assert "error_count" in data
        assert "error_rate" in data
    
    def test_api_timeline_endpoint(self):
        """Test /api/timeline endpoint"""
        response = self.client.get('/api/timeline')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)

class TestEndToEndIntegration:
    """Test complete observability pipeline"""
    
    def test_full_pipeline(self):
        """Test complete flow from agent interaction to visualization"""
        # This would be a comprehensive test that:
        # 1. Creates agents with tracing enabled
        # 2. Simulates agent interactions
        # 3. Verifies logs are generated correctly
        # 4. Tests dashboard APIs return correct data
        # 5. Validates graph visualization data
        
        # For now, this is a placeholder for the full integration test
        assert True  # Placeholder

if __name__ == "__main__":
    pytest.main([__file__])