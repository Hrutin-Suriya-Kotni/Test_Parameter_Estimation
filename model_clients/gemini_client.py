#!/usr/bin/env python3
"""
Gemini model client for conversation analysis
Uses Google's Gemini API
"""

import os
import sys
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_clients.base_client import BaseModelClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GeminiClient(BaseModelClient):
    """Client for communicating with Google Gemini API"""
    
    def __init__(self):
        super().__init__("Gemini")
        self.api_key = None
        self.model = None
        self.safety_settings = None
    
    def initialize(self) -> bool:
        """Initialize the Gemini client"""
        try:
            import google.generativeai as genai
            
            # Load environment variables
            load_dotenv()
            
            self.api_key = os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY not found in .env file. Please add it to your .env file.")
            
            genai.configure(api_key=self.api_key)
            # Use a stable, broadly available model name for v1beta generateContent
            self.model = genai.GenerativeModel("gemini-2.5-flash")
            
            # Safety settings to avoid blocking
            self.safety_settings = {
                'HATE': 'BLOCK_NONE',
                'HARASSMENT': 'BLOCK_NONE',
                'SEXUAL': 'BLOCK_NONE',
                'DANGEROUS': 'BLOCK_NONE'
            }
            
            # Test connection to verify initialization
            if self.test_connection():
                self.initialized = True
                return True
            else:
                self.initialized = False
                return False
                
        except Exception as e:
            print(f"Gemini client initialization failed: {e}")
            self.initialized = False
            return False
    
    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        """Analyze conversation using Gemini API"""
        try:
            # Enhanced prompt with JSON formatting instructions
            enhanced_prompt = f"""{prompt}

CRITICAL: You must respond with ONLY a valid JSON object. No additional text before or after.

Required JSON format:
{{"Value": "Met" or "Not Met", "Evidence": "detailed explanation"}}

Transcript:
{transcript}"""
            
            response = self.model.generate_content(
                enhanced_prompt,
                safety_settings=self.safety_settings,
                generation_config={
                    'temperature': 0.1,  # Low temperature for consistent results  # Reduced for faster inference
                }
            )
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def test_connection(self) -> bool:
        """Test if the Gemini API is accessible"""
        try:
            response = self.analyze_conversation("Hello, this is a test message.", "Test transcript")
            if response.startswith("Error:"):
                print(f"Gemini test_connection error detail: {response}")
                return False
            return True
        except Exception as e:
            print(f"Gemini connection test failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get Gemini model information"""
        base_info = super().get_model_info()
        base_info.update({
            'api_type': 'Google Gemini',
            'model': 'gemini-2.5-flash',
            'api_key_configured': bool(self.api_key)
        })
        return base_info
