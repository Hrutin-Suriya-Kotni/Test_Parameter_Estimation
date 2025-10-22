#!/usr/bin/env python3
"""
Token Analysis Script
Analyzes token counts for prompts and conversations using openchat-3.5-1210 tokenizer
"""

import sys
import json
import csv
from pathlib import Path
from typing import Dict, List
from transformers import AutoTokenizer

# Add parent directory to path to import prompts
sys.path.insert(0, str(Path(__file__).parent.parent))
from prompts import ASSESSMENT_PROMPTS

def initialize_tokenizer(model_name: str = "openchat/openchat-3.5-1210"):
    """Initialize the tokenizer"""
    print(f"Loading tokenizer: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    return tokenizer

def count_tokens(text: str, tokenizer) -> int:
    """Count tokens in text"""
    return len(tokenizer.encode(text))

def analyze_prompts(tokenizer) -> Dict:
    """Analyze all prompt templates"""
    results = {}
    
    print(f"  Found {len(ASSESSMENT_PROMPTS)} prompt templates")
    
    for prompt_name, prompt_text in ASSESSMENT_PROMPTS.items():
        print(f"  Tokenizing '{prompt_name}'... ", end='', flush=True)
        token_count = count_tokens(prompt_text, tokenizer)
        print(f"[{token_count} tokens]")
        
        results[prompt_name] = {
            'token_count': token_count,
            'char_count': len(prompt_text),
            'line_count': len(prompt_text.split('\n'))
        }
    
    print(f"  ✓ Completed all prompts")
    return results

def analyze_type1_conversations(tokenizer, csv_path: Path) -> Dict:
    """Analyze Type1 conversations from CSV"""
    print(f"Analyzing Type1 conversations: {csv_path}")
    
    results = {
        'total_conversations': 0,
        'conversations': [],
        'total_tokens': 0,
        'min_tokens': float('inf'),
        'max_tokens': 0
    }
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, 1):
            conv_id = row.get('conversation_id', 'unknown')
            paragraph = row.get('transcript', row.get('overall_paragraph', ''))
            
            print(f"  Processing conversation {idx}: {conv_id[:8]}... ", end='', flush=True)
            token_count = count_tokens(paragraph, tokenizer)
            print(f"[{token_count} tokens]")
            
            results['conversations'].append({
                'conversation_id': conv_id,
                'token_count': token_count,
                'char_count': len(paragraph)
            })
            
            results['total_tokens'] += token_count
            results['min_tokens'] = min(results['min_tokens'], token_count)
            results['max_tokens'] = max(results['max_tokens'], token_count)
            results['total_conversations'] += 1
    
    results['avg_tokens'] = results['total_tokens'] / results['total_conversations'] if results['total_conversations'] > 0 else 0
    print(f"  ✓ Completed {results['total_conversations']} conversations")
    
    return results

def analyze_type2b_conversations(tokenizer, csv_path: Path) -> Dict:
    """Analyze Type2b conversations from CSV"""
    print(f"Analyzing Type2b conversations: {csv_path}")
    
    results = {
        'total_conversations': 0,
        'conversations': [],
        'total_tokens': 0,
        'min_tokens': float('inf'),
        'max_tokens': 0
    }
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, 1):
            conv_id = row.get('conversation_id', 'unknown')
            paragraph = row.get('transcript', row.get('labeled_paragraph', ''))
            
            print(f"  Processing conversation {idx}: {conv_id[:8]}... ", end='', flush=True)
            token_count = count_tokens(paragraph, tokenizer)
            print(f"[{token_count} tokens]")
            
            results['conversations'].append({
                'conversation_id': conv_id,
                'token_count': token_count,
                'char_count': len(paragraph)
            })
            
            results['total_tokens'] += token_count
            results['min_tokens'] = min(results['min_tokens'], token_count)
            results['max_tokens'] = max(results['max_tokens'], token_count)
            results['total_conversations'] += 1
    
    results['avg_tokens'] = results['total_tokens'] / results['total_conversations'] if results['total_conversations'] > 0 else 0
    print(f"  ✓ Completed {results['total_conversations']} conversations")
    
    return results

def analyze_type2a_conversations(tokenizer, json_dir: Path) -> Dict:
    """Analyze Type2a conversations from JSON files"""
    print(f"Analyzing Type2a conversations: {json_dir}")
    
    results = {
        'total_conversations': 0,
        'conversations': [],
        'total_tokens': 0,
        'min_tokens': float('inf'),
        'max_tokens': 0
    }
    
    json_files = sorted(json_dir.glob('*.json'))
    print(f"  Found {len(json_files)} JSON files")
    
    for idx, json_file in enumerate(json_files, 1):
        print(f"  Processing {idx}/{len(json_files)}: {json_file.stem[:8]}... ", end='', flush=True)
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Tokenize the FULL JSON structure (as it would be sent to model)
            full_json_text = json.dumps(data, ensure_ascii=False)
            
            token_count = count_tokens(full_json_text, tokenizer)
            print(f"[{token_count} tokens]")
            
            turns = data.get('turns', [])
            results['conversations'].append({
                'conversation_id': json_file.stem,
                'token_count': token_count,
                'char_count': len(full_json_text),
                'num_turns': len(turns)
            })
            
            results['total_tokens'] += token_count
            results['min_tokens'] = min(results['min_tokens'], token_count)
            results['max_tokens'] = max(results['max_tokens'], token_count)
            results['total_conversations'] += 1
    
    results['avg_tokens'] = results['total_tokens'] / results['total_conversations'] if results['total_conversations'] > 0 else 0
    print(f"  ✓ Completed {results['total_conversations']} conversations")
    
    return results

def main():
    """Main analysis function"""
    base_dir = Path(__file__).parent.parent
    
    # Initialize tokenizer
    tokenizer = initialize_tokenizer()
    
    print("\n" + "="*80)
    print("TOKEN ANALYSIS - OpenChat-3.5-1210 Tokenizer")
    print("="*80 + "\n")
    
    # Analyze prompts
    print("1. Analyzing Prompt Templates...")
    prompt_results = analyze_prompts(tokenizer)
    
    # Analyze conversations
    print("\n2. Analyzing Type1 Conversations...")
    type1_results = analyze_type1_conversations(
        tokenizer, 
        base_dir / 'data' / 'type1_overall_paragraph.csv'
    )
    
    print("\n3. Analyzing Type2b Conversations...")
    type2b_results = analyze_type2b_conversations(
        tokenizer,
        base_dir / 'data' / 'type2b_labeled_paragraph.csv'
    )
    
    print("\n4. Analyzing Type2a Conversations...")
    type2a_results = analyze_type2a_conversations(
        tokenizer,
        base_dir / 'data' / 'type2a_json'
    )
    
    # Save results
    all_results = {
        'tokenizer': 'openchat/openchat-3.5-1210',
        'prompts': prompt_results,
        'type1': type1_results,
        'type2a': type2a_results,
        'type2b': type2b_results
    }
    
    output_file = Path(__file__).parent / 'token_analysis_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Results saved to: {output_file}")
    
    # Print summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\nPrompt Templates ({len(prompt_results)}):")
    for name, stats in prompt_results.items():
        print(f"  - {name:20s}: {stats['token_count']:,} tokens")
    
    print(f"\nType1 Conversations:")
    print(f"  - Total: {type1_results['total_conversations']}")
    print(f"  - Avg tokens: {type1_results['avg_tokens']:.1f}")
    print(f"  - Range: {type1_results['min_tokens']:,} - {type1_results['max_tokens']:,}")
    
    print(f"\nType2a Conversations:")
    print(f"  - Total: {type2a_results['total_conversations']}")
    print(f"  - Avg tokens: {type2a_results['avg_tokens']:.1f}")
    print(f"  - Range: {type2a_results['min_tokens']:,} - {type2a_results['max_tokens']:,}")
    
    print(f"\nType2b Conversations:")
    print(f"  - Total: {type2b_results['total_conversations']}")
    print(f"  - Avg tokens: {type2b_results['avg_tokens']:.1f}")
    print(f"  - Range: {type2b_results['min_tokens']:,} - {type2b_results['max_tokens']:,}")
    
    return all_results

if __name__ == "__main__":
    main()

