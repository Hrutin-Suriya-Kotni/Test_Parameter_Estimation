#!/usr/bin/env python3
"""
Mistral v0.2 model test runner for conversation analysis
Tests all conversation types using mistralai/Mistral-7B-Instruct-v0.2 via Hugging Face Inference providers
"""

import os
import sys
from datetime import datetime
from typing import Dict

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_clients.mistral_v0_2_client import MistralV02Client
from test_runners.base_test_runner import BaseTestRunner
from prompts import ASSESSMENT_PROMPTS


class MistralV02TestRunner:
    """Test runner for Mistral v0.2 (HF provider)"""

    def __init__(self):
        self.model_client = MistralV02Client()
        self.test_runners = {}

        for test_type in ASSESSMENT_PROMPTS.keys():
            self.test_runners[test_type] = BaseTestRunner(self.model_client, test_type)

    def test_single_type(self, test_type: str, max_conversations: int = None) -> str:
        """Test a single conversation type"""
        if test_type not in self.test_runners:
            print(f"❌ Unknown test type: {test_type}")
            return None

        print(f"🧪 Running {test_type} test with Mistral v0.2...")
        prompt = ASSESSMENT_PROMPTS[test_type]
        return self.test_runners[test_type].run_full_test(prompt, max_conversations)

    def test_all_types(self, max_conversations: int = None) -> Dict[str, str]:
        """Test all conversation types"""
        print("🚀 Running ALL conversation tests with Mistral v0.2")
        print("=" * 60)

        results = {}

        for test_type in ASSESSMENT_PROMPTS.keys():
            print(f"\n{'='*50}")
            print(f"Testing {test_type.upper()} with Mistral v0.2")
            print(f"{'='*50}")

            try:
                filepath = self.test_single_type(test_type, max_conversations)
                if filepath:
                    results[test_type] = filepath
                    print(f"✅ {test_type} test completed successfully!")
                else:
                    print(f"❌ {test_type} test failed!")

            except Exception as e:
                print(f"❌ {test_type} test failed with error: {str(e)}")
                results[test_type] = None

            import time

            time.sleep(3)

        return results

    def run_interactive(self):
        """Run interactive test selection"""
        print("🤖 Mistral v0.2 Model Test Runner (HF)")
        print("=" * 40)

        test_types = list(ASSESSMENT_PROMPTS.keys())

        while True:
            print("\nAvailable test types:")
            for i, test_type in enumerate(test_types, 1):
                print(f"  {i}. {test_type}")

            print("\nOptions:")
            print("  1. Run all tests")
            print("  2. Run specific test type")
            print("  3. Exit")

            try:
                choice = input("\nEnter your choice (1-3): ").strip()

                if choice == "1":
                    max_conv = input(
                        "Enter max conversations (or press Enter for all): "
                    ).strip()
                    max_conv = int(max_conv) if max_conv.isdigit() else None

                    start_time = datetime.now()
                    self.test_all_types(max_conv)
                    end_time = datetime.now()

                    print(f"\n{'='*60}")
                    print("🎯 ALL MISTRAL v0.2 TESTS COMPLETED!")
                    print(f"⏱️  Total time: {end_time - start_time}")
                    print("📁 Results saved in: results/mistral_v0_2/")
                    print(f"{'='*60}")
                    break

                elif choice == "2":
                    print("\nSelect test type:")
                    for i, test_type in enumerate(test_types, 1):
                        print(f"  {i}. {test_type}")

                    test_choice = input(
                        f"Enter test number (1-{len(test_types)}): "
                    ).strip()
                    try:
                        test_index = int(test_choice) - 1
                        if 0 <= test_index < len(test_types):
                            test_type = test_types[test_index]
                            max_conv = input(
                                "Enter max conversations (or press Enter for all): "
                            ).strip()
                            max_conv = int(max_conv) if max_conv.isdigit() else None

                            self.test_single_type(test_type, max_conv)
                        else:
                            print("Invalid test number!")
                    except ValueError:
                        print("Please enter a valid number!")

                elif choice == "3":
                    print("👋 Goodbye!")
                    break

                else:
                    print("Please enter a valid choice (1-3)")

            except KeyboardInterrupt:
                print("\n\n⚠️  Test interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}")


def main():
    runner = MistralV02TestRunner()
    runner.run_interactive()


if __name__ == "__main__":
    main()

