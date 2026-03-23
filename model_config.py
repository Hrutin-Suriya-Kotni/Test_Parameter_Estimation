#!/usr/bin/env python3
"""
Model configuration for conversation analysis
Defines available models and their configurations
"""

from typing import Dict, Any, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ModelConfig:
    """Configuration for all available models"""
    
    # Model registry - add new models here
    AVAILABLE_MODELS = {
        'mistral': {
            'class_name': 'MistralClient',
            'module_path': 'model_clients.mistral_client',
            'display_name': 'Mistral (NVIDIA NIM)',
            'description': 'Mistral via NVIDIA NIM OpenAI-compatible API',
            'requires_api_key': True,
            'api_key_env_var': 'NVIDIA_API_KEY',
            'config': {
                'api_url': 'https://integrate.api.nvidia.com/v1',
                'model': 'mistralai/mistral-7b-instruct-v0.3',
                'temperature': 0.1,
            }
        },
        'gemini': {
            'class_name': 'GeminiClient',
            'module_path': 'model_clients.gemini_client',
            'display_name': 'Google Gemini',
            'description': 'Google Gemini 1.5 Flash model via API',
            'requires_api_key': True,
            'api_key_env_var': 'GEMINI_API_KEY',
            'config': {
                'model': 'gemini-2.5-flash',
                'temperature': 0.1,
            }
        },
        'llama': {
            'class_name': 'LlamaClient',
            'module_path': 'model_clients.llama_client',
            'display_name': 'Meta Llama 3 8B Instruct',
            'description': 'meta/llama-3.1-8b-instruct via NVIDIA NIM OpenAI-compatible API',
            'requires_api_key': True,
            'api_key_env_var': 'NVIDIA_API_KEY',
            'config': {
                'api_url': 'https://integrate.api.nvidia.com/v1',
                'model': 'meta/llama-3.1-8b-instruct',
                'temperature': 0.1
            }
        },
        'qwen': {
            'class_name': 'QwenClient',
            'module_path': 'model_clients.qwen_client',
            'display_name': 'Qwen 2.5 7B Instruct',
            'description': 'qwen/qwen2.5-7b-instruct via NVIDIA NIM OpenAI-compatible API',
            'requires_api_key': True,
            'api_key_env_var': 'NVIDIA_API_KEY',
            'config': {
                'api_url': 'https://integrate.api.nvidia.com/v1',
                'model': 'qwen/qwen2.5-7b-instruct',
                'temperature': 0.1
            }
        },
        'mistral_v0_2': {
            'class_name': 'MistralV02Client',
            'module_path': 'model_clients.mistral_v0_2_client',
            'display_name': 'Mistral 7B Instruct v0.2',
            'description': 'mistralai/mistral-7b-instruct-v0.2 via NVIDIA NIM OpenAI-compatible API',
            'requires_api_key': True,
            'api_key_env_var': 'NVIDIA_API_KEY',
            'config': {
                'api_url': 'https://integrate.api.nvidia.com/v1',
                'model': 'mistralai/mistral-7b-instruct-v0.2',
                'temperature': 0.1
            }
        },
        'gemma': {
            'class_name': 'GemmaClient',
            'module_path': 'model_clients.gemma_client',
            'display_name': 'Gemma 2 9B',
            'description': 'google/gemma-2-9b via NVIDIA NIM OpenAI-compatible API',
            'requires_api_key': True,
            'api_key_env_var': 'NVIDIA_API_KEY',
            'config': {
                'api_url': 'https://integrate.api.nvidia.com/v1',
                'model': 'google/gemma-2-9b-it',
                'temperature': 0.1
            }
        },
        'gemma_inhouse': {
            'class_name': 'GemmaInhouseClient',
            'module_path': 'model_clients.gemma_inhouse_client',
            'display_name': 'Gemma In-house (vLLM)',
            'description': 'In-house vLLM server OpenAI-compatible /v1/chat/completions',
            'requires_api_key': False,
            'api_key_env_var': 'GEMMA_INHOUSE_API_KEY',
            'config': {
                'api_url': 'http://192.168.30.251:5000/v1',
                'model': 'google/gemma-2-9b-it',
                'temperature': 0.1
            }
        },
        'qwen_inhouse': {
            'class_name': 'QwenInhouseClient',
            'module_path': 'model_clients.qwen_inhouse_client',
            'display_name': 'Qwen In-house (vLLM)',
            'description': 'In-house vLLM Qwen2.5-7B-Instruct OpenAI-compatible /v1/chat/completions',
            'requires_api_key': False,
            'api_key_env_var': 'QWEN_INHOUSE_API_KEY',
            'config': {
                'api_url': 'http://192.168.30.121:5000/v1',
                'model': 'Qwen/Qwen2.5-7B-Instruct',
                'temperature': 0.1
            }
        }
        # Add new models here following the same pattern
        # 'new_model': {
        #     'class_name': 'NewModelClient',
        #     'module_path': 'model_clients.new_model_client',
        #     'display_name': 'New Model',
        #     'description': 'Description of the new model',
        #     'requires_api_key': True,
        #     'api_key_env_var': 'NEW_MODEL_API_KEY',
        #     'config': {
        #         'api_url': 'https://api.newmodel.com',
        #         'model': 'new-model-v1',
        #         'max_tokens': 512,
        #         'temperature': 0.1
        #     }
        # }
    }
    
    @classmethod
    def get_available_models(cls) -> List[str]:
        """Get list of available model names"""
        return list(cls.AVAILABLE_MODELS.keys())
    
    @classmethod
    def get_model_config(cls, model_name: str) -> Dict[str, Any]:
        """Get configuration for a specific model"""
        return cls.AVAILABLE_MODELS.get(model_name, {})
    
    @classmethod
    def is_model_available(cls, model_name: str) -> bool:
        """Check if a model is available"""
        return model_name in cls.AVAILABLE_MODELS
    
    @classmethod
    def get_model_display_name(cls, model_name: str) -> str:
        """Get display name for a model"""
        config = cls.get_model_config(model_name)
        return config.get('display_name', model_name)
    
    @classmethod
    def check_model_requirements(cls, model_name: str) -> Dict[str, Any]:
        """Check if model requirements are met"""
        config = cls.get_model_config(model_name)
        if not config:
            return {'available': False, 'reason': 'Model not found'}
        
        # Check API key requirement
        if config.get('requires_api_key', False):
            api_key_var = config.get('api_key_env_var')
            if api_key_var:
                api_key = os.getenv(api_key_var)
                if not api_key:
                    return {
                        'available': False, 
                        'reason': f'API key not found. Please set {api_key_var} in your .env file'
                    }
        
        return {'available': True, 'reason': 'All requirements met'}
    
    @classmethod
    def get_available_models_with_status(cls) -> Dict[str, Dict[str, Any]]:
        """Get all models with their availability status"""
        models_status = {}
        
        for model_name in cls.AVAILABLE_MODELS.keys():
            config = cls.get_model_config(model_name)
            status = cls.check_model_requirements(model_name)
            
            models_status[model_name] = {
                'config': config,
                'status': status,
                'display_name': config.get('display_name', model_name),
                'description': config.get('description', 'No description available')
            }
        
        return models_status
    
    @classmethod
    def print_model_status(cls):
        """Print status of all available models"""
        print("🤖 Available Models Status:")
        print("=" * 50)
        
        models_status = cls.get_available_models_with_status()
        
        for model_name, info in models_status.items():
            status_icon = "✅" if info['status']['available'] else "❌"
            print(f"{status_icon} {info['display_name']} ({model_name})")
            print(f"   Description: {info['description']}")
            if not info['status']['available']:
                print(f"   Issue: {info['status']['reason']}")
            print()


# Test function
def test_model_config():
    """Test the model configuration"""
    print("🧪 Testing Model Configuration")
    print("=" * 40)
    
    config = ModelConfig()
    
    # Print available models
    print(f"Available models: {config.get_available_models()}")
    
    # Print model status
    config.print_model_status()
    
    # Test individual model configs
    for model_name in config.get_available_models():
        print(f"\n{model_name.upper()} Configuration:")
        model_config = config.get_model_config(model_name)
        for key, value in model_config.items():
            if key != 'config':
                print(f"  {key}: {value}")
        print(f"  config: {model_config.get('config', {})}")


if __name__ == "__main__":
    test_model_config()
