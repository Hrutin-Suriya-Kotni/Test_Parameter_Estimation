#!/usr/bin/env python3
"""
Selective Qwen-inhouse test runner

Runs the Qwen inhouse model only for specific conversation numbers (1-based).
Default conversations: 12 and 18 (these were previously failing due to token limits).

Results are saved under results/qwen-inhouse/ as with other runners.
"""

import os
import sys
from typing import List, Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_clients.qwen_inhouse_client import QwenInhouseClient
from test_runners.base_test_runner import BaseTestRunner
from prompts import ASSESSMENT_PROMPTS
from data_loader import load_all_conversations


class QwenInhouseSelectedRunner:
    """Run Qwen-inhouse on a selected set of conversations."""

    def __init__(self, conversation_numbers: Optional[List[int]] = None):
        self.model_client = QwenInhouseClient()
        # default to conversations 12 and 18 (1-based indices)
        self.conversation_numbers = conversation_numbers or [12, 18]

    def _select_conversations(self, all_convs: List[dict]) -> List[dict]:
        selected = []
        total = len(all_convs)
        for num in self.conversation_numbers:
            idx = num - 1
            if 0 <= idx < total:
                selected.append(all_convs[idx])
            else:
                print(f"⚠️  Conversation number {num} is out of range (1..{total}) - skipping")
        return selected

    def run(self, test_types: Optional[List[str]] = None):
        """Run selected tests.

        Args:
            test_types: list of keys from ASSESSMENT_PROMPTS to run. If None, run all.
        """
        # Load all conversations
        all_convs = load_all_conversations()
        if not all_convs:
            print("❌ No conversations loaded. Aborting.")
            return

        selected_convs = self._select_conversations(all_convs)
        if not selected_convs:
            print("❌ No valid conversations selected. Aborting.")
            return

        # Decide which test types to run
        available = list(ASSESSMENT_PROMPTS.keys())
        if test_types:
            types_to_run = [t for t in test_types if t in available]
            invalid = [t for t in test_types if t not in available]
            if invalid:
                print(f"⚠️  Ignoring unknown test types: {invalid}")
        else:
            types_to_run = available

        print(f"🧾 Running Qwen-inhouse on conversations: {[c.get('id') for c in selected_convs]}")
        print(f"🔎 Test types: {types_to_run}")

        for test_type in types_to_run:
            print(f"\n{'='*60}\nRunning test type: {test_type}\n{'='*60}")
            prompt = ASSESSMENT_PROMPTS[test_type]
            runner = BaseTestRunner(self.model_client, test_type)

            # Ensure client connectivity before running
            if not runner.test_api_connectivity():
                print(f"❌ Model connectivity failed for {self.model_client.model_name}. Skipping {test_type}.")
                continue

            results = runner.run_tests(selected_convs, prompt)
            runner.save_results(results)
            runner.print_summary(results)


def parse_cli_args() -> (List[int], Optional[List[str]]):
    """Simple CLI parsing: provide conversation numbers and optional comma-separated test types.

    Usage examples:
      python test_qwen_inhouse_selected.py            # runs default [12,18] for all test types
      python test_qwen_inhouse_selected.py 12 18     # runs conv 12 and 18 for all test types
      python test_qwen_inhouse_selected.py --types closing,opening  # run specific types
    """
    import argparse

    parser = argparse.ArgumentParser(description="Run Qwen-inhouse for selected conversations")
    parser.add_argument(
        "numbers",
        nargs="*",
        type=int,
        help="Conversation numbers (1-based). If omitted, defaults to 12 and 18."
    )
    parser.add_argument(
        "--types",
        type=str,
        help="Comma-separated list of test types from prompts.py to run (default: all)"
    )

    args = parser.parse_args()
    nums = args.numbers if args.numbers else None
    types = [t.strip() for t in args.types.split(",")] if args.types else None
    return nums, types


def main():
    nums, types = parse_cli_args()
    runner = QwenInhouseSelectedRunner(conversation_numbers=nums)
    runner.run(test_types=types)


if __name__ == "__main__":
    main()
