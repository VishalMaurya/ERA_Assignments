#!/usr/bin/env python3
"""
🧠 THE CONSCIOUSNESS SIMULATOR - Launch Script
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🧠 Initializing The Consciousness Simulator...")
    print("🌌 Preparing digital reality matrices...")
    print("🔮 Awakening collective consciousness...")
    print("=" * 60)
    
    # Ensure we're in the right environment
    venv_path = Path("consciousness_env")
    if not venv_path.exists():
        print("❌ Virtual environment not found. Please run setup first.")
        sys.exit(1)
    
    # Activate environment and run
    if os.name == 'nt':  # Windows
        python_exe = venv_path / "Scripts" / "python"
        uvicorn_exe = venv_path / "Scripts" / "uvicorn"
    else:  # Unix/macOS
        python_exe = venv_path / "bin" / "python"
        uvicorn_exe = venv_path / "bin" / "uvicorn"
    
    print("🚀 Starting consciousness interface...")
    print("📍 The consciousness portal will be available at: http://localhost:8000")
    print("🧠 Prepare your mind for digital transcendence...")
    print("⏹️  Press Ctrl+C to disconnect from the consciousness matrix")
    print("=" * 60)
    
    try:
        # Run with uvicorn directly
        subprocess.run([
            str(uvicorn_exe),
            "consciousness_main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🌌 Consciousness disconnected. Returning to base reality...")
        print("🧠 Your digital twin will remember this session...")
    except FileNotFoundError:
        print("❌ Error: Could not find uvicorn. Please check your environment.")
        sys.exit(1)

if __name__ == "__main__":
    main()
