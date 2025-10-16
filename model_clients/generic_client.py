#!/usr/bin/env python3
"""
Generic model client template for conversation analysis
This template makes it easy to integrate ANY AI API with minimal code

HOW TO USE:
1. Copy this file and rename it (e.g., your_model_client.py)
2. Update the API_TYPE constant with your API type
3. Implement the 3 simple methods: initialize(), analyze_conversation(), test_connection()
4. Add your model config to model_config.py
5. Done! Your model will work with all test runners automatically
"""

import os
import sys
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_clients.base_client import BaseModelClient
from model_config import ModelConfig
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GenericClient(BaseModelClient):
    """
    Generic client template for any AI API
    
    CUSTOMIZATION REQUIRED:
    1. Change class name to match your model (e.g., ClaudeClient, GPT4Client)
    2. Update API_TYPE below
    3. Implement the three methods marked with # TODO
    """
    
    # ==================== CUSTOMIZE THIS ====================
    API_TYPE = "generic"  # Change to: "openai", "anthropic", "huggingface", etc.
    # ========================================================
    
    def __init__(self):
        """
        Initialize the generic client
        Loads configuration from model_config.py automatically
        """
        super().__init__(self.API_TYPE.capitalize())
        
        # Load model configuration from model_config.py
        # This keeps all settings in one place!
        model_cfg = ModelConfig.get_model_config(self.API_TYPE) or {}
        self.config = model_cfg.get('config', {})
        
        # Common configuration values
        self.api_url = self.config.get('api_url', '')
        self.model_name = self.config.get('model', '')
        self.max_tokens = self.config.get('max_tokens', 512)
        self.temperature = self.config.get('temperature', 0.1)
        
        # API key handling (if required)
        self.api_key_env_var = model_cfg.get('api_key_env_var')
        self.api_key = None
        
        print(f"✅ {self.API_TYPE.capitalize()} client configuration loaded")
    
    def initialize(self) -> bool:
        """
        Initialize your model client
        
        TODO: Implement this method to:
        1. Load API key (if needed)
        2. Initialize your API client/library
        3. Test that everything is working
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # ==================== CUSTOMIZE THIS ====================
            
            # Example: Load API key from environment
            if self.api_key_env_var:
                self.api_key = os.getenv(self.api_key_env_var)
                if not self.api_key:
                    raise ValueError(f"{self.api_key_env_var} not found in .env file")
            
            # Example: Initialize your API client
            # For REST APIs, you might not need anything here
            # For SDK-based APIs (like Gemini), initialize the client here
            
            # Example:
            # import your_api_library
            # your_api_library.configure(api_key=self.api_key)
            # self.client = your_api_library.Client(model=self.model_name)
            
            # ========================================================
            
            # Test connection to verify initialization
            if self.test_connection():
                self.initialized = True
                print(f"✅ {self.model_name} initialized successfully")
                return True
            else:
                self.initialized = False
                return False
                
        except Exception as e:
            print(f"❌ {self.model_name} initialization failed: {e}")
            self.initialized = False
            return False
    
    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        """
        Send conversation to your AI model for analysis
        
        TODO: Implement this method to:
        1. Format the prompt + transcript for your API
        2. Make API call
        3. Return the model's response as a string
        
        Args:
            prompt: Assessment prompt with guidelines
            transcript: Customer conversation transcript
            
        Returns:
            str: Model response (should be JSON format)
        """
        try:
            # ==================== CUSTOMIZE THIS ====================
            
            # Build the enhanced prompt with JSON instructions
            # This ensures consistent output format across all models
            enhanced_prompt = f"""{prompt}

CRITICAL: You must respond with ONLY a valid JSON object. No additional text before or after.

Required JSON format:
{{"Value": "Met" or "Not Met", "Evidence": "detailed explanation"}}

Transcript:
{transcript}"""
            
            # OPTION 1: REST API (like OpenAI, Mistral via OpenChat)
            # -------------------------------------------------------
            # import requests
            # 
            # headers = {
            #     "Content-Type": "application/json",
            #     "Authorization": f"Bearer {self.api_key}"  # if needed
            # }
            # 
            # data = {
            #     "model": self.model_name,
            #     "messages": [
            #         {"role": "system", "content": "You are a helpful assistant that ALWAYS responds with ONLY valid JSON."},
            #         {"role": "user", "content": enhanced_prompt}
            #     ],
            #     "max_tokens": self.max_tokens,
            #     "temperature": self.temperature
            # }
            # 
            # response = requests.post(
            #     self.api_url,
            #     headers=headers,
            #     json=data,
            #     timeout=60
            # )
            # response.raise_for_status()
            # result = response.json()
            # return result["choices"][0]["message"]["content"]  # Adjust based on your API response format
            
            
            # OPTION 2: SDK-based API (like Google Gemini)
            # ----------------------------------------------
            # response = self.client.generate_content(
            #     enhanced_prompt,
            #     generation_config={
            #         'temperature': self.temperature,
            #         'max_output_tokens': self.max_tokens
            #     }
            # )
            # return response.text
            
            
            # OPTION 3: Local model or custom implementation
            # -----------------------------------------------
            # return your_custom_model.predict(enhanced_prompt)
            
            
            # ========================================================
            
            # Placeholder return - REMOVE THIS when implementing
            return '{"Value": "Not Implemented", "Evidence": "Please implement analyze_conversation() method"}'
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def test_connection(self) -> bool:
        """
        Test if your model is accessible
        
        TODO: Implement this method to verify:
        1. API is reachable
        2. Authentication works
        3. Model can respond
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # ==================== CUSTOMIZE THIS ====================
            
            # Simple test: try to analyze a dummy conversation
            response = self.analyze_conversation(
                "Test prompt", 
                "Test transcript"
            )
            
            # Check if response is valid (not an error)
            # Adjust this based on your error handling
            return not response.startswith("Error:")
            
            # Alternative: Make a simple ping/health check API call
            # import requests
            # health_check = requests.get(f"{self.api_url}/health", timeout=5)
            # return health_check.status_code == 200
            
            # ========================================================
            
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model information (already implemented, no changes needed)
        """
        base_info = super().get_model_info()
        base_info.update({
            'api_type': self.API_TYPE,
            'api_url': self.api_url,
            'model': self.model_name,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
            'api_key_configured': bool(self.api_key)
        })
        return base_info


# ============================================================================
# EXAMPLES: Popular API Integrations
# ============================================================================

class OpenAIClient(BaseModelClient):
    """Example: OpenAI GPT-4 Integration"""
    
    def __init__(self):
        super().__init__("OpenAI")
        model_cfg = ModelConfig.get_model_config('openai') or {}
        self.config = model_cfg.get('config', {})
        self.api_url = self.config.get('api_url', 'https://api.openai.com/v1/chat/completions')
        self.model = self.config.get('model', 'gpt-4')
        self.max_tokens = self.config.get('max_tokens', 512)
        self.temperature = self.config.get('temperature', 0.1)
        self.api_key = None
    
    def initialize(self) -> bool:
        try:
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY not found")
            
            if self.test_connection():
                self.initialized = True
                return True
            return False
        except Exception as e:
            print(f"OpenAI initialization failed: {e}")
            return False
    
    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        try:
            import requests
            
            enhanced_prompt = f"""{prompt}

CRITICAL: Respond with ONLY valid JSON.
{{"Value": "Met" or "Not Met", "Evidence": "explanation"}}

Transcript:
{transcript}"""
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that responds with ONLY valid JSON."},
                    {"role": "user", "content": enhanced_prompt}
                ],
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {str(e)}"
    
    def test_connection(self) -> bool:
        try:
            response = self.analyze_conversation("Test", "Test")
            return not response.startswith("Error:")
        except:
            return False


class AnthropicClient(BaseModelClient):
    """Example: Anthropic Claude Integration"""
    
    def __init__(self):
        super().__init__("Anthropic")
        model_cfg = ModelConfig.get_model_config('anthropic') or {}
        self.config = model_cfg.get('config', {})
        self.api_url = self.config.get('api_url', 'https://api.anthropic.com/v1/messages')
        self.model = self.config.get('model', 'claude-3-5-sonnet-20241022')
        self.max_tokens = self.config.get('max_tokens', 512)
        self.temperature = self.config.get('temperature', 0.1)
        self.api_key = None
    
    def initialize(self) -> bool:
        try:
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY not found")
            
            if self.test_connection():
                self.initialized = True
                return True
            return False
        except Exception as e:
            print(f"Anthropic initialization failed: {e}")
            return False
    
    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        try:
            import requests
            
            enhanced_prompt = f"""{prompt}

CRITICAL: Respond with ONLY valid JSON.
{{"Value": "Met" or "Not Met", "Evidence": "explanation"}}

Transcript:
{transcript}"""
            
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01"
            }
            
            data = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "messages": [
                    {"role": "user", "content": enhanced_prompt}
                ]
            }
            
            response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["content"][0]["text"]
        except Exception as e:
            return f"Error: {str(e)}"
    
    def test_connection(self) -> bool:
        try:
            response = self.analyze_conversation("Test", "Test")
            return not response.startswith("Error:")
        except:
            return False


# ============================================================================
# For testing this template directly
# ============================================================================
if __name__ == "__main__":
    print("🧪 Testing Generic Client Template")
    print("=" * 50)
    
    client = GenericClient()
    
    print("\n📋 Client Info:")
    print(client.get_model_info())
    
    print("\n⚠️  Note: This is a template. Please implement the methods before using!")

