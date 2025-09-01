#!/usr/bin/env python3
"""
Test script for the deployed Mistral model via OpenChat API

This script tests the same endpoint as the curl command:
curl -X POST http://192.168.30.239:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openchat/openchat-3.5-1210",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is the capital of India?"}
    ],
    "max_tokens": 500,
    "temperature": 1
  }' | jq -r '.choices[0].message.content'
"""

import requests
import json
from typing import Optional, Dict, Any

class MistralDeploymentTester:
    """Test the deployed Mistral model via OpenChat API"""
    
    def __init__(self, base_url: str = "http://192.168.30.239:8000/chat"):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
    
    def test_basic_chat(self, 
                        user_message: str = "What is the capital of India?",
                        system_message: str = "You are a helpful assistant.",
                        model: str = "openchat/openchat-3.5-1210",
                        max_tokens: int = 500,
                        temperature: float = 1.0) -> Optional[str]:
        """
        Test the basic chat functionality (mirrors the curl command)
        
        Args:
            user_message: The user's question
            system_message: The system prompt
            model: The model to use
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            The API response content or None if failed
        """
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        print(f"Testing endpoint: {self.base_url}")
        print(f"Model: {model}")
        print(f"User message: {user_message}")
        print(f"System message: {system_message}")
        print(f"Max tokens: {max_tokens}")
        print(f"Temperature: {temperature}")
        print("-" * 50)
        
        try:
            response = requests.post(
                self.base_url, 
                headers=self.headers, 
                json=data, 
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            
            # Extract the content (equivalent to jq -r '.choices[0].message.content')
            content = result["choices"][0]["message"]["content"]
            return content
            
        except requests.exceptions.Timeout:
            print("❌ Request timed out")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ Connection error - check if the server is running")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP error: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response text: {e.response.text}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test if the API endpoint is accessible"""
        try:
            # Try a minimal POST request to test connectivity
            test_data = {
                "model": "openchat/openchat-3.5-1210",
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 10,
                "temperature": 0.1
            }
            response = requests.post(self.base_url, headers=self.headers, json=test_data, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def run_comprehensive_test(self):
        """Run a comprehensive test suite"""
        print("=" * 60)
        print("Mistral Deployment Test Suite")
        print("=" * 60)
        
        # Test 1: Basic connection
        print("\n1. Testing API connection...")
        if self.test_connection():
            print("✅ API endpoint is accessible")
        else:
            print("❌ API endpoint is not accessible")
            print("Please check if the Mistral server is running at:", self.base_url)
            return
        
        # Test 2: Basic chat (exact curl command equivalent)
        print("\n2. Testing basic chat (curl equivalent)...")
        response = self.test_basic_chat()
        if response:
            print("✅ Basic chat test successful!")
            print(f"Response: {response}")
        else:
            print("❌ Basic chat test failed!")
        
        # Test 3: Different temperature setting
        print("\n3. Testing with temperature = 0.1 (project default)...")
        response = self.test_basic_chat(
            user_message="What is the capital of France?",
            temperature=0.1
        )
        if response:
            print("✅ Temperature test successful!")
            print(f"Response: {response}")
        else:
            print("❌ Temperature test failed!")
        
        # Test 4: JSON response test
        print("\n4. Testing JSON response capability...")
        json_test_prompt = "Respond with a JSON object containing the capital and population of Japan."
        response = self.test_basic_chat(
            user_message=json_test_prompt,
            temperature=0.1
        )
        if response:
            print("✅ JSON test successful!")
            print(f"Response: {response}")
            
            # Try to parse as JSON
            try:
                json.loads(response)
                print("✅ Response is valid JSON!")
            except json.JSONDecodeError:
                print("⚠️  Response is not valid JSON")
        else:
            print("❌ JSON test failed!")
        
        print("\n" + "=" * 60)
        print("Test suite completed!")
        print("=" * 60)

def main():
    """Run the Mistral deployment test"""
    tester = MistralDeploymentTester()
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()
