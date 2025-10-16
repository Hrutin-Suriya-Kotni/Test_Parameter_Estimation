#!/usr/bin/env python3
"""
Server 3 Full Test - All data types, all guidelines, 20 conversations each
Matches Server 5 test structure exactly
"""

import sys
sys.stdout = open(sys.stdout.fileno(), mode='w', buffering=1)  # Line buffering

import requests
import pandas as pd
import json
import time
import os
from datetime import datetime
from pathlib import Path

print("="*70, flush=True)
print("SERVER 3 OPENCHAT MISTRAL - COMPREHENSIVE TEST", flush=True)
print("="*70, flush=True)

# ============================================================================
# CONFIGURATION
# ============================================================================

API_URL = 'http://27.111.72.53:3333/v1/chat/completions'
MODEL = 'openchat/openchat-3.5-1210'
MAX_TOKENS = 512
TEMPERATURE = 0.1
TIMEOUT = 600  # 10 minutes per request for very long transcripts

# ============================================================================
# PROMPTS
# ============================================================================

PROMPTS = {
    'opening': """Analyze if the agent followed opening guidelines:
1. Greeted customer (Good morning/afternoon/evening/Hello)
2. Introduced themselves with their name
3. Confirmed or asked customer's name

Respond with ONLY valid JSON:
{"Value": "Met" or "Not Met", "Evidence": "brief explanation"}

Transcript:
""",
    'closing': """Analyze if the agent followed closing guidelines:
1. Asked if there's anything else to help with
2. Asked to share feedback
3. Closed with proper greetings
4. Asked customer to end call politely if needed

Respond with ONLY valid JSON:
{"Value": "Met" or "Not Met", "Evidence": "brief explanation"}

Transcript:
""",
    'reassurance': """Analyze if the agent provided reassurance statements similar to:
- "You can rest assured we are working on this"
- "I will get back to you as soon as possible"
- "We will handle this matter promptly"
- "Our support team is here for you"

Respond with ONLY valid JSON:
{"Value": "Met" or "Not Met", "Evidence": "brief explanation"}

Transcript:
""",
    'hold': """Analyze if the agent used hold statements like:
- "May I place your call on hold for X minutes?"
- "Thank you for being on hold"
- "Kya mein aapki call ko hold pe rak saktha"

Respond with ONLY valid JSON:
{"Value": "Met" or "Not Met", "Evidence": "brief explanation"}

Transcript:
""",
    'further_assistance': """Analyze if the agent asked for further assistance:
- "Is there anything else I may assist you with?"
- "Iske alawa koi aur sahayata"
- Similar statements

Respond with ONLY valid JSON:
{"Value": "Met" or "Not Met", "Evidence": "brief explanation"}

Transcript:
"""
}

# ============================================================================
# FUNCTIONS
# ============================================================================

def load_conversations(data_type, max_count=20):
    """Load conversations for a data type"""
    conversations = []
    
    if data_type == 'type1':
        csv_path = 'data/type1_overall_paragraph.csv'
        df = pd.read_csv(csv_path)
        for idx, row in df.head(max_count).iterrows():
            conversations.append({
                'id': row.get('conversation_id', f'type1_conv_{idx}'),
                'transcript': str(row['transcript']),
                'type': 'type1'
            })
    
    elif data_type == 'type2a':
        json_dir = 'data/type2a_json'
        json_files = sorted(Path(json_dir).glob('*.json'))[:max_count]
        for json_file in json_files:
            with open(json_file, 'r') as f:
                data = json.load(f)
                transcript = '\n'.join([f"{msg['speaker']}: {msg['text']}" for msg in data.get('messages', [])])
                conversations.append({
                    'id': json_file.stem,
                    'transcript': transcript,
                    'type': 'type2a'
                })
    
    elif data_type == 'type2b':
        csv_path = 'data/type2b_labeled_paragraph.csv'
        df = pd.read_csv(csv_path)
        for idx, row in df.head(max_count).iterrows():
            conversations.append({
                'id': row.get('conversation_id', f'type2b_conv_{idx}'),
                'transcript': str(row['transcript']),
                'type': 'type2b'
            })
    
    return conversations

def call_api(prompt, transcript):
    """Call Server 3 API with dynamic max_tokens"""
    full_prompt = prompt + transcript
    
    # Estimate tokens (rough: 1 token ≈ 4 chars)
    estimated_input_tokens = len(full_prompt) // 4
    
    # Model max context: 8192 tokens
    # Leave buffer: use 80% of available space
    max_context = 8192
    available_tokens = max_context - estimated_input_tokens
    
    # Use smaller of: requested tokens or 80% of available tokens
    dynamic_max_tokens = min(MAX_TOKENS, int(available_tokens * 0.8))
    
    # Ensure minimum of 50 tokens for response
    dynamic_max_tokens = max(50, dynamic_max_tokens)
    
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Respond with ONLY valid JSON."},
            {"role": "user", "content": full_prompt}
        ],
        "max_tokens": dynamic_max_tokens,
        "temperature": TEMPERATURE
    }
    
    start_time = time.time()
    
    try:
        response = requests.post(API_URL, json=data, timeout=TIMEOUT)
        latency = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            usage = result.get('usage', {})
            
            return {
                'success': True,
                'content': content,
                'latency': latency,
                'prompt_tokens': usage.get('prompt_tokens', 0),
                'completion_tokens': usage.get('completion_tokens', 0),
                'total_tokens': usage.get('total_tokens', 0),
                'max_tokens_used': dynamic_max_tokens
            }
        else:
            return {
                'success': False,
                'error': f"HTTP {response.status_code}",
                'latency': latency
            }
    except Exception as e:
        latency = time.time() - start_time
        return {
            'success': False,
            'error': str(e),
            'latency': latency
        }

def parse_json(text):
    """Extract and parse JSON from text"""
    json_objects = []
    i = 0
    while i < len(text):
        if text[i] == '{':
            depth = 0
            start = i
            while i < len(text):
                if text[i] == '{':
                    depth += 1
                elif text[i] == '}':
                    depth -= 1
                    if depth == 0:
                        try:
                            parsed = json.loads(text[start:i+1])
                            if isinstance(parsed, dict) and 'Value' in parsed:
                                json_objects.append(parsed)
                        except:
                            pass
                        break
                i += 1
        i += 1
    
    return json_objects[-1] if json_objects else None

def test_conversations(data_type, guideline, conversations):
    """Test all conversations for a guideline"""
    results = []
    prompt = PROMPTS[guideline]
    
    for i, conv in enumerate(conversations, 1):
        print(f"      [{i}/{len(conversations)}] {conv['id'][:30]}...", end=' ', flush=True)
        
        # Skip extremely long transcripts that cause Server 3 to hang
        # Server 3 max context is 8192 tokens, very long transcripts can cause issues
        if len(conv['transcript']) > 5000:
            result = {
                'conversation_id': conv['id'],
                'data_type': data_type,
                'parameter_tested': guideline.upper(),
                'success': False,
                'result_value': 'Skipped',
                'evidence': f'Transcript too long ({len(conv["transcript"])} chars) - would exceed context',
                'total_latency': 0
            }
            results.append(result)
            print(f"⏭️  Skipped (too long: {len(conv['transcript'])} chars)", flush=True)
            continue
        
        # Call API
        api_result = call_api(prompt, conv['transcript'])
        
        if api_result['success']:
            # Parse JSON
            parsed = parse_json(api_result['content'])
            
            if parsed:
                result = {
                    'conversation_id': conv['id'],
                    'data_type': data_type,
                    'parameter_tested': guideline.upper(),
                    'parameter_name': guideline.replace('_', ' ').title(),
                    'model_name': 'Server3_OpenChat_Mistral',
                    'timestamp': datetime.now().isoformat(),
                    'success': True,
                    'result_value': parsed.get('Value', 'Error'),
                    'evidence': parsed.get('Evidence', 'N/A'),
                    'transcript_length': len(conv['transcript']),
                    'response_length': len(api_result['content']),
                    'total_latency': api_result['latency'],
                    'prompt_tokens': api_result['prompt_tokens'],
                    'completion_tokens': api_result['completion_tokens'],
                    'total_tokens': api_result['total_tokens'],
                    'api_temperature': TEMPERATURE,
                    'api_max_tokens': api_result.get('max_tokens_used', MAX_TOKENS),
                    'api_endpoint': API_URL,
                    'model_version': MODEL
                }
                print(f"✅ {parsed.get('Value')} ({api_result['latency']:.2f}s)", flush=True)
            else:
                result = {
                    'conversation_id': conv['id'],
                    'data_type': data_type,
                    'parameter_tested': guideline.upper(),
                    'success': False,
                    'result_value': 'Parse Error',
                    'evidence': 'Failed to parse JSON',
                    'total_latency': api_result['latency']
                }
                print(f"❌ Parse failed", flush=True)
        else:
            result = {
                'conversation_id': conv['id'],
                'data_type': data_type,
                'parameter_tested': guideline.upper(),
                'success': False,
                'result_value': 'API Error',
                'evidence': api_result.get('error', 'Unknown error'),
                'total_latency': api_result.get('latency', 0)
            }
            print(f"❌ {api_result.get('error', 'Error')}", flush=True)
        
        results.append(result)
        time.sleep(1)  # Rate limiting
    
    return results

def save_results(results, data_type, guideline):
    """Save results to CSV"""
    output_dir = f'MISTRAL_BOOM_BOOM/server3_base_openchat_mistral/{data_type}'
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = f'{output_dir}/{guideline}_results.csv'
    df = pd.DataFrame(results)
    df.to_csv(filepath, index=False)
    
    return filepath

def print_summary(results):
    """Print test summary"""
    total = len(results)
    successful = sum(1 for r in results if r.get('success', False))
    met = sum(1 for r in results if r.get('result_value') == 'Met')
    not_met = sum(1 for r in results if r.get('result_value') == 'Not Met')
    
    latencies = [r.get('total_latency', 0) for r in results if r.get('success', False)]
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    
    tokens = [r.get('total_tokens', 0) for r in results if r.get('success', False)]
    avg_tokens = sum(tokens) / len(tokens) if tokens else 0
    
    print(f"\n  📊 SUMMARY:", flush=True)
    print(f"     Total: {total} | Success: {successful}/{total} ({successful/total*100:.1f}%)", flush=True)
    print(f"     Met: {met} | Not Met: {not_met}", flush=True)
    print(f"     Avg Latency: {avg_latency:.2f}s | Avg Tokens: {avg_tokens:.0f}", flush=True)

# ============================================================================
# MAIN
# ============================================================================

def main():
    print(f"\n  🤖 Model: {MODEL}", flush=True)
    print(f"  🌐 API: {API_URL}", flush=True)
    print(f"  📂 Data Types: type1, type2a, type2b", flush=True)
    print(f"  🔍 Guidelines: opening, closing, reassurance, hold, further_assistance", flush=True)
    print(f"  💬 Conversations per test: 20", flush=True)
    print("="*70, flush=True)
    
    data_types = ['type1', 'type2a', 'type2b']
    guidelines = ['opening', 'closing', 'reassurance', 'hold', 'further_assistance']
    
    total_tests = len(data_types) * len(guidelines)
    current_test = 0
    start_time = time.time()
    
    for data_type in data_types:
        print(f"\n{'#'*70}", flush=True)
        print(f"DATA TYPE: {data_type.upper()}", flush=True)
        print(f"{'#'*70}", flush=True)
        
        # Load conversations once per data type
        print(f"\n  📂 Loading {data_type} conversations...", flush=True)
        conversations = load_conversations(data_type, max_count=20)
        print(f"  ✅ Loaded {len(conversations)} conversations", flush=True)
        
        for guideline in guidelines:
            current_test += 1
            
            elapsed = time.time() - start_time
            avg_time = elapsed / current_test if current_test > 1 else 0
            remaining = avg_time * (total_tests - current_test)
            
            print(f"\n{'='*70}", flush=True)
            print(f"TEST {current_test}/{total_tests}: {data_type} - {guideline.title()}", flush=True)
            if current_test > 1:
                print(f"Progress: {current_test/total_tests*100:.1f}% | Elapsed: {elapsed/60:.1f}min | ETA: {remaining/60:.1f}min", flush=True)
            print(f"{'='*70}", flush=True)
            
            # Run test
            results = test_conversations(data_type, guideline, conversations)
            
            # Save results
            print(f"\n  💾 Saving results...", flush=True)
            filepath = save_results(results, data_type, guideline)
            print(f"  ✅ Saved: {filepath}", flush=True)
            
            # Print summary
            print_summary(results)
            
            # Delay between tests
            if current_test < total_tests:
                print(f"\n  ⏸️  Pausing 2s before next test...", flush=True)
                time.sleep(2)
    
    end_time = time.time()
    total_minutes = (end_time - start_time) / 60
    
    print(f"\n{'='*70}", flush=True)
    print("🎉 ALL TESTS COMPLETED!", flush=True)
    print(f"{'='*70}", flush=True)
    print(f"  ⏱️  Total time: {total_minutes:.1f} minutes ({total_minutes/60:.2f} hours)", flush=True)
    print(f"  📁 Results: MISTRAL_BOOM_BOOM/server3_base_openchat_mistral/", flush=True)
    print(f"  🎯 Tests completed: {current_test}/{total_tests}", flush=True)
    print(f"{'='*70}", flush=True)

if __name__ == "__main__":
    main()

