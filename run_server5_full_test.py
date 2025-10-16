#!/usr/bin/env python3
"""
Run comprehensive Server 5 tests
Server5 on all data types and all guidelines (20 conversations each)
"""

import sys
from boom_boom_test import BoomBoomTestRunner
from prompts import ASSESSMENT_PROMPTS
import time

def main():
    print("\n" + "="*70)
    print("="*70)
    print("🚀 SERVER 5 COMPREHENSIVE TEST")
    print("="*70)
    print("="*70)
    
    runner = BoomBoomTestRunner()
    
    # Only Server 5
    model_name = 'server5_base_mistral'
    
    # All data types
    data_types = ['type1', 'type2a', 'type2b']
    
    # All parameters/guidelines
    all_parameters = list(ASSESSMENT_PROMPTS.keys())
    
    max_conversations = 20
    
    total_tests = len(data_types) * len(all_parameters)
    current_test = 0
    
    print("\n📋 TEST CONFIGURATION:")
    print("="*70)
    print(f"  🤖 Model: Server5 Base Mistral")
    print(f"  📂 Data Types: {', '.join(data_types)}")
    print(f"  🔍 Guidelines to test:")
    for i, param in enumerate(all_parameters, 1):
        print(f"      {i}. {param.replace('_', ' ').title()}")
    print(f"  💬 Conversations per test: {max_conversations}")
    print(f"  🎯 Total tests: {total_tests} ({len(data_types)} types × {len(all_parameters)} guidelines)")
    print(f"  ⏱️  Estimated duration: ~{total_tests * 2} minutes (approximate)")
    print("="*70)
    
    print("\n⚠️  IMPORTANT NOTES:")
    print("  • Each conversation will show detailed progress")
    print("  • Results are saved after each batch of 20 conversations")
    print("  • 1 second delay between conversations")
    print("  • 2 second delay between test batches")
    print("="*70)
    
    print("\n🚀 STARTING TESTS...")
    print("="*70)
    
    start_time = time.time()
    
    for data_type in data_types:
        print(f"\n{'#'*70}")
        print(f"{'#'*70}")
        print(f"###  DATA TYPE: {data_type.upper()}")
        print(f"{'#'*70}")
        print(f"{'#'*70}\n")
        
        for parameter in all_parameters:
            current_test += 1
            
            elapsed_time = time.time() - start_time
            avg_time_per_test = elapsed_time / current_test if current_test > 1 else 0
            estimated_remaining = avg_time_per_test * (total_tests - current_test)
            
            print(f"\n{'='*70}")
            print(f"{'='*70}")
            print(f"   🎯 TEST {current_test}/{total_tests}")
            print(f"{'='*70}")
            print(f"   📊 Model: Server5 Base Mistral")
            print(f"   📂 Data Type: {data_type}")
            print(f"   🔍 Parameter: {parameter.replace('_', ' ').title()}")
            print(f"   📈 Progress: {(current_test/total_tests)*100:.1f}%")
            if current_test > 1:
                print(f"   ⏱️  Elapsed: {elapsed_time/60:.1f} min")
                print(f"   ⏳ Est. Remaining: {estimated_remaining/60:.1f} min")
            print(f"{'='*70}")
            print(f"{'='*70}\n")
            
            try:
                test_start = time.time()
                runner.test_model_on_data_type(
                    model_name=model_name,
                    data_type=data_type,
                    test_type=parameter,
                    max_conversations=max_conversations
                )
                test_duration = time.time() - test_start
                
                print(f"\n{'='*70}")
                print(f"✅ TEST {current_test}/{total_tests} COMPLETED!")
                print(f"   Duration: {test_duration/60:.1f} minutes")
                print(f"{'='*70}\n")
                
            except Exception as e:
                print(f"\n{'='*70}")
                print(f"❌ TEST {current_test}/{total_tests} FAILED!")
                print(f"   Error: {e}")
                print(f"{'='*70}")
                import traceback
                traceback.print_exc()
            
            # Small delay between tests
            if current_test < total_tests:
                print(f"⏸️  Pausing 2 seconds before next test...\n")
                time.sleep(2)
    
    end_time = time.time()
    total_minutes = (end_time - start_time) / 60
    
    print("\n" + "="*70)
    print("="*70)
    print("🎉 ALL SERVER 5 TESTS COMPLETED!")
    print("="*70)
    print("="*70)
    
    print(f"\n📊 FINAL SUMMARY:")
    print("="*70)
    print(f"  ✅ Tests completed: {current_test}/{total_tests}")
    print(f"  ⏱️  Total time: {total_minutes:.1f} minutes ({total_minutes/60:.2f} hours)")
    print(f"  ⚡ Average time per test: {total_minutes/total_tests:.2f} minutes")
    print("="*70)
    
    print(f"\n📁 RESULTS LOCATION:")
    print("="*70)
    print(f"  Base directory: MISTRAL_BOOM_BOOM/")
    print(f"\n  Detailed results by data type:")
    for dtype in data_types:
        print(f"    📂 {dtype}:")
        for param in all_parameters:
            print(f"       └─ {param.replace('_', ' ').title()}")
        print(f"    Location: MISTRAL_BOOM_BOOM/{dtype}/server5_base_mistral/")
        print()
    print("="*70)
    
    print(f"\n🎯 TEST MATRIX COMPLETED:")
    print("="*70)
    print(f"  Data Types: {len(data_types)}")
    print(f"  Guidelines: {len(all_parameters)}")
    print(f"  Conversations per test: {max_conversations}")
    print(f"  Total conversations processed: {total_tests * max_conversations}")
    print("="*70)
    
    print("\n✨ ALL DONE! ✨\n")

if __name__ == "__main__":
    main()

