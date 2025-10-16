#!/usr/bin/env python3
"""
Run comprehensive BOOM BOOM tests
Server3 + Server5 on all data types and all guidelines
"""

import sys
from boom_boom_test import BoomBoomTestRunner
from prompts import ASSESSMENT_PROMPTS
import time

def main():
    print("="*70)
    print("🚀 COMPREHENSIVE BOOM BOOM TEST")
    print("="*70)
    print("\nConfiguration:")
    print("  Models: Server3, Server5")
    print("  Data Types: type1, type2a, type2b")
    print("  Parameters: ALL (Opening, Closing, Reassurance, Hold, Further Assistance)")
    print("  Conversations per type: 20")
    print("="*70)
    
    runner = BoomBoomTestRunner()
    
    # Models to test (only Server3 and Server5 for now)
    models_to_test = [
        'server3_base_openchat_mistral',
        'server5_base_mistral'
    ]
    
    # All data types
    data_types = ['type1', 'type2a', 'type2b']
    
    # All parameters/guidelines
    all_parameters = list(ASSESSMENT_PROMPTS.keys())
    
    max_conversations = 20
    
    total_tests = len(models_to_test) * len(data_types) * len(all_parameters)
    current_test = 0
    
    print(f"\n⚡ Total tests to run: {total_tests}")
    print("="*70)
    
    start_time = time.time()
    
    for model_name in models_to_test:
        for data_type in data_types:
            for parameter in all_parameters:
                current_test += 1
                
                print(f"\n{'='*70}")
                print(f"📊 Test {current_test}/{total_tests}")
                print(f"   Model: {model_name}")
                print(f"   Data: {data_type}")
                print(f"   Parameter: {parameter.replace('_', ' ').title()}")
                print(f"{'='*70}")
                
                try:
                    runner.test_model_on_data_type(
                        model_name=model_name,
                        data_type=data_type,
                        test_type=parameter,
                        max_conversations=max_conversations
                    )
                    print(f"✅ Test {current_test}/{total_tests} completed")
                except Exception as e:
                    print(f"❌ Test {current_test}/{total_tests} failed: {e}")
                
                # Small delay between tests
                time.sleep(2)
    
    end_time = time.time()
    total_minutes = (end_time - start_time) / 60
    
    print("\n" + "="*70)
    print("🎉 ALL TESTS COMPLETED!")
    print("="*70)
    print(f"Total time: {total_minutes:.1f} minutes")
    print(f"Tests completed: {current_test}/{total_tests}")
    print(f"\n📁 Results saved in: MISTRAL_BOOM_BOOM/")
    print("\nCheck results in:")
    for model in models_to_test:
        for dtype in data_types:
            print(f"  - MISTRAL_BOOM_BOOM/{dtype}/{model}/")

if __name__ == "__main__":
    main()


