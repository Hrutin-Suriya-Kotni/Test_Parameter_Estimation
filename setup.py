#!/usr/bin/env python3
"""
Setup script for CRED Conversation Analysis Tool
"""

import os
import sys
import subprocess
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip3", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["data", "results"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python version {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def main():
    """Main setup function"""
    print("=" * 50)
    print("CRED Conversation Analysis Tool - Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        print("\n⚠️  Setup incomplete. Please install requirements manually:")
        print("pip install -r requirements.txt")
        return
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Place your Excel file in the 'data' directory")
    print("2. Run 'python test_api.py' to test the setup")
    print("3. Run 'python main.py' to start the analysis")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main() 