#!/usr/bin/env python3
"""
Semantic Similarity Comparison between RTX and V100 Evidence
Uses TF-IDF and Cosine Similarity
"""

import json
import re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def load_results():
    """Load both test results"""
    base_dir = Path(__file__).parent
    
    with open(base_dir / 'results/openchat_test_results_20251022_185711.json') as f:
        rtx_data = json.load(f)
    
    with open(base_dir / 'results/mistral_v100_test_results_20251022_235847.json') as f:
        v100_data = json.load(f)
    
    return rtx_data, v100_data

def extract_evidence(response):
    """Extract Evidence field from response"""
    if not response:
        return ""
    
    # Try to parse JSON and extract Evidence
    try:
        # Find JSON in response
        start_idx = response.find('{')
        end_idx = response.rfind('}') + 1
        
        if start_idx != -1 and end_idx > start_idx:
            json_str = response[start_idx:end_idx]
            parsed = json.loads(json_str)
            evidence = parsed.get('Evidence', parsed.get('evidence', ''))
            
            # Handle if evidence is a list or dict
            if isinstance(evidence, list):
                evidence = ' '.join(str(e) for e in evidence)
            elif isinstance(evidence, dict):
                evidence = str(evidence)
            
            return str(evidence)
    except:
        pass
    
    # Fallback: try to extract text after "Evidence"
    match = re.search(r'"Evidence"\s*:\s*"([^"]*)"', response, re.DOTALL)
    if match:
        return match.group(1)
    
    return response  # Return full response if can't extract

def create_lookup(results):
    """Create lookup: (conv_id, guideline, data_type) -> result"""
    lookup = {}
    for r in results:
        key = (r['conversation_id'], r['guideline'], r['data_type'])
        lookup[key] = r
    return lookup

def calculate_cosine_similarities(rtx_results, v100_results):
    """Calculate cosine similarity for Evidence texts"""
    rtx_lookup = create_lookup(rtx_results)
    v100_lookup = create_lookup(v100_results)
    
    comparisons = []
    
    for key in rtx_lookup:
        if key in v100_lookup:
            rtx_r = rtx_lookup[key]
            v100_r = v100_lookup[key]
            
            # Skip if either has parse error or failed status
            if rtx_r.get('status') != 'success' or v100_r.get('status') != 'success':
                continue
            
            # Skip if either has Parse Error as value
            if rtx_r.get('value') == 'Parse Error' or v100_r.get('value') == 'Parse Error':
                continue
            
            rtx_evidence = extract_evidence(rtx_r.get('response', ''))
            v100_evidence = extract_evidence(v100_r.get('response', ''))
            
            # Skip empty evidence
            if not rtx_evidence or not v100_evidence:
                continue
            
            # Calculate TF-IDF cosine similarity
            vectorizer = TfidfVectorizer()
            try:
                tfidf_matrix = vectorizer.fit_transform([rtx_evidence, v100_evidence])
                similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                
                comparisons.append({
                    'conv_id': key[0],
                    'guideline': key[1],
                    'data_type': key[2],
                    'rtx_value': rtx_r.get('value'),
                    'v100_value': v100_r.get('value'),
                    'cosine_similarity': similarity,
                    'rtx_evidence': rtx_evidence[:200],  # First 200 chars for reference
                    'v100_evidence': v100_evidence[:200],
                    'value_match': rtx_r.get('value') == v100_r.get('value')
                })
            except:
                # Skip if vectorization fails
                pass
    
    return comparisons

def analyze_similarities(comparisons):
    """Analyze similarity scores"""
    print("="*80)
    print("SEMANTIC SIMILARITY ANALYSIS (Cosine Similarity)")
    print("="*80)
    
    if not comparisons:
        print("No valid comparisons found!")
        return
    
    scores = [c['cosine_similarity'] for c in comparisons]
    
    print(f"\nTotal Evidence Pairs Compared: {len(comparisons)}")
    print(f"\nCosine Similarity Statistics:")
    print(f"  Mean:   {np.mean(scores):.4f}")
    print(f"  Median: {np.median(scores):.4f}")
    print(f"  Std Dev: {np.std(scores):.4f}")
    print(f"  Min:    {np.min(scores):.4f}")
    print(f"  Max:    {np.max(scores):.4f}")
    
    # Distribution
    print(f"\nSimilarity Distribution:")
    print(f"  >0.9 (Very High):   {sum(1 for s in scores if s > 0.9)} ({sum(1 for s in scores if s > 0.9)/len(scores)*100:.1f}%)")
    print(f"  0.7-0.9 (High):     {sum(1 for s in scores if 0.7 <= s <= 0.9)} ({sum(1 for s in scores if 0.7 <= s <= 0.9)/len(scores)*100:.1f}%)")
    print(f"  0.5-0.7 (Moderate): {sum(1 for s in scores if 0.5 <= s < 0.7)} ({sum(1 for s in scores if 0.5 <= s < 0.7)/len(scores)*100:.1f}%)")
    print(f"  <0.5 (Low):         {sum(1 for s in scores if s < 0.5)} ({sum(1 for s in scores if s < 0.5)/len(scores)*100:.1f}%)")
    
    # By guideline
    print(f"\nAverage Similarity by Guideline:")
    for guideline in ['opening', 'closing', 'reassurance', 'hold', 'further_assistance']:
        guideline_scores = [c['cosine_similarity'] for c in comparisons if c['guideline'] == guideline]
        if guideline_scores:
            print(f"  {guideline:20s}: {np.mean(guideline_scores):.4f} (n={len(guideline_scores)})")
    
    # By data type
    print(f"\nAverage Similarity by Data Type:")
    for dtype in ['type1', 'type2a', 'type2b']:
        type_scores = [c['cosine_similarity'] for c in comparisons if c['data_type'] == dtype]
        if type_scores:
            print(f"  {dtype:10s}: {np.mean(type_scores):.4f} (n={len(type_scores)})")
    
    # Value match correlation
    print(f"\nSimilarity when Values Match vs Don't Match:")
    match_scores = [c['cosine_similarity'] for c in comparisons if c['value_match']]
    nomatch_scores = [c['cosine_similarity'] for c in comparisons if not c['value_match']]
    
    if match_scores:
        print(f"  Same Value (Met/Not Met agree): {np.mean(match_scores):.4f} (n={len(match_scores)})")
    if nomatch_scores:
        print(f"  Different Value (disagree):     {np.mean(nomatch_scores):.4f} (n={len(nomatch_scores)})")
    
    # Lowest similarities (potential issues)
    print(f"\nLowest Similarity Pairs (Top 10):")
    sorted_comps = sorted(comparisons, key=lambda x: x['cosine_similarity'])
    for i, comp in enumerate(sorted_comps[:10], 1):
        print(f"  {i}. {comp['conv_id'][:12]} | {comp['guideline']:12s} | {comp['data_type']:6s} | Score:{comp['cosine_similarity']:.3f} | RTX:{comp['rtx_value']:8s} V100:{comp['v100_value']:8s}")
    
    # Highest similarities
    print(f"\nHighest Similarity Pairs (Top 10):")
    for i, comp in enumerate(sorted_comps[-10:][::-1], 1):
        print(f"  {i}. {comp['conv_id'][:12]} | {comp['guideline']:12s} | {comp['data_type']:6s} | Score:{comp['cosine_similarity']:.3f} | RTX:{comp['rtx_value']:8s} V100:{comp['v100_value']:8s}")
    
    return comparisons

def main():
    print("Loading results...")
    rtx_data, v100_data = load_results()
    
    print("Calculating cosine similarities...")
    comparisons = calculate_cosine_similarities(rtx_data['results'], v100_data['results'])
    
    analyze_similarities(comparisons)
    
    # Save results
    output_file = Path(__file__).parent / 'results/semantic_similarity_analysis.json'
    with open(output_file, 'w') as f:
        json.dump(comparisons, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Detailed similarity scores saved to: {output_file}")

if __name__ == "__main__":
    main()

