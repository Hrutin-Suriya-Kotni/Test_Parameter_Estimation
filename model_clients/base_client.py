#!/usr/bin/env python3
"""
Base model client interface for conversation analysis
Provides a common interface for all AI model clients
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
import time
from datetime import datetime


class BaseModelClient(ABC):
    """Abstract base class for all model clients"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.initialized = False
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the model client"""
        pass
    
    @abstractmethod
    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        """Analyze conversation using the model"""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """Test if the model is accessible"""
        pass
    
    def parse_json_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Parse JSON response from model"""
        try:
            # Clean the response
            cleaned = response_text.strip()
            
            # Try to extract JSON from response
            if '{' in cleaned and '}' in cleaned:
                start = cleaned.find('{')
                end = cleaned.rfind('}') + 1
                json_str = cleaned[start:end]
                
                # Try to parse the JSON
                parsed = json.loads(json_str)
                
                # Validate the structure
                if isinstance(parsed, dict) and 'Value' in parsed:
                    return parsed
                else:
                    return None
            else:
                return None
                
        except json.JSONDecodeError:
            return None
        except Exception:
            return None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            'model_name': self.model_name,
            'initialized': self.initialized,
            'timestamp': datetime.now().isoformat()
        }
    
    def __str__(self) -> str:
        return f"{self.model_name}Client"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model_name='{self.model_name}')"
