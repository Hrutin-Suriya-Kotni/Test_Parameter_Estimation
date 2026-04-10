#!/usr/bin/env python3
"""
Qwen-inhouse model client for conversation analysis.
Uses in-house vLLM server (FastAPI) at configurable base URL.
OpenAI-compatible /v1/chat/completions endpoint.
"""

import os
import sys
from typing import Dict, Any

from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_clients.base_client import BaseModelClient


class QwenInhouseClient(BaseModelClient):
    """Client for in-house vLLM Qwen (OpenAI-compatible chat completions)."""

    def __init__(self):
        super().__init__("Qwen-inhouse")
        load_dotenv()
        self.base_url = os.getenv("QWEN_INHOUSE_BASE_URL", "http://192.168.30.251:9000/v1")
        self.model = os.getenv("QWEN_INHOUSE_MODEL", "Qwen/Qwen2.5-7B-Instruct")
        self.api_key_env = "QWEN_INHOUSE_API_KEY"
        self.client = None

    def initialize(self) -> bool:
        """Initialize the Qwen-inhouse client."""
        try:
            load_dotenv()
            api_key = (os.getenv(self.api_key_env) or "").strip()
            if not api_key or api_key == "inhouse-no-key":
                api_key = "inhouse-no-key"
            from openai import OpenAI
            self.client = OpenAI(base_url=self.base_url, api_key=api_key)
            self.initialized = True
            return True
        except Exception as e:
            print(f"Qwen-inhouse client initialization failed: {e}")
            self.initialized = False
            return False

    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        """Analyze conversation using in-house vLLM chat completions."""
        try:
            if not self.client:
                if not self.initialize():
                    return "Error: Qwen-inhouse client initialization failed"

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
                messages=[{"role": "user", "content": enhanced_prompt}],
            )
            return completion.choices[0].message.content or ""
        except Exception as e:
            return f"Error: {str(e)}"

    def test_connection(self) -> bool:
        """Test if the in-house vLLM server is accessible."""
        try:
            response = self.analyze_conversation(
                "Reply with the single word: OK",
                "Short test transcript.",
            )
            if str(response).strip().startswith("Error:"):
                print(f"Qwen-inhouse test_connection error: {response}")
                if "401" in str(response) or "Unauthorized" in str(response):
                    print("   💡 Replace QWEN_INHOUSE_API_KEY in .env with the real token your vLLM server was started with (--api-key). 'inhouse-no-key' is only a placeholder.")
                return False
            return True
        except Exception as e:
            print(f"Qwen-inhouse connection test failed: {e}")
            return False

    def get_model_info(self) -> Dict[str, Any]:
        """Return client info."""
        base_info = super().get_model_info()
        base_info.update({
            "api_type": "vLLM OpenAI-compatible (in-house)",
            "base_url": self.base_url,
            "model": self.model or "(default)",
            "api_key_env_var": self.api_key_env,
        })
        return base_info
