#!/usr/bin/env python3
"""
Summary viewer for Server 3 results
"""

import pandas as pd
import os

def view_summary():
    """View summary of Server 3 results"""
    
    base_dir = "MISTRAL_BOOM_BOOM/server3_base_openchat_mistral"
    
    print("="*80)
    print("SERVER 3 OPENCHAT MISTRAL - RESULTS SUMMARY")
    print("="*80)
    print()
    
    data_types = ['type1', 'type2a', 'type2b']
    test_types = ['opening', 'closing', 'reassurance', 'hold', 'further_assistance']
    
    overall = {
        'total_conversations': 0,
        'successful': 0,
        'met': 0,
        'not_met': 0,
        'latencies': [],
        'tokens': []
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
                
                tokens = df[df['success'] == True]['total_tokens']
                avg_tokens = tokens.mean() if len(tokens) > 0 else 0
                
                # Update overall stats
                overall['total_conversations'] += total
                overall['successful'] += successful
                overall['met'] += met
                overall['not_met'] += not_met
                overall['latencies'].extend(latencies.tolist())
                overall['tokens'].extend(tokens.tolist())
                
                # Determine emoji based on success rate
                emoji = "🟢" if success_rate >= 90 else "🟡" if success_rate >= 60 else "🔴"
                
                print(f"{emoji} {test_type.replace('_', ' ').title():20} | "
                      f"Success: {successful:2}/{total} ({success_rate:5.1f}%) | "
                      f"Met: {met:2} | Not Met: {not_met:2} | "
                      f"Latency: {avg_latency:5.2f}s | "
                      f"Tokens: {avg_tokens:4.0f}")
    
    # Overall summary
    print(f"\n{'='*80}")
    print("OVERALL SUMMARY")
    print(f"{'='*80}")
    
    total_success_rate = (overall['successful'] / overall['total_conversations'] * 100)
    avg_overall_latency = sum(overall['latencies']) / len(overall['latencies']) if overall['latencies'] else 0
    avg_overall_tokens = sum(overall['tokens']) / len(overall['tokens']) if overall['tokens'] else 0
    
    print(f"Total Conversations: {overall['total_conversations']}")
    print(f"Success Rate: {overall['successful']}/{overall['total_conversations']} ({total_success_rate:.1f}%)")
    print(f"Failed: {overall['total_conversations'] - overall['successful']}")
    print(f"Met: {overall['met']} ({overall['met']/overall['successful']*100:.1f}%)")
    print(f"Not Met: {overall['not_met']} ({overall['not_met']/overall['successful']*100:.1f}%)")
    print(f"Average Latency: {avg_overall_latency:.2f}s")
    print(f"Average Tokens: {avg_overall_tokens:.0f}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    view_summary()


