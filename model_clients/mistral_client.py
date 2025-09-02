#!/usr/bin/env python3
"""
Mistral model client for conversation analysis
Uses local OpenChat server running Mistral model
"""

import requests
import os
import sys
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_clients.base_client import BaseModelClient
from config import OPENCHAT_API_URL, OPENCHAT_MODEL, OPENCHAT_MAX_TOKENS, OPENCHAT_TEMPERATURE


class MistralClient(BaseModelClient):
    """Client for communicating with local OpenChat server (running Mistral model)"""
    
    def __init__(self):
        super().__init__("Mistral")
        self.base_url = OPENCHAT_API_URL
        self.model = OPENCHAT_MODEL
        self.max_tokens = OPENCHAT_MAX_TOKENS
        self.temperature = OPENCHAT_TEMPERATURE
        self.headers = {"Content-Type": "application/json"}
    
    def initialize(self) -> bool:
        """Initialize the Mistral client"""
        try:
            # Test connection to verify initialization
            if self.test_connection():
                self.initialized = True
                return True
            else:
                self.initialized = False
                return False
        except Exception as e:
            print(f"Mistral client initialization failed: {e}")
            self.initialized = False
            return False
    
    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        """Analyze conversation using Mistral API (via OpenChat)"""
        try:
            # Enhanced prompt with JSON formatting instructions
            enhanced_prompt = f"""{prompt}

CRITICAL: You must respond with ONLY a valid JSON object. No additional text before or after.

Required JSON format:
{{"Value": "Met" or "Not Met", "Evidence": "detailed explanation"}}

Transcript:
{transcript}"""
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that ALWAYS responds with ONLY valid JSON in the exact format requested. Never add explanatory text before or after the JSON. Use double quotes and ensure the JSON is properly formatted."},
                    {"role": "user", "content": enhanced_prompt}
                ],
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
            }
            
            response = requests.post(
                self.base_url, 
                headers=self.headers, 
                json=data, 
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def test_connection(self) -> bool:
        """Test if the OpenChat server is accessible"""
        try:
            response = self.analyze_conversation("Hello, this is a test message.", "Test transcript")
            return not response.startswith("Error:")
        except Exception as e:
            print(f"OpenChat connection test failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get Mistral model information"""
        base_info = super().get_model_info()
        base_info.update({
            'api_url': self.base_url,
            'model': self.model,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature
        })
        return base_info
