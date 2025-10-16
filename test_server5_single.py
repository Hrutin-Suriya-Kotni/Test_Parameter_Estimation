#!/usr/bin/env python3
"""
Quick test of Server 5 with one conversation to debug response
"""

import sys
from boom_boom_test import BoomBoomTestRunner

def main():
    print("="*70)
    print("🔍 SERVER 5 DEBUG TEST - Single Conversation")
    print("="*70)
    
    runner = BoomBoomTestRunner()
    
    # Test just 1 conversation
    runner.test_model_on_data_type(
        model_name='server5_base_mistral',
        data_type='type1',
        test_type='opening',
        max_conversations=1
    )

if __name__ == "__main__":
    main()

