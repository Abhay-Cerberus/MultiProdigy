#!/usr/bin/env python3
"""
Run the LLM System Demo
Tests the unified LLM architecture with all providers
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def main():
    print("🚀 MultiProdigy LLM System Demo Launcher")
    print("=" * 50)
    print("This demo tests the unified LLM architecture")
    print("=" * 50)
    
    try:
        from demo.llm_demo import main as demo_main
        demo_main()
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure you're in the MultiProdigy project root directory")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()