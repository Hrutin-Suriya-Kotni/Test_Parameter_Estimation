#!/usr/bin/env python3
"""
Simple test script that exactly mirrors the curl command:

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

def test_mistral_curl_equivalent():
    """Test the exact same request as the curl command"""
    
    url = "http://192.168.30.239:8000/chat"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "model": "openchat/openchat-3.5-1210",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of India?"}
        ],
        "max_tokens": 500,
        "temperature": 1
    }
    
    print("Testing deployed Mistral model...")
    print(f"URL: {url}")
    print(f"Model: {data['model']}")
    print(f"User message: {data['messages'][1]['content']}")
    print(f"Max tokens: {data['max_tokens']}")
    print(f"Temperature: {data['temperature']}")
    print("-" * 50)
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        print("✅ Success!")
        print(f"Response: {content}")
        return content
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - check if the server is running")
        return None
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP error: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response text: {e.response.text}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

if __name__ == "__main__":
    test_mistral_curl_equivalent()
