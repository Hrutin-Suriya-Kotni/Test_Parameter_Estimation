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
            
            # Try to find all JSON objects and return the last valid one
            # This handles cases where the prompt is echoed back with examples
            if '{' in cleaned and '}' in cleaned:
                # Find all potential JSON objects by looking for {} pairs
                json_objects = []
                i = 0
                while i < len(cleaned):
                    if cleaned[i] == '{':
                        # Found a potential JSON start, find matching }
                        depth = 0
                        start = i
                        while i < len(cleaned):
                            if cleaned[i] == '{':
                                depth += 1
                            elif cleaned[i] == '}':
                                depth -= 1
                                if depth == 0:
                                    # Found complete JSON object
                                    json_str = cleaned[start:i+1]
                                    try:
                                        parsed = json.loads(json_str)
                                        if isinstance(parsed, dict) and 'Value' in parsed:
                                            # Valid JSON with Value field
                                            json_objects.append(parsed)
                                    except:
                                        pass
                                    break
                            i += 1
                    i += 1
                
                # Return the last valid JSON object (most likely the actual response)
                if json_objects:
                    return json_objects[-1]
                else:
                    return None
            else:
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
