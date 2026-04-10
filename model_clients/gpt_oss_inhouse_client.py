#!/usr/bin/env python3
"""
In-house vLLM model client for conversation analysis.
Uses OpenAI-compatible /v1/chat/completions endpoint.
Configured for openai/gpt-oss-20b.
"""

import sys
import os
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_clients.base_client import BaseModelClient


class InhouseVLLMClient(BaseModelClient):
    """Client for in-house vLLM models (OpenAI-compatible)."""

    def __init__(self):
        super().__init__("vLLM-inhouse")

        # 🔥 Hardcoded config (no .env)
        self.base_url = "http://192.168.30.251:9000/v1"
        self.model = "openai/gpt-oss-20b"
        self.api_key = "inhouse-no-key"  # replace if your server uses auth

        self.client = None

    def initialize(self) -> bool:
        """Initialize the vLLM client."""
        try:
            from openai import OpenAI

            self.client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key
            )

            self.initialized = True
            return True

        except Exception as e:
            print(f"vLLM client initialization failed: {e}")
            self.initialized = False
            return False

    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        """Analyze conversation using vLLM chat completions."""
        try:
            if not self.client:
                if not self.initialize():
                    return "Error: vLLM client initialization failed"

            enhanced_prompt = (
                "You are a helpful assistant that ALWAYS responds with ONLY valid JSON "
                "in the exact format requested. Never add explanatory text before or after the JSON. "
                "Use double quotes and ensure the JSON is properly formatted.\n\n"
                f"{prompt}\n\n"
                "CRITICAL: You must respond with ONLY a valid JSON object. No additional text before or after.\n\n"
                f"Transcript:\n{transcript}"
            )

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": enhanced_prompt}
                ],
                temperature=0.2,
            )

            return completion.choices[0].message.content or ""

        except Exception as e:
            return f"Error: {str(e)}"

    def test_connection(self) -> bool:
        """Test if the vLLM server is accessible."""
        try:
            response = self.analyze_conversation(
                "Reply with the single word: OK",
                "Short test transcript.",
            )

            if str(response).strip().startswith("Error:"):
                print(f"vLLM test_connection error: {response}")

                if "401" in str(response) or "Unauthorized" in str(response):
                    print(
                        "💡 Your server requires an API key. "
                        "Update self.api_key in this file."
                    )

                return False

            return True

        except Exception as e:
            print(f"vLLM connection test failed: {e}")
            return False

    def get_model_info(self) -> Dict[str, Any]:
        """Return client info."""
        base_info = super().get_model_info()

        base_info.update({
            "api_type": "vLLM OpenAI-compatible (in-house)",
            "base_url": self.base_url,
            "model": self.model,
        })

        return base_info