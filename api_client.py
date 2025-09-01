import requests
import json
import time
from typing import Optional, Dict, Any
from config import (
    OPENCHAT_API_URL, 
    OPENCHAT_MODEL, 
    OPENCHAT_MAX_TOKENS, 
    OPENCHAT_TEMPERATURE,
    REQUEST_TIMEOUT
)

class OpenChatAPIClient:
    """Client for communicating with the local OpenChat API"""
    
    def __init__(self, base_url: str = OPENCHAT_API_URL):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
    
    def call_api(self, 
                 user_prompt: str, 
                 system_prompt: str = "You are a helpful assistant.",
                 model: str = OPENCHAT_MODEL,
                 max_tokens: int = OPENCHAT_MAX_TOKENS,
                 temperature: float = OPENCHAT_TEMPERATURE) -> Optional[str]:
        """
        Make a call to the local OpenChat API
        
        Args:
            user_prompt: The user's message
            system_prompt: The system prompt
            model: The model to use
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            The API response content or None if failed
        """
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        # Adjust timeout based on prompt length
        prompt_length = len(user_prompt)
        if prompt_length > 5000:
            timeout = REQUEST_TIMEOUT * 3  # 3x timeout for very long conversations
        elif prompt_length > 2000:
            timeout = REQUEST_TIMEOUT * 2  # 2x timeout for long conversations
        else:
            timeout = REQUEST_TIMEOUT
        
        try:
            response = requests.post(
                self.base_url, 
                headers=self.headers, 
                json=data, 
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.Timeout:
            print(f"Timeout error (prompt length: {prompt_length} chars, timeout: {timeout}s)")
            return None
        except Exception as e:
            print(f"Error during API call: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test if the API is accessible"""
        try:
            response = self.call_api("Hello, this is a test message.")
            return response is not None
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

# Global API client instance
api_client = OpenChatAPIClient()

## Gemini client removed to focus solely on local Mistral via OpenChat

# OpenChat Client (Local Mistral Model)
class MistralClient:
    """Client for communicating with local OpenChat server (running Mistral model)"""
    
    def __init__(self):
        from config import OPENCHAT_API_URL, OPENCHAT_MODEL, OPENCHAT_MAX_TOKENS, OPENCHAT_TEMPERATURE
        
        self.base_url = OPENCHAT_API_URL
        self.model = OPENCHAT_MODEL
        self.max_tokens = OPENCHAT_MAX_TOKENS
        self.temperature = OPENCHAT_TEMPERATURE
        self.headers = {"Content-Type": "application/json"}
    
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