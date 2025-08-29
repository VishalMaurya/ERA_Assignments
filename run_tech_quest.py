#!/usr/bin/env python3
"""
🎮 Tech Quest Academy Runner
Start the gamified learning platform for AI/ML & DevOps
"""

import subprocess
import sys
import os

def main():
    print("🎮 Starting Tech Quest Academy...")
    print("🚀 Initializing gamified learning platform...")
    print("📚 Preparing AI/ML & DevOps challenges...")
    print("="*60)
    print("🎯 Game server will be available at: http://localhost:8000")
    print("🎮 Ready to level up your tech skills!")
    print("⏹️  Press Ctrl+C to stop the game server")
    print("="*60)
    
    try:
        # Run the Tech Quest Academy with proper environment
        if os.path.exists("consciousness_env/bin/python"):
            python_executable = "consciousness_env/bin/python"
        elif os.path.exists("venv/bin/python"):
            python_executable = "venv/bin/python"
        else:
            python_executable = sys.executable
        
        # Start the FastAPI server
        subprocess.run([
            python_executable, "-m", "uvicorn",
            "tech_quest_main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
        
    except KeyboardInterrupt:
        print("\n🎮 Game server stopped. Thanks for playing Tech Quest Academy!")
    except Exception as e:
        print(f"\n❌ Error starting Tech Quest Academy: {e}")
        print("💡 Make sure your virtual environment is activated and dependencies are installed.")

if __name__ == "__main__":
    main()
