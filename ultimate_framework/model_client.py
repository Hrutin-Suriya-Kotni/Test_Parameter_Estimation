"""
Model Client - Handles communication with different model APIs
Supports: vLLM servers, Gemini API
"""

import requests
import json
import time
import os
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import logging

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

logger = logging.getLogger(__name__)


class BaseModelClient(ABC):
    """Base class for all model clients"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get('name', 'Unknown Model')
        self.timeout = config.get('timeout', 30)
        logger.info(f"Initialized {self.name}")
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate response from the model
        
        Args:
            prompt: User prompt/transcript
            system_prompt: Optional system instruction
        
        Returns:
            Dict with keys: response, success, error (if failed), latency
        """
        pass
    
    def test_connection(self) -> bool:
        """Test if the model is accessible"""
        try:
            result = self.generate("Hello", system_prompt="You are a test assistant.")
            return result['success']
        except Exception as e:
            logger.error(f"Connection test failed for {self.name}: {e}")
            return False


class vLLMClient(BaseModelClient):
    """Client for vLLM-served models"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.endpoint = config['endpoint']
        self.model_name = config['model_name']
        self.temperature = config.get('temperature', 0.3)
        self.max_tokens = config.get('max_tokens', 500)
        
        # Test connection
        if not self._test_health():
            logger.warning(f"Health check failed for {self.name} at {self.endpoint}")
    
    def _test_health(self) -> bool:
        """Quick health check"""
        try:
            # Try to hit the health endpoint if available
            base_url = self.endpoint.rsplit('/v1/', 1)[0]
            health_url = f"{base_url}/health"
            response = requests.get(health_url, timeout=5)
            return response.status_code == 200
        except:
            # If health endpoint doesn't exist, that's okay
            return True
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Generate response from vLLM server"""
        start_time = time.time()
        
        # Construct messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Smart max_tokens calculation to avoid context length errors
        # Rough estimate: 1 token ≈ 4 characters
        estimated_input_tokens = (len(prompt) + len(system_prompt or "")) // 4
        model_max_length = 8192  # OpenChat Mistral context limit
        
        # Calculate available tokens with 5% safety buffer
        available_tokens = int((model_max_length - estimated_input_tokens) * 0.95)
        adjusted_max_tokens = min(self.max_tokens, max(available_tokens, 50))
        
        # Log if adjustment needed
        if adjusted_max_tokens < self.max_tokens:
            logger.warning(f"Long input (~{estimated_input_tokens} tokens). " +
                         f"Adjusted max_tokens: {self.max_tokens} → {adjusted_max_tokens}")
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": adjusted_max_tokens
        }
        
        try:
            response = requests.post(
                self.endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=self.timeout
            )
            
            latency = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                response_text = data['choices'][0]['message']['content']
                
                return {
                    'success': True,
                    'response': response_text,
                    'latency': latency,
                    'model': self.name,
                    'raw_response': data
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text}",
                    'latency': latency,
                    'model': self.name
                }
        
        except requests.Timeout:
            return {
                'success': False,
                'error': f"Request timeout after {self.timeout}s",
                'latency': time.time() - start_time,
                'model': self.name
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'latency': time.time() - start_time,
                'model': self.name
            }


class GeminiClient(BaseModelClient):
    """Client for Google Gemini API"""
    
    def __init__(self, config: Dict[str, Any]):
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai not installed. Run: pip install google-generativeai")
        
        super().__init__(config)
        
        # Get API key from environment
        api_key_env = config.get('api_key_env', 'GEMINI_API_KEY')
        api_key = os.getenv(api_key_env)
        
        if not api_key:
            raise ValueError(f"API key not found in environment variable: {api_key_env}")
        
        genai.configure(api_key=api_key)
        
        self.model_name = config['model_name']
        self.temperature = config.get('temperature', 0.3)
        self.max_tokens = config.get('max_tokens', 500)
        
        # Initialize model
        self.model = genai.GenerativeModel(self.model_name)
        
        # Safety settings (permissive for call center transcripts)
        self.safety_settings = {
            'HATE': 'BLOCK_NONE',
            'HARASSMENT': 'BLOCK_NONE',
            'SEXUAL': 'BLOCK_NONE',
            'DANGEROUS': 'BLOCK_NONE'
        }
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Generate response from Gemini API"""
        start_time = time.time()
        
        # Combine system prompt and user prompt
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        try:
            response = self.model.generate_content(
                full_prompt,
                safety_settings=self.safety_settings,
                generation_config={
                    'temperature': self.temperature,
                    'max_output_tokens': self.max_tokens
                }
            )
            
            latency = time.time() - start_time
            
            return {
                'success': True,
                'response': response.text,
                'latency': latency,
                'model': self.name,
                'raw_response': str(response)
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'latency': time.time() - start_time,
                'model': self.name
            }


class ModelClientFactory:
    """Factory to create appropriate model client"""
    
    @staticmethod
    def create_client(config: Dict[str, Any]) -> BaseModelClient:
        """
        Create a model client based on configuration
        
        Args:
            config: Model configuration dict
        
        Returns:
            Appropriate model client instance
        """
        model_type = config.get('type', 'vllm').lower()
        
        if model_type == 'vllm':
            return vLLMClient(config)
        elif model_type == 'gemini':
            return GeminiClient(config)
        else:
            raise ValueError(f"Unknown model type: {model_type}. Supported: vllm, gemini")


if __name__ == "__main__":
    # Test the model clients
    logging.basicConfig(level=logging.INFO)
    
    # Test vLLM client (if available)
    test_vllm_config = {
        'name': 'Test vLLM',
        'type': 'vllm',
        'endpoint': 'http://192.168.30.252:8000/v1/chat/completions',
        'model_name': 'openchat/openchat-3.5-1210',
        'temperature': 0.3,
        'max_tokens': 100
    }
    
    print("\n=== Testing vLLM Client ===")
    try:
        client = ModelClientFactory.create_client(test_vllm_config)
        result = client.generate("Say 'Hello, I am working!' in one sentence.")
        
        if result['success']:
            print(f"✅ Success! Latency: {result['latency']:.2f}s")
            print(f"Response: {result['response'][:200]}")
        else:
            print(f"❌ Failed: {result['error']}")
    except Exception as e:
        print(f"❌ Error: {e}")

