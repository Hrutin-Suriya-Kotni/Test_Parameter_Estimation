#!/usr/bin/env python3
"""
Test launcher script for CRED conversation analysis
Provides easy access to all test runners from the root directory
"""

import os
import sys
import subprocess
from datetime import datetime


def run_script(script_path, description):
    """Run a script and handle errors"""
    print(f"\n🚀 {description}")
    print("=" * 50)
    
    try:
        # Run the script
        result = subprocess.run([sys.executable, script_path], 
                              cwd=os.path.dirname(os.path.abspath(__file__)),
                              capture_output=False)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
        else:
            print(f"❌ {description} failed with return code {result.returncode}")
            
    except Exception as e:
        print(f"❌ Error running {description}: {e}")


def main():
    """Main launcher function"""
    print("🎯 CRED Conversation Analysis - Test Launcher")
    print("=" * 60)
    
    # Available test scripts
    test_scripts = {
        '1': {
            'script': 'test_runners/test_mistral.py',
            'description': 'Test Mistral Model'
        },
        '2': {
            'script': 'test_runners/test_gemini.py', 
            'description': 'Test Gemini Model'
        },
        '3': {
            'script': 'test_runners/test_comparison.py',
            'description': 'Compare All Models'
        },
        '4': {
            'script': 'test_runners/run_all_models.py',
            'description': 'Run All Models (Master Runner)'
        },
        '5': {
            'script': 'model_config.py',
            'description': 'Check Model Status'
        }
    }
    
    while True:
        print("\n📋 Available Tests:")
        for key, info in test_scripts.items():
            print(f"  {key}. {info['description']}")
        print("  6. Exit")
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '6':
                print("👋 Goodbye!")
                break
            elif choice in test_scripts:
                script_info = test_scripts[choice]
                script_path = script_info['script']
                description = script_info['description']
                
                # Check if script exists
                if os.path.exists(script_path):
                    run_script(script_path, description)
                else:
                    print(f"❌ Script not found: {script_path}")
            else:
                print("Please enter a valid choice (1-6)")
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Test interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
