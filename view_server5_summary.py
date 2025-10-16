#!/usr/bin/env python3
"""
Quick summary viewer for Server 5 clean results
"""

import pandas as pd
import os

def view_summary():
    """View summary of Server 5 results from clean structure"""
    
    base_dir = "MISTRAL_BOOM_BOOM/server5_base_mistral"
    
    print("="*80)
    print("SERVER 5 BASE MISTRAL - RESULTS SUMMARY")
    print("="*80)
    print()
    
    data_types = ['type1', 'type2a', 'type2b']
    test_types = ['opening', 'closing', 'reassurance', 'hold', 'further_assistance']
    
    overall = {
        'total_conversations': 0,
        'successful': 0,
        'met': 0,
        'not_met': 0,
        'latencies': []
    }
    
    for data_type in data_types:
        print(f"\n{'─'*80}")
        print(f"📂 {data_type.upper()}")
        print(f"{'─'*80}")
        
        for test_type in test_types:
            csv_file = os.path.join(base_dir, data_type, f"{test_type}_results.csv")
            
            if os.path.exists(csv_file):
                df = pd.read_csv(csv_file)
                
                total = len(df)
                successful = df['success'].sum()
                success_rate = (successful / total * 100) if total > 0 else 0
                
                successful_df = df[df['success'] == True]
                met = (successful_df['result_value'] == 'Met').sum()
                not_met = (successful_df['result_value'] == 'Not Met').sum()
                
                latencies = df[df['success'] == True]['total_latency']
                avg_latency = latencies.mean() if len(latencies) > 0 else 0
                
                # Update overall stats
                overall['total_conversations'] += total
                overall['successful'] += successful
                overall['met'] += met
                overall['not_met'] += not_met
                overall['latencies'].extend(latencies.tolist())
                
                # Determine emoji based on success rate
                emoji = "🟢" if success_rate >= 90 else "🟡" if success_rate >= 75 else "🔴"
                
                print(f"{emoji} {test_type.replace('_', ' ').title():20} | "
                      f"Success: {successful:2}/{total} ({success_rate:5.1f}%) | "
                      f"Met: {met:2} | Not Met: {not_met:2} | "
                      f"Latency: {avg_latency:5.2f}s")
    
    # Overall summary
    print(f"\n{'='*80}")
    print("OVERALL SUMMARY")
    print(f"{'='*80}")
    
    total_success_rate = (overall['successful'] / overall['total_conversations'] * 100)
    avg_overall_latency = sum(overall['latencies']) / len(overall['latencies']) if overall['latencies'] else 0
    
    print(f"Total Conversations: {overall['total_conversations']}")
    print(f"Success Rate: {overall['successful']}/{overall['total_conversations']} ({total_success_rate:.1f}%)")
    print(f"Met: {overall['met']} ({overall['met']/overall['successful']*100:.1f}%)")
    print(f"Not Met: {overall['not_met']} ({overall['not_met']/overall['successful']*100:.1f}%)")
    print(f"Average Latency: {avg_overall_latency:.2f}s")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    view_summary()

