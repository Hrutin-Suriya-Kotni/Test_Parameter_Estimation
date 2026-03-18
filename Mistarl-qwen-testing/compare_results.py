#!/usr/bin/env python3
"""
Compare RTX 4000 vs V100 Results
Calculate agreement metrics and consistency analysis
"""

import json
from pathlib import Path
from collections import defaultdict

def load_results():
    """Load both test results"""
    with open('results/openchat_test_results_20251022_185711.json') as f:
        rtx_data = json.load(f)
    
    with open('results/mistral_v100_test_results_20251022_235847.json') as f:
        v100_data = json.load(f)
    
    return rtx_data, v100_data

def create_lookup(results):
    """Create lookup: (conv_id, guideline, data_type) -> result"""
    lookup = {}
    for r in results:
        key = (r['conversation_id'], r['guideline'], r['data_type'])
        lookup[key] = r
    return lookup

def calculate_value_agreement(rtx_results, v100_results):
    """Calculate % agreement on Value (Met/Not Met)"""
    rtx_lookup = create_lookup(rtx_results)
    v100_lookup = create_lookup(v100_results)
    
    agreements = defaultdict(lambda: {'agree': 0, 'disagree': 0, 'both_parse_error': 0, 'one_parse_error': 0})
    
    for key in rtx_lookup:
        if key in v100_lookup:
            rtx_val = rtx_lookup[key].get('value')
            v100_val = v100_lookup[key].get('value')
            
            conv_id, guideline, dtype = key
            
            if rtx_val == 'Parse Error' and v100_val == 'Parse Error':
                agreements['overall']['both_parse_error'] += 1
                agreements[f'guideline_{guideline}']['both_parse_error'] += 1
                agreements[f'type_{dtype}']['both_parse_error'] += 1
            elif rtx_val == 'Parse Error' or v100_val == 'Parse Error':
                agreements['overall']['one_parse_error'] += 1
                agreements[f'guideline_{guideline}']['one_parse_error'] += 1
                agreements[f'type_{dtype}']['one_parse_error'] += 1
            elif rtx_val == v100_val:
                agreements['overall']['agree'] += 1
                agreements[f'guideline_{guideline}']['agree'] += 1
                agreements[f'type_{dtype}']['agree'] += 1
            else:
                agreements['overall']['disagree'] += 1
                agreements[f'guideline_{guideline}']['disagree'] += 1
                agreements[f'type_{dtype}']['disagree'] += 1
                
                # Track disagreement details
                if 'disagreements' not in agreements:
                    agreements['disagreements'] = []
                agreements['disagreements'].append({
                    'conv_id': conv_id,
                    'guideline': guideline,
                    'data_type': dtype,
                    'rtx_value': rtx_val,
                    'v100_value': v100_val
                })
    
    return dict(agreements)

def calculate_latency_comparison(rtx_results, v100_results):
    """Compare latencies for same conversations"""
    rtx_lookup = create_lookup(rtx_results)
    v100_lookup = create_lookup(v100_results)
    
    latency_diffs = []
    
    for key in rtx_lookup:
        if key in v100_lookup:
            rtx_lat = rtx_lookup[key].get('latency', 0)
            v100_lat = v100_lookup[key].get('latency', 0)
            
            if rtx_lat > 0 and v100_lat > 0:
                diff = rtx_lat - v100_lat
                ratio = rtx_lat / v100_lat
                latency_diffs.append({
                    'conv_id': key[0],
                    'guideline': key[1],
                    'data_type': key[2],
                    'rtx_latency': rtx_lat,
                    'v100_latency': v100_lat,
                    'difference': diff,
                    'ratio': ratio
                })
    
    return latency_diffs

def main():
    print("="*80)
    print("RTX 4000 vs V100 COMPARISON ANALYSIS")
    print("="*80)
    
    rtx_data, v100_data = load_results()
    
    # Value Agreement
    print("\n1. VALUE AGREEMENT ANALYSIS")
    print("-"*80)
    
    agreements = calculate_value_agreement(rtx_data['results'], v100_data['results'])
    
    overall = agreements['overall']
    total = sum([overall['agree'], overall['disagree'], overall['both_parse_error'], overall['one_parse_error']])
    
    print(f"\nOverall (1,110 test pairs):")
    print(f"  Agree (same Value):        {overall['agree']:4d} ({overall['agree']/total*100:.1f}%)")
    print(f"  Disagree (diff Value):     {overall['disagree']:4d} ({overall['disagree']/total*100:.1f}%)")
    print(f"  Both Parse Error:          {overall['both_parse_error']:4d} ({overall['both_parse_error']/total*100:.1f}%)")
    print(f"  One Parse Error:           {overall['one_parse_error']:4d} ({overall['one_parse_error']/total*100:.1f}%)")
    
    # Agreement by guideline
    print(f"\nAgreement by Guideline:")
    for guideline in ['opening', 'closing', 'reassurance', 'hold', 'further_assistance']:
        key = f'guideline_{guideline}'
        stats = agreements[key]
        total_g = sum([stats['agree'], stats['disagree'], stats['both_parse_error'], stats['one_parse_error']])
        agree_pct = stats['agree'] / total_g * 100
        print(f"  {guideline:20s}: {stats['agree']}/222 ({agree_pct:.1f}%) agree, {stats['disagree']} disagree")
    
    # Agreement by data type
    print(f"\nAgreement by Data Type:")
    for dtype in ['type1', 'type2a', 'type2b']:
        key = f'type_{dtype}'
        stats = agreements[key]
        total_t = sum([stats['agree'], stats['disagree'], stats['both_parse_error'], stats['one_parse_error']])
        agree_pct = stats['agree'] / total_t * 100
        print(f"  {dtype:10s}: {stats['agree']}/370 ({agree_pct:.1f}%) agree, {stats['disagree']} disagree")
    
    # Show disagreements
    if 'disagreements' in agreements and agreements['disagreements']:
        print(f"\nDisagreements (RTX ≠ V100):")
        print(f"  Total: {len(agreements['disagreements'])}")
        print(f"\n  Sample (first 10):")
        for i, dis in enumerate(agreements['disagreements'][:10], 1):
            print(f"    {i}. {dis['conv_id'][:12]} | {dis['guideline']:12s} | {dis['data_type']:6s} | RTX:{dis['rtx_value']:8s} vs V100:{dis['v100_value']:8s}")
    
    # Latency comparison
    print(f"\n{'='*80}")
    print("2. LATENCY COMPARISON")
    print("-"*80)
    
    latency_diffs = calculate_latency_comparison(rtx_data['results'], v100_data['results'])
    
    if latency_diffs:
        avg_rtx = sum(d['rtx_latency'] for d in latency_diffs) / len(latency_diffs)
        avg_v100 = sum(d['v100_latency'] for d in latency_diffs) / len(latency_diffs)
        avg_diff = sum(d['difference'] for d in latency_diffs) / len(latency_diffs)
        avg_ratio = sum(d['ratio'] for d in latency_diffs) / len(latency_diffs)
        
        print(f"\nAverage Latency:")
        print(f"  RTX 4000:  {avg_rtx:.2f}s")
        print(f"  V100:      {avg_v100:.2f}s")
        print(f"  Difference: {avg_diff:+.2f}s")
        print(f"  Speed Ratio: RTX is {avg_ratio:.2f}x the V100 speed")
        
        # Fastest/slowest
        fastest_rtx = min(latency_diffs, key=lambda x: x['ratio'])
        slowest_rtx = max(latency_diffs, key=lambda x: x['ratio'])
        
        print(f"\nRTX performed best on:")
        print(f"  {fastest_rtx['conv_id'][:12]} | RTX:{fastest_rtx['rtx_latency']:.2f}s vs V100:{fastest_rtx['v100_latency']:.2f}s ({fastest_rtx['ratio']:.2f}x)")
        
        print(f"\nRTX performed worst on:")
        print(f"  {slowest_rtx['conv_id'][:12]} | RTX:{slowest_rtx['rtx_latency']:.2f}s vs V100:{slowest_rtx['v100_latency']:.2f}s ({slowest_rtx['ratio']:.2f}x)")
    
    # Save detailed comparison
    output = {
        'summary': {
            'total_comparisons': total,
            'value_agreement_rate': overall['agree'] / total,
            'disagreement_rate': overall['disagree'] / total,
            'parse_error_rate': (overall['both_parse_error'] + overall['one_parse_error']) / total
        },
        'agreements': agreements,
        'latency_comparison': {
            'average_rtx': avg_rtx if latency_diffs else 0,
            'average_v100': avg_v100 if latency_diffs else 0,
            'average_difference': avg_diff if latency_diffs else 0,
            'speed_ratio': avg_ratio if latency_diffs else 0
        }
    }
    
    output_file = Path('results/rtx_v100_comparison.json')
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Detailed comparison saved to: {output_file}")

if __name__ == "__main__":
    main()

