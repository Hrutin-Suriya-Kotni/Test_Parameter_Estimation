#!/usr/bin/env python3
"""
Test script for the CRED Conversation Analysis Tool

This script tests the API connection and basic functionality.
"""

from api_client import api_client
from data_loader import data_loader
from processor import processor
import json

def test_api_basic():
    """Test basic API functionality"""
    print("Testing basic API functionality...")
    
    test_prompt = "What is the capital of France?"
    response = api_client.call_api(user_prompt=test_prompt)
    
    if response:
        print("✅ Basic API test successful!")
        print(f"Response: {response[:100]}...")
        return True
    else:
        print("❌ Basic API test failed!")
        return False

def test_json_extraction():
    """Test JSON extraction functionality"""
    print("\nTesting JSON extraction...")
    
    # Test with a simple JSON response
    test_response = '''
    Here is my assessment:
    ```json
    {
        "Value": "Met",
        "Evidence": "The agent properly introduced themselves"
    }
    ```
    '''
    
    extracted = processor.extract_json_objects(test_response)
    if extracted and len(extracted) > 0:
        print("✅ JSON extraction test successful!")
        print(f"Extracted: {extracted}")
        return True
    else:
        print("❌ JSON extraction test failed!")
        return False

def test_single_conversation():
    """Test processing a single conversation"""
    print("\nTesting single conversation processing...")
    
    # Sample conversation
    sample_conversation = """
    Agent: Good morning! This is Priya calling from Cred. Am I speaking with Mr. Sharma?
    Customer: Yes, this is Sharma speaking.
    Agent: Thank you for confirming. How may I assist you today?
    Customer: I have a question about my recent payment.
    Agent: I'll be happy to help you with that. Let me check your account details.
    """
    
    # Test with opening assessment
    from prompts import PROMPT_OPENING
    full_prompt = sample_conversation + "\n\n" + PROMPT_OPENING
    
    response = api_client.call_api(user_prompt=full_prompt)
    if response:
        print("✅ Single conversation test successful!")
        print(f"Response: {response[:200]}...")
        
        # Test JSON extraction
        extracted = processor.extract_json_objects(response)
        if extracted:
            print(f"✅ JSON extraction successful: {extracted}")
        else:
            print("⚠️  JSON extraction failed for conversation test")
        
        return True
    else:
        print("❌ Single conversation test failed!")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("CRED Analysis Tool - API Tests")
    print("=" * 50)
    
    tests = [
        ("Basic API", test_api_basic),
        ("JSON Extraction", test_json_extraction),
        ("Single Conversation", test_single_conversation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} Test ---")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test failed with error: {e}")
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")
    print(f"{'='*50}")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the configuration.")

if __name__ == "__main__":
    main() 