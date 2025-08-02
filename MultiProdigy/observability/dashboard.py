import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

try:
    from flask import Flask, jsonify, render_template_string
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Warning: Flask not available. Install with: pip install flask")

class ObservabilityDashboard:
    """LangSmith-like dashboard for MultiProdigy agents"""
    
    def __init__(self, log_file: str = "agent_traces.jsonl"):
        self.log_file = Path(log_file)
        if FLASK_AVAILABLE:
            self.app = Flask(__name__)
            self._setup_routes()
        else:
            self.app = None
    
    def _setup_routes(self):
        if not FLASK_AVAILABLE:
            return
            
        @self.app.route('/api/traces')
        def get_traces():
            """Get all traces with optional filtering"""
            traces = self._load_traces()
            return jsonify(traces)
        
        @self.app.route('/api/traces/<trace_id>')
        def get_trace_details(trace_id):
            """Get detailed information for a specific trace"""
            traces = self._load_traces()
            trace = next((t for t in traces if t.get('trace_id') == trace_id), None)
            if not trace:
                return jsonify({'error': 'Trace not found'}), 404
            return jsonify(trace)
        
        @self.app.route('/api/timeline')
        def get_timeline():
            """Get timeline view of agent interactions"""
            traces = self._load_traces()
            timeline = self._build_timeline(traces)
            return jsonify(timeline)
        
        @self.app.route('/api/metrics')
        def get_metrics():
            """Get performance metrics"""
            traces = self._load_traces()
            metrics = self._calculate_metrics(traces)
            return jsonify(metrics)
        
        @self.app.route('/api/graph')
        def get_graph():
            """Get graph visualization data"""
            try:
                from .graph_builder import AgentGraphBuilder
                builder = AgentGraphBuilder(self.log_file)
                graph_data = builder.build_graph_data()
                return jsonify(graph_data)
            except Exception as e:
                return jsonify({"error": str(e), "nodes": [], "edges": []})
        
        @self.app.route('/static/graph.html')
        def graph_view():
            """Graph visualization page"""
            graph_html_path = Path(__file__).parent / 'static' / 'graph.html'
            if graph_html_path.exists():
                return graph_html_path.read_text(encoding='utf-8')
            return "Graph visualization not found", 404
        
        @self.app.route('/')
        def dashboard():
            """Main dashboard UI"""
            return render_template_string(DASHBOARD_HTML)
    
    def _load_traces(self) -> List[Dict[str, Any]]:
        """Load traces from log file"""
        if not self.log_file.exists():
            return []
        
        traces = []
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        traces.append(json.loads(line.strip()))
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"Warning: Could not read log file {self.log_file}: {e}")
            return []
        
        return sorted(traces, key=lambda x: x.get('timestamp', x.get('start_time', '')))
    
    def _build_timeline(self, traces: List[Dict]) -> List[Dict]:
        """Build timeline view of agent interactions"""
        timeline = []
        
        for trace in traces:
            if trace.get('event_type') == 'message_sent':
                timeline.append({
                    'timestamp': trace.get('timestamp'),
                    'type': 'message',
                    'sender': trace.get('sender'),
                    'receiver': trace.get('receiver'),
                    'content_preview': trace.get('content_preview'),
                    'message_id': trace.get('message_id')
                })
            elif trace.get('event_type') in ['message_received', 'message_processing']:
                timeline.append({
                    'timestamp': trace.get('start_time'),
                    'type': 'processing',
                    'agent': trace.get('agent_name'),
                    'duration_ms': trace.get('duration_ms'),
                    'status': trace.get('status'),
                    'trace_id': trace.get('trace_id')
                })
        
        return timeline
    
    def _calculate_metrics(self, traces: List[Dict]) -> Dict[str, Any]:
        """Calculate performance metrics"""
        total_messages = len([t for t in traces if t.get('event_type') == 'message_sent'])
        total_processing = len([t for t in traces if t.get('duration_ms')])
        
        durations = [t.get('duration_ms', 0) for t in traces if t.get('duration_ms')]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        errors = len([t for t in traces if t.get('status') == 'error'])
        
        return {
            'total_messages': total_messages,
            'total_processing_events': total_processing,
            'average_duration_ms': round(avg_duration, 2),
            'error_count': errors,
            'error_rate': round(errors / max(total_processing, 1) * 100, 2)
        }
    
    def run(self, host='localhost', port=5000, debug=False):
        """Start the dashboard server"""
        if not FLASK_AVAILABLE:
            print("❌ Flask not available. Install with: pip install flask")
            return
            
        if not self.app:
            print("❌ Dashboard not initialized properly")
            return
            
        print(f"🚀 MultiProdigy Observability Dashboard running at http://{host}:{port}")
        try:
            self.app.run(host=host, port=port, debug=debug)
        except Exception as e:
            print(f"❌ Could not start dashboard: {e}")

# Simple HTML template for the dashboard
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>MultiProdigy Observability Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .header { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metrics { display: flex; gap: 20px; margin-bottom: 30px; flex-wrap: wrap; }
        .metric-card { background: white; padding: 20px; border-radius: 8px; min-width: 200px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric-card h3 { margin: 0 0 10px 0; color: #333; }
        .metric-value { font-size: 24px; font-weight: bold; color: #007bff; }
        .timeline { background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .timeline-item { padding: 15px; border-left: 4px solid #007bff; margin: 10px 0; background: #f8f9fa; border-radius: 4px; }
        .timeline-item.error { border-left-color: #dc3545; background: #f8d7da; }
        .timeline-item.message { border-left-color: #28a745; background: #d4edda; }
        .timestamp { font-weight: bold; color: #666; }
        .content { margin-top: 5px; }
        .loading { text-align: center; padding: 20px; color: #666; }
        .nav-links { margin-bottom: 20px; }
        .nav-links a { margin-right: 15px; padding: 8px 16px; background: #007bff; color: white; text-decoration: none; border-radius: 4px; }
        .nav-links a:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 MultiProdigy Agent Observatory</h1>
        <div class="nav-links">
            <a href="/">Dashboard</a>
            <a href="/static/graph.html">Network Graph</a>
        </div>
    </div>
    
    <div class="metrics" id="metrics">
        <div class="metric-card">
            <h3>📨 Total Messages</h3>
            <div class="metric-value" id="total-messages">Loading...</div>
        </div>
        <div class="metric-card">
            <h3>⏱️ Avg Duration</h3>
            <div class="metric-value" id="avg-duration">Loading...</div>
        </div>
        <div class="metric-card">
            <h3>❌ Error Rate</h3>
            <div class="metric-value" id="error-rate">Loading...</div>
        </div>
        <div class="metric-card">
            <h3>🔄 Status</h3>
            <div class="metric-value" id="status">Active</div>
        </div>
    </div>
    
    <div class="timeline">
        <h2>📋 Agent Timeline</h2>
        <div id="timeline-content" class="loading">Loading timeline...</div>
    </div>

    <script>
        function loadMetrics() {
            fetch('/api/metrics')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('total-messages').textContent = data.total_messages || 0;
                    document.getElementById('avg-duration').textContent = (data.average_duration_ms || 0) + 'ms';
                    document.getElementById('error-rate').textContent = (data.error_rate || 0) + '%';
                })
                .catch(e => {
                    console.error('Error loading metrics:', e);
                    document.getElementById('total-messages').textContent = 'Error';
                });
        }
        
        function loadTimeline() {
            fetch('/api/timeline')
                .then(r => r.json())
                .then(data => {
                    const timeline = document.getElementById('timeline-content');
                    
                    if (data.length === 0) {
                        timeline.innerHTML = '<div class="loading">No agent activity yet. Agents will appear here when they start communicating.</div>';
                        return;
                    }
                    
                    timeline.innerHTML = '';
                    
                    data.slice(-20).forEach(item => {  // Show last 20 events
                        const div = document.createElement('div');
                        div.className = `timeline-item ${item.type || ''}`;
                        
                        if (item.type === 'message') {
                            div.innerHTML = `
                                <div class="timestamp">${new Date(item.timestamp).toLocaleTimeString()}</div>
                                <div class="content">📨 <strong>${item.sender}</strong> → <strong>${item.receiver}</strong></div>
                                <div style="margin-top: 5px; font-style: italic; color: #666;">${item.content_preview || 'No preview'}</div>
                            `;
                        } else if (item.type === 'processing') {
                            div.innerHTML = `
                                <div class="timestamp">${new Date(item.timestamp).toLocaleTimeString()}</div>
                                <div class="content">⚙️ <strong>${item.agent}</strong> processed message</div>
                                <div style="margin-top: 5px; color: #666;">Duration: ${item.duration_ms || 0}ms | Status: ${item.status || 'unknown'}</div>
                            `;
                        }
                        
                        timeline.appendChild(div);
                    });
                })
                .catch(e => {
                    console.error('Error loading timeline:', e);
                    document.getElementById('timeline-content').innerHTML = '<div class="loading">Error loading timeline data</div>';
                });
        }
        
        // Load data initially
        loadMetrics();
        loadTimeline();
        
        // Auto-refresh every 5 seconds
        setInterval(() => {
            loadMetrics();
            loadTimeline();
        }, 5000);
    </script>
</body>
</html>
'''