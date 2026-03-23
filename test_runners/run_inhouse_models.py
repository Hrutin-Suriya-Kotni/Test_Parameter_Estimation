#!/usr/bin/env python3
"""
Run all test types sequentially for in-house models.
Models: gemma_inhouse, qwen_inhouse

Usage:
  python test_runners/run_inhouse_models.py
  python test_runners/run_inhouse_models.py --max-conversations 10
"""

import os
import sys
import argparse
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_runners.run_all_models import MasterTestRunner


def main():
    parser = argparse.ArgumentParser(description='Run all tests for in-house models')
    parser.add_argument('--max-conversations', type=int, default=None,
                        help='Limit conversations per test type (default: all)')
    args = parser.parse_args()

    print('🚀 In-house Models Runner')
    print('=' * 50)
    start = datetime.now()

    runner = MasterTestRunner()

    target_models = ['gemma_inhouse', 'qwen_inhouse']
    available = [m for m in target_models if m in runner.available_models]
    missing = [m for m in target_models if m not in runner.available_models]

    if missing:
        print(f'⚠️  Missing/unavailable in-house models: {missing}')
    if not available:
        print('❌ No in-house models available. Check .env/API endpoints.')
        return

    all_results = {}
    for model_name in available:
        print(f'
{'='*60}')
        print(f'Running ALL tests for: {model_name}')
        print(f'{'='*60}')
        all_results[model_name] = runner.test_single_model_all_types(
            model_name,
            max_conversations=args.max_conversations,
        )

    end = datetime.now()
    print('
' + '=' * 60)
    print('✅ In-house run complete')
    print(f'⏱️  Total time: {end - start}')
    print('📁 Results saved under results/gemma-inhouse and results/qwen-inhouse')
    print('=' * 60)


if __name__ == '__main__':
    main()
