#!/usr/bin/env python3
"""
Server5 Base Mistral Client
API: http://27.111.72.51:8000/generate
Format: Simple prompt-response
"""

import requests
import os
import sys
import time
from typing import Dict, Any, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_clients.base_client import BaseModelClient
from model_config import ModelConfig


class Server5BaseMistralClient(BaseModelClient):
    """Client for Server5 Base Mistral API"""
    
    def __init__(self):
        super().__init__("Server5_Base_Mistral")
        
        # Load config
        config = ModelConfig.get_model_config('server5_base_mistral') or {}
        cfg = config.get('config', {})
        
        self.api_url = cfg.get('api_url', 'http://27.111.72.51:8000/generate')
        self.max_tokens = cfg.get('max_new_tokens', 512)
        self.temperature = cfg.get('temperature', 0.1)
        self.headers = {"Content-Type": "application/json"}
        
        # Metadata tracking
        self.last_request_metadata = {}
        
        print(f"✅ Server5 Base Mistral client initialized")
        print(f"   API: {self.api_url}")
    
    def initialize(self) -> bool:
        """Initialize the client"""
        try:
            if self.test_connection():
                self.initialized = True
                return True
            return False
        except Exception as e:
            print(f"Server5 initialization failed: {e}")
            return False
    
    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        """Analyze conversation and track metadata"""
        try:
            # Build enhanced prompt
            enhanced_prompt = f"""{prompt}

CRITICAL: Respond with ONLY valid JSON.
{{"Value": "Met" or "Not Met", "Evidence": "detailed explanation"}}

Transcript:
{transcript}"""
            
            # Prepare request (Server5 uses "prompt" not "messages")
            data = {
                "prompt": enhanced_prompt,
                "max_new_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            # Track start time
            start_time = time.time()
            
            # Make API call
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=data,
                timeout=120
            )
            
            # Track end time
            end_time = time.time()
            latency = end_time - start_time
            
            response.raise_for_status()
            result = response.json()
            
            # Extract response content (Server5 returns {"response": "..."})
            content = result.get("response", "")
            
            # Estimate tokens (approximate - Server5 doesn't provide token counts)
            prompt_tokens_estimate = len(enhanced_prompt.split())
            completion_tokens_estimate = len(content.split())
            total_tokens_estimate = prompt_tokens_estimate + completion_tokens_estimate
            
            # Store metadata
            self.last_request_metadata = {
                "latency_seconds": round(latency, 3),
                "prompt_tokens_estimate": prompt_tokens_estimate,
                "completion_tokens_estimate": completion_tokens_estimate,
                "total_tokens_estimate": total_tokens_estimate,
                "response_length_chars": len(content),
                "api_endpoint": self.api_url,
                "temperature": self.temperature,
                "max_new_tokens": self.max_tokens,
                "note": "Token counts are estimates (API doesn't provide exact counts)"
            }
            
            return content
            
        except Exception as e:
            self.last_request_metadata = {
                "error": str(e),
                "latency_seconds": 0,
                "total_tokens_estimate": 0
            }
            return f"Error: {str(e)}"
    
    def test_connection(self) -> bool:
        """Test if the API is accessible"""
        try:
            # Simple test with minimal prompt
            data = {
                "prompt": "Say hi",
                "max_new_tokens": 10,
                "temperature": 0.7
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return "response" in result and len(result["response"]) > 0
        except Exception as e:
            print(f"Server5 connection test failed: {e}")
            return False
    
    def get_last_metadata(self) -> Dict[str, Any]:
        """Get metadata from last API call"""
        return self.last_request_metadata.copy()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        base_info = super().get_model_info()
        base_info.update({
            'api_url': self.api_url,
            'max_new_tokens': self.max_tokens,
            'temperature': self.temperature,
            'api_type': 'Simple prompt-response',
            'note': 'Token counts are estimates'
        })
        return base_info


if __name__ == "__main__":
    print("🧪 Testing Server5 Base Mistral Client")
    print("="*60)
    
    client = Server5BaseMistralClient()
    
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

