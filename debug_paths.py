#!/usr/bin/env python3
"""
Debug script to check path resolution
"""

import os
import sys

print("🔍 Debugging path resolution...")
print(f"Current working directory: {os.getcwd()}")
print(f"Script location: {os.path.abspath(__file__)}")

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from config import CRED_DATA_PATH, CRED_FILE_NAME
    print(f"✅ Config imported successfully")
    print(f"CRED_DATA_PATH: {CRED_DATA_PATH}")
    print(f"CRED_FILE_NAME: {CRED_FILE_NAME}")
    
    # Check if the file exists
    full_path = os.path.join(CRED_DATA_PATH, CRED_FILE_NAME)
    print(f"Full file path: {full_path}")
    print(f"File exists: {os.path.exists(full_path)}")
    
    # Check the data directory
    print(f"Data directory exists: {os.path.exists(CRED_DATA_PATH)}")
    if os.path.exists(CRED_DATA_PATH):
        print(f"Data directory contents: {os.listdir(CRED_DATA_PATH)}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

