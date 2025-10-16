#!/usr/bin/env python3
"""
Summarize Server 5 test results
"""

import pandas as pd
import os
from pathlib import Path
import glob

def get_latest_results():
    """Get the latest result CSV for each test"""
    base_dir = "MISTRAL_BOOM_BOOM"
    
    results = {}
    
    data_types = ['type1', 'type2a', 'type2b']
    test_types = ['opening', 'closing', 'reassurance', 'hold', 'further_assistance']
    
    for data_type in data_types:
        for test_type in test_types:
            # Find all CSV files for this combination
            pattern = f"{base_dir}/{data_type}/server5_base_mistral/*/{test_type}_results.csv"
            files = sorted(glob.glob(pattern))
            
            if files:
                # Get the latest one (last in sorted order)
                latest_file = files[-1]
                key = f"{data_type}_{test_type}"
                results[key] = latest_file
    
    return results

def analyze_results():
    """Analyze all Server 5 results"""
    latest_results = get_latest_results()
    
    print("="*80)
    print("SERVER 5 (27.111.72.51:8000) - COMPREHENSIVE TEST RESULTS")
    print("="*80)
    print()
    
    overall_stats = {
        'total_tests': 0,
        'total_conversations': 0,
        'successful_calls': 0,
        'failed_calls': 0,
        'met_count': 0,
        'not_met_count': 0,
        'total_latency': 0
    }
    
    data_types = ['type1', 'type2a', 'type2b']
    test_types = ['opening', 'closing', 'reassurance', 'hold', 'further_assistance']
    
    detailed_results = []
    
    for data_type in data_types:
        print(f"\n{'#'*80}")
        print(f"DATA TYPE: {data_type.upper()}")
        print(f"{'#'*80}\n")
        
        for test_type in test_types:
            key = f"{data_type}_{test_type}"
            
            if key not in latest_results:
                print(f"  ⚠️  {test_type.replace('_', ' ').title()}: NO DATA")
                continue
            
            csv_file = latest_results[key]
            
            try:
                df = pd.read_csv(csv_file)
                
                total = len(df)
                successful = df['success'].sum()
                failed = total - successful
                
                # Count Met/Not Met from successful calls only
                successful_df = df[df['success'] == True]
                met = (successful_df['result_value'] == 'Met').sum()
                not_met = (successful_df['result_value'] == 'Not Met').sum()
                
                # Calculate latency stats
                latencies = df[df['success'] == True]['total_latency']
                avg_latency = latencies.mean() if len(latencies) > 0 else 0
                
                overall_stats['total_tests'] += 1
                overall_stats['total_conversations'] += total
                overall_stats['successful_calls'] += successful
                overall_stats['failed_calls'] += failed
                overall_stats['met_count'] += met
                overall_stats['not_met_count'] += not_met
                overall_stats['total_latency'] += latencies.sum() if len(latencies) > 0 else 0
                
                success_rate = (successful / total * 100) if total > 0 else 0
                
                print(f"  📊 {test_type.replace('_', ' ').title()}")
                print(f"     Total: {total} | Success: {successful}/{total} ({success_rate:.1f}%)")
                print(f"     Met: {met} | Not Met: {not_met} | Failed: {failed}")
                print(f"     Avg Latency: {avg_latency:.2f}s")
                print(f"     File: {os.path.basename(os.path.dirname(csv_file))}/{os.path.basename(csv_file)}")
                print()
                
                detailed_results.append({
                    'data_type': data_type,
                    'test_type': test_type,
                    'total': total,
                    'successful': successful,
                    'failed': failed,
                    'met': met,
                    'not_met': not_met,
                    'success_rate': success_rate,
                    'avg_latency': avg_latency
                })
                
            except Exception as e:
                print(f"  ❌ {test_type.replace('_', ' ').title()}: ERROR - {e}")
                print()
    
    # Print overall summary
    print("\n" + "="*80)
    print("OVERALL SUMMARY")
    print("="*80)
    print(f"Total Tests Completed: {overall_stats['total_tests']}/15")
    print(f"Total Conversations Processed: {overall_stats['total_conversations']}")
    print(f"Successful API Calls: {overall_stats['successful_calls']}/{overall_stats['total_conversations']} "
          f"({overall_stats['successful_calls']/overall_stats['total_conversations']*100:.1f}%)")
    print(f"Failed API Calls: {overall_stats['failed_calls']}")
    print()
    print(f"Results Distribution (from successful calls):")
    print(f"  Met: {overall_stats['met_count']}")
    print(f"  Not Met: {overall_stats['not_met_count']}")
    print()
    print(f"Average Latency: {overall_stats['total_latency']/overall_stats['successful_calls']:.2f}s")
    print("="*80)
    
    # Create summary by test type
    print("\n" + "="*80)
    print("SUMMARY BY GUIDELINE")
    print("="*80)
    
    for test_type in test_types:
        test_results = [r for r in detailed_results if r['test_type'] == test_type]
        if test_results:
            total_conv = sum(r['total'] for r in test_results)
            total_success = sum(r['successful'] for r in test_results)
            total_met = sum(r['met'] for r in test_results)
            total_not_met = sum(r['not_met'] for r in test_results)
            avg_success_rate = sum(r['success_rate'] for r in test_results) / len(test_results)
            
            print(f"\n{test_type.replace('_', ' ').title()}:")
            print(f"  Conversations: {total_conv}")
            print(f"  Success Rate: {avg_success_rate:.1f}%")
            print(f"  Met: {total_met} | Not Met: {total_not_met}")
    
    print("\n" + "="*80)
    
    return detailed_results

if __name__ == "__main__":
    analyze_results()

