import sys
import os
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
import json

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

try:
    from flask import Flask, render_template_string, jsonify, request
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Warning: Flask not available. Install with: pip install flask")

class FixedLogCollector:
    """Fixed log collector that handles different column schemas"""
    
    def __init__(self, db_path="multiprodigy_logs.db"):
        # Use the database in the current directory
        self.db_path = db_path
        self.column_mapping = self._detect_schema()
    
    def _detect_schema(self):
        """Detect the actual database schema"""
        try:
            if not os.path.exists(self.db_path):
                print(f"Database {self.db_path} not found. Using default schema.")
                return {
                    'level': 'level', 
                    'agent_name': 'agent_name', 
                    'message': 'message', 
                    'timestamp': 'timestamp'
                }
                
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("PRAGMA table_info(logs)")
                columns = {row[1]: row for row in cursor.fetchall()}
                
                # Map standard names to actual column names
                mapping = {}
                mapping['level'] = 'level' if 'level' in columns else 'log_level' if 'log_level' in columns else None
                mapping['agent_name'] = 'agent_name' if 'agent_name' in columns else None
                mapping['message'] = 'message' if 'message' in columns else None
                mapping['timestamp'] = 'timestamp' if 'timestamp' in columns else None
                
                print(f"Detected database schema: {mapping}")
                return mapping
                
        except Exception as e:
            print(f"Schema detection failed: {e}")
            return {
                'level': 'level', 
                'agent_name': 'agent_name', 
                'message': 'message', 
                'timestamp': 'timestamp'
            }
    
    def get_recent_logs(self, limit=100):
        """Get recent logs with proper column handling"""
        try:
            if not os.path.exists(self.db_path):
                return pd.DataFrame(columns=['timestamp', 'agent_name', 'level', 'message'])
                
            with sqlite3.connect(self.db_path) as conn:
                # Build query based on available columns
                select_cols = []
                if self.column_mapping['timestamp']:
                    select_cols.append(f"{self.column_mapping['timestamp']} as timestamp")
                if self.column_mapping['agent_name']:
                    select_cols.append(f"{self.column_mapping['agent_name']} as agent_name")
                if self.column_mapping['level']:
                    select_cols.append(f"{self.column_mapping['level']} as level")
                if self.column_mapping['message']:
                    select_cols.append(f"{self.column_mapping['message']} as message")
                
                if not select_cols:
                    # Fallback: get all columns
                    query = f"SELECT * FROM logs ORDER BY id DESC LIMIT {limit}"
                else:
                    query = f"SELECT {', '.join(select_cols)} FROM logs ORDER BY created_at DESC LIMIT {limit}"
                
                df = pd.read_sql_query(query, conn)
                return df
                
        except Exception as e:
            print(f"Get logs error: {e}")
            # Return empty dataframe with expected columns
            return pd.DataFrame(columns=['timestamp', 'agent_name', 'level', 'message'])
    
    def get_log_counts(self):
        """Get log counts by level and agent"""
        try:
            if not os.path.exists(self.db_path):
                return {'total': 0, 'by_level': {}, 'by_agent': {}}
                
            with sqlite3.connect(self.db_path) as conn:
                # Count total logs
                total_query = "SELECT COUNT(*) FROM logs"
                total_count = conn.execute(total_query).fetchone()[0]
                
                # Count by level if level column exists
                level_counts = {}
                if self.column_mapping['level']:
                    level_query = f"SELECT {self.column_mapping['level']}, COUNT(*) FROM logs GROUP BY {self.column_mapping['level']}"
                    level_results = conn.execute(level_query).fetchall()
                    level_counts = {level: count for level, count in level_results}
                
                # Count by agent if agent_name column exists  
                agent_counts = {}
                if self.column_mapping['agent_name']:
                    agent_query = f"SELECT {self.column_mapping['agent_name']}, COUNT(*) FROM logs GROUP BY {self.column_mapping['agent_name']}"
                    agent_results = conn.execute(agent_query).fetchall()
                    agent_counts = {agent: count for agent, count in agent_results}
                
                return {
                    'total': total_count,
                    'by_level': level_counts,
                    'by_agent': agent_counts
                }
                
        except Exception as e:
            print(f"Get counts error: {e}")
            return {
                'total': 0,
                'by_level': {},
                'by_agent': {}
            }
    
    def get_recent_activity(self, hours=1):
        """Get recent activity for network graph"""
        try:
            if not os.path.exists(self.db_path):
                return pd.DataFrame(columns=['agent_name', 'message', 'timestamp'])
                
            with sqlite3.connect(self.db_path) as conn:
                cutoff_time = (datetime.now() - timedelta(hours=hours)).isoformat()
                
                # Query based on available columns
                if self.column_mapping['timestamp'] and self.column_mapping['agent_name']:
                    query = f"""
                    SELECT {self.column_mapping['agent_name']} as agent_name, 
                           {self.column_mapping['message']} as message,
                           {self.column_mapping['timestamp']} as timestamp
                    FROM logs 
                    WHERE {self.column_mapping['timestamp']} > ?
                    ORDER BY created_at DESC
                    """
                    df = pd.read_sql_query(query, conn, params=[cutoff_time])
                else:
                    # Fallback query
                    query = "SELECT * FROM logs ORDER BY id DESC LIMIT 50"
                    df = pd.read_sql_query(query, conn)
                
                return df
                
        except Exception as e:
            print(f"Get activity error: {e}")
            return pd.DataFrame(columns=['agent_name', 'message', 'timestamp'])

# Initialize the fixed collector
log_collector = FixedLogCollector()

def get_metrics_data():
    """Get metrics from the fixed collector"""
    try:
        counts = log_collector.get_log_counts()
        total_logs = counts.get('total', 0)
        error_count = counts.get('by_level', {}).get('ERROR', 0)
        error_rate = round((error_count / total_logs * 100) if total_logs > 0 else 0, 1)
        
        return {
            'total_messages': total_logs,
            'average_duration_ms': 0,  # Will implement when we add timing
            'error_rate': error_rate,
            'status': 'Active' if total_logs > 0 else 'Waiting'
        }
    except Exception as e:
        print(f"Error getting metrics: {e}")
        return {
            'total_messages': 0,
            'average_duration_ms': 0,
            'error_rate': 0,
            'status': 'Error'
        }

def get_timeline_data():
    """Get recent log activity for timeline"""
    try:
        recent_logs_df = log_collector.get_recent_logs(limit=50)
        timeline = []
        
        for _, log in recent_logs_df.iterrows():
            # Determine timeline item type based on message content
            message = str(log.get('message', ''))
            level = str(log.get('level', 'INFO'))
            
            if 'error' in message.lower() or level == 'ERROR':
                item_type = 'error'
            elif any(keyword in message.lower() for keyword in ['sent', 'received', 'message', 'response']):
                item_type = 'message'
            else:
                item_type = 'processing'
            
            timeline.append({
                'timestamp': log.get('timestamp', datetime.now().isoformat()),
                'agent': log.get('agent_name', 'Unknown'),
                'level': level,
                'message': message,
                'type': item_type
            })
        
        return timeline
        
    except Exception as e:
        print(f"Error getting timeline: {e}")
        return []

def get_network_data():
    """Get data for network graph with error handling"""
    try:
        activity = log_collector.get_recent_activity()
        
        nodes = set()
        edges = []
        
        # Extract agent interactions from messages
        for _, row in activity.iterrows():
            agent_name = row.get('agent_name', 'Unknown')
            message = str(row.get('message', ''))
            
            nodes.add(agent_name)
            
            # Try to extract message targets from message content
            if any(keyword in message.lower() for keyword in ['to', 'sent', 'received']):
                # Simple parsing for various message patterns
                words = message.split()
                for i, word in enumerate(words):
                    if word.lower() in ['to', 'from'] and i + 1 < len(words):
                        target = words[i + 1].rstrip(':.,!?')
                        if target != agent_name and len(target) > 2:  # Basic filter
                            nodes.add(target)
                            edges.append({
                                'source': agent_name,
                                'target': target,
                                'weight': 1
                            })
        
        return {
            'nodes': [{'id': node, 'label': node} for node in nodes],
            'edges': edges
        }
        
    except Exception as e:
        print(f"Network data error: {e}")
        return {'nodes': [], 'edges': []}

# Dashboard HTML Template
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>MultiProdigy Observability Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            min-height: 100vh; 
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { 
            background: rgba(255,255,255,0.95); 
            padding: 30px; 
            border-radius: 15px; 
            margin-bottom: 30px; 
            box-shadow: 0 8px 32px rgba(0,0,0,0.1); 
            backdrop-filter: blur(10px);
        }
        .header h1 { margin: 0; color: #333; font-size: 2.5em; }
        .header p { margin: 10px 0 0 0; color: #666; font-size: 1.1em; }
        .nav-links { margin-top: 20px; }
        .nav-links a { 
            margin-right: 15px; 
            padding: 12px 24px; 
            background: #667eea; 
            color: white; 
            text-decoration: none; 
            border-radius: 8px; 
            transition: all 0.3s ease;
            display: inline-block;
        }
        .nav-links a:hover { background: #5a6fd8; transform: translateY(-2px); }
        .metrics { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px; 
        }
        .metric-card { 
            background: rgba(255,255,255,0.95); 
            padding: 25px; 
            border-radius: 15px; 
            box-shadow: 0 8px 32px rgba(0,0,0,0.1); 
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }
        .metric-card:hover { transform: translateY(-5px); }
        .metric-card h3 { margin: 0 0 15px 0; color: #333; font-size: 1.2em; }
        .metric-value { font-size: 2.2em; font-weight: bold; color: #667eea; margin-bottom: 5px; }
        .metric-change { font-size: 0.9em; color: #28a745; }
        .timeline { 
            background: rgba(255,255,255,0.95); 
            border-radius: 15px; 
            padding: 30px; 
            box-shadow: 0 8px 32px rgba(0,0,0,0.1); 
            backdrop-filter: blur(10px);
            max-height: 600px;
            overflow-y: auto;
        }
        .timeline h2 { margin: 0 0 25px 0; color: #333; }
        .timeline-item { 
            padding: 20px; 
            border-left: 4px solid #667eea; 
            margin: 15px 0; 
            background: rgba(102,126,234,0.1); 
            border-radius: 8px; 
            transition: all 0.3s ease;
        }
        .timeline-item:hover { transform: translateX(5px); background: rgba(102,126,234,0.15); }
        .timeline-item.error { border-left-color: #dc3545; background: rgba(220,53,69,0.1); }
        .timeline-item.message { border-left-color: #28a745; background: rgba(40,167,69,0.1); }
        .timeline-item.processing { border-left-color: #ffc107; background: rgba(255,193,7,0.1); }
        .timestamp { font-weight: bold; color: #666; font-size: 0.9em; }
        .agent-name { color: #667eea; font-weight: bold; }
        .content { margin-top: 8px; line-height: 1.4; }
        .loading { 
            text-align: center; 
            padding: 40px; 
            color: #666; 
            font-style: italic;
        }
        .status-indicator { 
            display: inline-block; 
            width: 10px; 
            height: 10px; 
            border-radius: 50%; 
            background: #28a745; 
            margin-right: 8px; 
            animation: pulse 2s infinite;
        }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
        .refresh-btn { 
            background: #667eea; 
            color: white; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 8px; 
            cursor: pointer; 
            float: right;
            margin-top: -10px;
        }
        .refresh-btn:hover { background: #5a6fd8; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 MultiProdigy Observatory</h1>
            <p>Real-time monitoring and visualization for your AI agent network</p>
            <div class="nav-links">
                <a href="/">📊 Dashboard</a>
                <a href="/monitoring">📈 Enhanced Monitoring</a>
                <a href="/api/logs">📋 Raw Logs</a>
            </div>
        </div>
        
        <div class="metrics" id="metrics">
            <div class="metric-card">
                <h3>📨 Total Messages</h3>
                <div class="metric-value" id="total-messages">Loading...</div>
                <div class="metric-change">↗️ Live data</div>
            </div>
            <div class="metric-card">
                <h3>⏱️ Avg Response</h3>
                <div class="metric-value" id="avg-duration">Loading...</div>
                <div class="metric-change">Real-time average</div>
            </div>
            <div class="metric-card">
                <h3>❌ Error Rate</h3>
                <div class="metric-value" id="error-rate">Loading...</div>
                <div class="metric-change">System health</div>
            </div>
            <div class="metric-card">
                <h3>🟢 System Status</h3>
                <div class="metric-value" id="status">
                    <span class="status-indicator"></span>Loading...
                </div>
                <div class="metric-change">Live monitoring</div>
            </div>
        </div>
        
        <div class="timeline">
            <h2>📋 Live Agent Activity</h2>
            <button class="refresh-btn" onclick="loadTimeline()">🔄 Refresh</button>
            <div id="timeline-content" class="loading">Loading agent activity...</div>
        </div>
    </div>

    <script>
        function formatTimestamp(timestamp) {
            try {
                const date = new Date(timestamp);
                return date.toLocaleTimeString() + ' ' + date.toLocaleDateString();
            } catch (e) {
                return timestamp;
            }
        }

        function loadMetrics() {
            fetch('/api/metrics')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('total-messages').textContent = data.total_messages || 0;
                    document.getElementById('avg-duration').textContent = (data.average_duration_ms || 0) + 'ms';
                    document.getElementById('error-rate').textContent = (data.error_rate || 0) + '%';
                    
                    const statusEl = document.getElementById('status');
                    statusEl.innerHTML = `<span class="status-indicator"></span>${data.status || 'Unknown'}`;
                })
                .catch(e => {
                    console.error('Error loading metrics:', e);
                    document.getElementById('total-messages').textContent = 'Error';
                    document.getElementById('avg-duration').textContent = 'Error';
                    document.getElementById('error-rate').textContent = 'Error';
                    document.getElementById('status').textContent = 'Error';
                });
        }
        
        function loadTimeline() {
            fetch('/api/timeline')
                .then(r => r.json())
                .then(data => {
                    const timeline = document.getElementById('timeline-content');
                    
                    if (data.length === 0) {
                        timeline.innerHTML = `
                            <div class="loading">
                                🤖 No agent activity detected yet.<br>
                                <small>Agents will appear here when they start processing messages.</small>
                            </div>`;
                        return;
                    }
                    
                    timeline.innerHTML = '';
                    
                    data.slice(-30).reverse().forEach(item => {
                        const div = document.createElement('div');
                        div.className = `timeline-item ${item.type || 'processing'}`;
                        
                        let icon = '⚙️';
                        if (item.type === 'error') icon = '❌';
                        else if (item.type === 'message') icon = '📨';
                        
                        div.innerHTML = `
                            <div class="timestamp">${formatTimestamp(item.timestamp)}</div>
                            <div class="content">
                                ${icon} <span class="agent-name">${item.agent || 'Unknown Agent'}</span>
                                <div style="margin-top: 5px;">${item.message || 'No message content'}</div>
                            </div>
                        `;
                        
                        timeline.appendChild(div);
                    });
                })
                .catch(e => {
                    console.error('Error loading timeline:', e);
                    document.getElementById('timeline-content').innerHTML = `
                        <div class="loading">
                            ❌ Error loading timeline data<br>
                            <small>Please check the console for details.</small>
                        </div>`;
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

        console.log('🚀 MultiProdigy Dashboard loaded successfully!');
    </script>
</body>
</html>
'''

def create_app():
    """Create Flask application"""
    if not FLASK_AVAILABLE:
        raise ImportError("Flask is not available. Install with: pip install flask")
    
    app = Flask(__name__)
    
    # Main dashboard route
    @app.route('/')
    def dashboard():
        """Main dashboard UI"""
        return render_template_string(DASHBOARD_HTML)
    
    # API Routes
    @app.route('/api/metrics')
    def api_metrics():
        """API endpoint for metrics data"""
        return jsonify(get_metrics_data())

    @app.route('/api/timeline')
    def api_timeline():
        """API endpoint for timeline data"""
        return jsonify(get_timeline_data())

    @app.route('/api/graph')
    def api_graph():
        """API endpoint for network graph data"""
        try:
            graph_data = get_network_data()
            
            # Convert to the expected format
            nodes = []
            for node in graph_data.get('nodes', []):
                nodes.append({
                    "id": node['id'],
                    "label": node['label'],
                    "status": "active",
                    "size": 20,
                    "message_count": 0,
                    "error_count": 0,
                    "avg_duration_ms": 0
                })
            
            edges = []
            for edge in graph_data.get('edges', []):
                edges.append({
                    "id": f"{edge['source']}-{edge['target']}",
                    "source": edge['source'],
                    "target": edge['target'],
                    "timestamp": "",
                    "content_preview": "Agent communication"
                })
            
            return jsonify({
                "nodes": nodes,
                "edges": edges
            })
        
        except Exception as e:
            print(f"Error getting graph data: {e}")
            return jsonify({"nodes": [], "edges": []})

    @app.route('/api/logs')
    def api_logs():
        """API endpoint to get logs"""
        try:
            agent_name = request.args.get('agent')
            level = request.args.get('level')
            limit = int(request.args.get('limit', 100))

            logs_df = log_collector.get_recent_logs(limit=limit)
            
            # Filter by agent if specified
            if agent_name and 'agent_name' in logs_df.columns:
                logs_df = logs_df[logs_df['agent_name'] == agent_name]
            
            # Filter by level if specified
            if level and 'level' in logs_df.columns:
                logs_df = logs_df[logs_df['level'] == level]
            
            logs = logs_df.to_dict('records')
            return jsonify(logs)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/monitoring')
    def monitoring_dashboard():
        """Enhanced monitoring dashboard"""
        # Simple monitoring view for now
        return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Enhanced Monitoring</title></head>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h1>🔬 Enhanced Monitoring</h1>
            <p>Advanced monitoring features coming soon...</p>
            <a href="/">← Back to Dashboard</a>
            
            <div style="margin-top: 30px;">
                <h2>Raw Logs</h2>
                <div id="logs" style="background: #f5f5f5; padding: 15px; border-radius: 8px; max-height: 400px; overflow-y: auto;">
                    Loading logs...
                </div>
            </div>
            
            <script>
                fetch('/api/logs')
                    .then(r => r.json())
                    .then(logs => {
                        const logsDiv = document.getElementById('logs');
                        if (logs.length === 0) {
                            logsDiv.innerHTML = 'No logs available';
                            return;
                        }
                        
                        logsDiv.innerHTML = logs.map(log => 
                            `<div style="margin-bottom: 10px; padding: 8px; background: white; border-radius: 4px;">
                                <strong>${log.timestamp || 'No timestamp'}</strong> - 
                                <span style="color: blue;">${log.agent_name || 'Unknown'}</span> - 
                                <span style="color: red;">[${log.level || 'INFO'}]</span><br>
                                ${log.message || 'No message'}
                            </div>`
                        ).join('');
                    })
                    .catch(e => {
                        document.getElementById('logs').innerHTML = 'Error loading logs: ' + e.message;
                    });
            </script>
        </body>
        </html>
        ''')
    
    return app

if __name__ == "__main__":
    if FLASK_AVAILABLE:
        app = create_app()
        print("🚀 Starting MultiProdigy Dashboard...")
        app.run(host="127.0.0.1", port=5000, debug=True)
    else:
        print("❌ Flask not available. Install with: pip install flask pandas")