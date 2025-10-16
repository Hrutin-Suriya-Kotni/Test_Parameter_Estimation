#!/usr/bin/env python3
"""
Server3 Base OpenChat Mistral Client
API: http://27.111.72.53:8000/chat
Format: OpenAI-compatible
"""

import requests
import os
import sys
import time
from typing import Dict, Any, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_clients.base_client import BaseModelClient
from model_config import ModelConfig


class Server3OpenChatMistralClient(BaseModelClient):
    """Client for Server3 OpenChat Mistral API"""
    
    def __init__(self):
        super().__init__("Server3_OpenChat_Mistral")
        
        print("🔍 DEBUG: Loading Server3 configuration...")
        
        # Load config
        config = ModelConfig.get_model_config('server3_base_openchat_mistral') or {}
        print(f"🔍 DEBUG: Config loaded: {config.get('display_name', 'N/A')}")
        
        cfg = config.get('config', {})
        print(f"🔍 DEBUG: API URL from config: {cfg.get('api_url', 'NOT FOUND')}")
        
        self.api_url = cfg.get('api_url', 'http://27.111.72.53:3333/v1/chat/completions')
        self.model = cfg.get('model', 'openchat/openchat-3.5-1210')
        self.max_tokens = cfg.get('max_tokens', 512)
        self.temperature = cfg.get('temperature', 0.1)
        self.headers = {"Content-Type": "application/json"}
        
        # Metadata tracking
        self.last_request_metadata = {}
        
        print(f"✅ Server3 OpenChat Mistral client initialized")
        print(f"   API: {self.api_url}")
        print(f"   Model: {self.model}")
        print(f"   Max Tokens: {self.max_tokens}")
        print(f"   Temperature: {self.temperature}")
    
    def initialize(self) -> bool:
        """Initialize the client"""
        try:
            print(f"🔍 DEBUG: Testing connection to {self.api_url}...")
            if self.test_connection():
                self.initialized = True
                print("🔍 DEBUG: Connection test passed!")
                return True
            print("🔍 DEBUG: Connection test failed!")
            return False
        except Exception as e:
            print(f"❌ Server3 initialization failed: {e}")
            return False
    
    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        """Analyze conversation and track metadata"""
        try:
            print(f"🔍 DEBUG: analyze_conversation called")
            print(f"🔍 DEBUG: API URL: {self.api_url}")
            
            # Build enhanced prompt
            enhanced_prompt = f"""{prompt}

CRITICAL: Respond with ONLY valid JSON.
{{"Value": "Met" or "Not Met", "Evidence": "detailed explanation"}}

Transcript:
{transcript}"""
            
            print(f"🔍 DEBUG: Prompt length: {len(enhanced_prompt)} chars")
            
            # Prepare request (shortened system message for Server3 stability)
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "Respond with ONLY valid JSON."},
                    {"role": "user", "content": enhanced_prompt}
                ],
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            print(f"🔍 DEBUG: Making API call to {self.api_url}...")
            
            # Track start time
            start_time = time.time()
            
            # Make API call (very long timeout for Server3 - it's extremely slow)
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=data,
                timeout=300  # 5 minutes - Server 3 is very slow
            )
            
            print(f"🔍 DEBUG: Response status: {response.status_code}")
            
            # Track end time
            end_time = time.time()
            latency = end_time - start_time
            
            response.raise_for_status()
            result = response.json()
            
            # Extract response content
            content = result["choices"][0]["message"]["content"]
            
            # Extract and store metadata
            usage = result.get("usage", {})
            self.last_request_metadata = {
                "latency_seconds": round(latency, 3),
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
                "model": result.get("model", self.model),
                "finish_reason": result["choices"][0].get("finish_reason", "unknown"),
                "api_endpoint": self.api_url,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
            
            return content
            
        except Exception as e:
            self.last_request_metadata = {
                "error": str(e),
                "latency_seconds": 0,
                "total_tokens": 0
            }
            return f"Error: {str(e)}"
    
    def test_connection(self) -> bool:
        """Test if the API is accessible"""
        try:
            print(f"🔍 DEBUG: test_connection - Testing {self.api_url}")
            
            # Simple test with minimal prompt
            data = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": "Hi"}
                ],
                "max_tokens": 5,
                "temperature": 0.7
            }
            
            print(f"🔍 DEBUG: Sending test request...")
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=data,
                timeout=300  # Very long timeout (5 minutes) - Server 3 is very slow
            )
            
            print(f"🔍 DEBUG: Test response status: {response.status_code}")
            response.raise_for_status()
            result = response.json()
            
            success = "choices" in result and len(result["choices"]) > 0
            print(f"🔍 DEBUG: Connection test result: {success}")
            return success
        except Exception as e:
            print(f"❌ Server3 connection test failed: {e}")
            print(f"🔍 DEBUG: Exception type: {type(e).__name__}")
            return False
    
    def get_last_metadata(self) -> Dict[str, Any]:
        """Get metadata from last API call"""
        return self.last_request_metadata.copy()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        base_info = super().get_model_info()
        base_info.update({
            'api_url': self.api_url,
            'model': self.model,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
            'api_type': 'OpenAI-compatible'
        })
        return base_info


if __name__ == "__main__":
    print("🧪 Testing Server3 OpenChat Mistral Client")
    print("="*60)
    
    client = Server3OpenChatMistralClient()
    
    if client.initialize():
        print("\n✅ Client initialized successfully")
        
        # Test with simple prompt
        print("\n🔍 Testing API call...")
        response = client.analyze_conversation(
            "Analyze this conversation",
            "Agent: Hello! Customer: Hi there!"
        )
        
        print(f"\n📊 Response: {response[:200]}...")
        print(f"\n📈 Metadata: {client.get_last_metadata()}")
    else:
        print("\n❌ Client initialization failed")

