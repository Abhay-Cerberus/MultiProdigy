import os
import sys
import time
import logging
import threading
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from MultiProdigy.runtime.engine import RuntimeEngine
    from MultiProdigy.monitor.log_collector import log_collector
    from MultiProdigy.observability.dashboard import create_app
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all required files exist:")
    print("  - MultiProdigy/runtime/engine.py")
    print("  - MultiProdigy/monitor/log_collector.py") 
    print("  - MultiProdigy/observability/dashboard.py")
    sys.exit(1)

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(asctime)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def simulate_agent_activities(engine: RuntimeEngine):
    """Simulate some agent activities for demonstration"""
    logger = logging.getLogger("MultiProdigy_Main")
    
    try:
        # Simulate some agent interactions
        if 'echo_agent' in engine.agents:
            echo_agent = engine.agents['echo_agent']
            result = echo_agent.process("Hi")
            logger.info("Message echoed successfully", extra={'original_length': len("Hi"), 'echo_length': len(str(result))})
        
        if 'ollama_agent' in engine.agents:
            ollama_agent = engine.agents['ollama_agent']
            message = {'content': 'What is AI?'}
            logger.info(f"Received message: {message}")
            result = ollama_agent.process(message)
            logger.info(f"Sending response: {result}")
        
        # Generate some sample logs for dashboard testing
        log_collector.generate_sample_data()
        
    except Exception as e:
        logger.error(f"Error during agent simulation: {e}")

def run_dashboard():
    """Run the Flask dashboard in a separate thread"""
    logger = logging.getLogger("MultiProdigy_Main")
    
    try:
        # Wait a moment for the system to initialize
        time.sleep(2)
        
        logger.info("Starting dashboard at http://127.0.0.1:5000")
        
        # Create and run the Flask app
        app = create_app()
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
        
    except Exception as e:
        logger.error(f"Dashboard startup failed: {e}")

def main():
    """Main entry point for MultiProdigy system"""
    print("🚀 Welcome to MultiProdigy!")
    print("Phase 1 & 2: Log Monitoring and Visualization System")
    print("=" * 50)
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger("MultiProdigy_Main")
    
    try:
        logger.info("MultiProdigy System initializing...")
        
        # Initialize log collector first (this creates the database)
        log_collector.start()
        print("✅ Log collector initialized")
        
        print("Starting complete system (runtime + dashboard)...")
        
        # Initialize and start the runtime engine
        logger.info("Starting runtime engine...")
        engine = RuntimeEngine()
        logger.info("Runtime engine started successfully")
        
        # Simulate some agent activities
        logger.info("Simulating agent activities...")
        simulate_agent_activities(engine)
        logger.info("Agent simulation completed")
        
        # Start dashboard in a separate thread
        dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
        dashboard_thread.start()
        
        print("\n🚀 MultiProdigy Observability Dashboard running at http://127.0.0.1:5000")
        print("\n📊 Available endpoints:")
        print("   • Main Dashboard: http://127.0.0.1:5000/")
        print("   • Enhanced Monitoring: http://127.0.0.1:5000/monitoring")
        print("   • API Metrics: http://127.0.0.1:5000/api/metrics")
        print("   • Logs API: http://127.0.0.1:5000/api/logs")
        print("\n⌨️  Press Ctrl+C to stop the system")
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down MultiProdigy...")
            log_collector.stop()
            print("✅ System shutdown complete")
            
    except Exception as e:
        logger.error(f"System startup failed: {e}")
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)