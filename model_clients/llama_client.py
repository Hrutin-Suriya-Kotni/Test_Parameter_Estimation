#!/usr/bin/env python3
"""
Llama model client for conversation analysis
Uses NVIDIA NIM OpenAI-compatible chat.completions API
"""

import os
import sys
from typing import Dict, Any

from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_clients.base_client import BaseModelClient


class LlamaClient(BaseModelClient):
    """Client for communicating with meta/llama-3.1-8b-instruct via NVIDIA NIM"""

    def __init__(self):
        super().__init__("Llama")
        self.model = "meta/llama-3.1-8b-instruct"
        self.api_key_env = "NVIDIA_API_KEY"
        self.client = None

    def initialize(self) -> bool:
        """Initialize the Llama client"""
        try:
            # Load environment variables
            load_dotenv()

            api_key = os.getenv(self.api_key_env)
            if not api_key:
                raise ValueError(
                    f"{self.api_key_env} not found in environment. "
                    f"Please add it to your .env file."
                )

            from openai import OpenAI

            self.client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=api_key,
            )

            # Don't call test_connection here to avoid extra requests
            self.initialized = True
            return True

        except Exception as e:
            print(f"Llama client initialization failed: {e}")
            self.initialized = False
            return False

    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        """Analyze conversation using Llama via NVIDIA NIM"""
        try:
            if not self.client:
                # Lazy init if needed
                if not self.initialize():
                    return "Error: Llama client initialization failed"

            enhanced_prompt = f"""{prompt}

CRITICAL: You must respond with ONLY a valid JSON object. No additional text before or after.

Transcript:
{transcript}"""

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that ALWAYS responds with ONLY valid JSON in the exact format requested. Never add explanatory text before or after the JSON. Use double quotes and ensure the JSON is properly formatted.",
                    },
                    {
                        "role": "user",
                        "content": enhanced_prompt,
                    },
                ],
                # No explicit max_tokens: let server-side defaults apply
            )

            return completion.choices[0].message.content

        except Exception as e:
            return f"Error: {str(e)}"

    def test_connection(self) -> bool:
        """Test if the Llama model is accessible"""
        try:
            response = self.analyze_conversation(
                "Hello, this is a test message.", "Test transcript"
            )
            if str(response).startswith("Error:"):
                print(f"Llama test_connection error detail: {response}")
                return False
            return True
        except Exception as e:
            print(f"Llama connection test failed: {e}")
            return False

    def get_model_info(self) -> Dict[str, Any]:
        """Get Llama model information"""
        base_info = super().get_model_info()
        base_info.update(
            {
                "api_type": "NVIDIA NIM OpenAI-compatible",
                "base_url": "https://integrate.api.nvidia.com/v1",
                "model": self.model,
                "api_key_env_var": self.api_key_env,
            }
        )
        return base_info

