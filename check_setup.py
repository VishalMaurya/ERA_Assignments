#!/usr/bin/env python3
"""
Check the setup status of the Animal & File Upload App
"""

import subprocess
import sys
from pathlib import Path

def check_uv():
    """Check if uv is installed"""
    try:
        result = subprocess.run(["uv", "--version"], check=True, capture_output=True, text=True)
        return True, result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, None

def check_venv():
    """Check if virtual environment exists"""
    venv_path = Path("venv")
    return venv_path.exists()

def check_dependencies():
    """Check if dependencies are installed in the virtual environment"""
    try:
        # Try to import key packages
        if check_venv():
            python_exe = Path("venv/bin/python") if sys.platform != "win32" else Path("venv/Scripts/python.exe")
            if python_exe.exists():
                result = subprocess.run([str(python_exe), "-c", "import fastapi, uvicorn; print('✅ Dependencies OK')"], 
                                      check=True, capture_output=True, text=True)
                return True, result.stdout.strip()
        return False, "Dependencies not found"
    except subprocess.CalledProcessError:
        return False, "Import failed"

def main():
    print("🔍 Animal & File Upload App - Setup Status")
    print("=" * 50)
    
    # Check uv
    uv_ok, uv_version = check_uv()
    if uv_ok:
        print(f"✅ uv: {uv_version}")
    else:
        print("❌ uv: Not installed")
    
    # Check virtual environment
    if check_venv():
        print("✅ Virtual Environment: venv/ directory exists")
    else:
        print("❌ Virtual Environment: venv/ directory not found")
    
    # Check dependencies
    deps_ok, deps_msg = check_dependencies()
    if deps_ok:
        print(f"✅ Dependencies: {deps_msg}")
    else:
        print(f"❌ Dependencies: {deps_msg}")
    
    print("\n" + "=" * 50)
    
    if uv_ok and check_venv() and deps_ok:
        print("🎉 Setup is complete! Run 'python run.py' to start the app.")
    else:
        print("⚠️  Setup incomplete. Run 'python run.py' to fix issues.")
    
    print("📍 App URL: http://localhost:8000")

if __name__ == "__main__":
    main()
