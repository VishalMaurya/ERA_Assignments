#!/usr/bin/env python3
"""
Simple script to run the Animal & File Upload App with uv virtual environment
"""

import subprocess
import sys
import os
from pathlib import Path

def check_uv():
    """Check if uv is installed"""
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_uv():
    """Install uv package manager"""
    print("📦 Installing uv...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "uv"])
    print("✅ uv installed successfully!")

def setup_virtual_env():
    """Create and setup virtual environment using uv"""
    venv_path = Path("venv")
    
    if not venv_path.exists():
        print("🔧 Creating virtual environment...")
        subprocess.check_call(["uv", "venv", "venv"])
        print("✅ Virtual environment created!")
    
    # Install dependencies
    print("📦 Installing dependencies...")
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate"
        pip_path = venv_path / "Scripts" / "pip"
    else:  # Unix/macOS
        activate_script = venv_path / "bin" / "activate"
        pip_path = venv_path / "bin" / "pip"
    
    subprocess.check_call(["uv", "pip", "install", "-r", "requirements.txt"])
    print("✅ Dependencies installed successfully!")

def get_python_executable():
    """Get the Python executable from the virtual environment"""
    venv_path = Path("venv")
    if os.name == 'nt':  # Windows
        return str(venv_path / "Scripts" / "python")
    else:  # Unix/macOS
        return str(venv_path / "bin" / "python")

def main():
    print("🐾 Animal & File Upload App (with uv)")
    print("=" * 40)
    
    # Check if uv is installed
    if not check_uv():
        print("❌ uv not found. Installing...")
        try:
            install_uv()
        except subprocess.CalledProcessError:
            print("❌ Failed to install uv. Please install manually:")
            print("   pip install uv")
            sys.exit(1)
    
    # Setup virtual environment and dependencies
    try:
        setup_virtual_env()
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to setup environment: {e}")
        print("Please check the error above and try again.")
        sys.exit(1)
    
    # Start the application
    print("🚀 Starting the application...")
    print("📍 The app will be available at: http://localhost:8000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 40)
    
    try:
        # Get the Python executable from virtual environment
        python_exe = get_python_executable()
        
        # Run the FastAPI application
        subprocess.run([
            python_exe, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped. Goodbye!")
    except FileNotFoundError:
        print("❌ Error: main.py not found. Make sure you're in the correct directory.")
        sys.exit(1)

if __name__ == "__main__":
    main()
