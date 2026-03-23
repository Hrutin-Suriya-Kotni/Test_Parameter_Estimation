#!/usr/bin/env python3
"""
Gemma model client for conversation analysis
Uses NVIDIA NIM OpenAI-compatible chat.completions API
"""

import os
import sys
from typing import Dict, Any

from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_clients.base_client import BaseModelClient


class GemmaClient(BaseModelClient):
    """Client for communicating with Gemma via NVIDIA NIM"""

    def __init__(self):
        super().__init__("Gemma")
        # NVIDIA model ids are case-sensitive; use lowercase.
        self.model = os.getenv("NVIDIA_GEMMA_MODEL", "google/gemma-2-9b-it")
        self.base_url = "https://integrate.api.nvidia.com/v1"
        self.api_key_env = "NVIDIA_API_KEY"
        self.client = None

    def initialize(self) -> bool:
        """Initialize the Gemma client"""
        try:
            load_dotenv()

            api_key = os.getenv(self.api_key_env)
            if not api_key:
                raise ValueError(
                    f"{self.api_key_env} not found in environment. "
                    f"Please add it to your .env file."
                )

            from openai import OpenAI

            self.client = OpenAI(base_url=self.base_url, api_key=api_key)
            # Don't call test_connection here to avoid extra requests.
            self.initialized = True
            return True

        except Exception as e:
            print(f"Gemma client initialization failed: {e}")
            self.initialized = False
            return False

    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        """Analyze conversation using Gemma via NVIDIA NIM"""
        try:
            if not self.client:
                if not self.initialize():
                    return "Error: Gemma client initialization failed"

            # NOTE: Some NVIDIA-hosted Gemma chat models reject the "system" role.
            # Put formatting constraints into the user message instead.
            enhanced_prompt = f"""You are a helpful assistant that ALWAYS responds with ONLY valid JSON in the exact format requested.
Never add explanatory text before or after the JSON. Use double quotes and ensure the JSON is properly formatted.

{prompt}

CRITICAL: You must respond with ONLY a valid JSON object. No additional text before or after.

Transcript:
{transcript}"""

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": enhanced_prompt},
                ],
                # No explicit max_tokens: let server-side defaults apply
            )

            return completion.choices[0].message.content

        except Exception as e:
            return f"Error: {str(e)}"

    def test_connection(self) -> bool:
        """Test if the Gemma model is accessible"""
        try:
            response = self.analyze_conversation(
                "Hello, this is a test message.", "Test transcript"
            )
            if str(response).startswith("Error:"):
                print(f"Gemma test_connection error detail: {response}")
                return False
            return True
        except Exception as e:
            print(f"Gemma connection test failed: {e}")
            return False

    def get_model_info(self) -> Dict[str, Any]:
        """Get Gemma model information"""
        base_info = super().get_model_info()
        base_info.update(
            {
                "api_type": "NVIDIA NIM OpenAI-compatible",
                "base_url": getattr(self, "base_url", None),
                "model": self.model,
                "api_key_env_var": self.api_key_env,
            }
        )
        return base_info

