#!/usr/bin/env python3
"""
Gemini 2.0 Flash Testing Script for 20 Conversations (Type2b)
Model: Gemini 2.0 Flash via Google AI API
Free Tier Info (2025):
- 60 requests per minute (RPM)
- 1,500 requests per day (RPD)
- Free forever (no credit card required)
- Context length: 1M tokens
- Fastest Gemini model
"""

import os
import sys
import json
import csv
import time
import signal
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
from prompts import ASSESSMENT_PROMPTS

# Try to import Google Generative AI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    print("⚠️  google-generativeai not installed. Install with: pip install google-generativeai")
    GEMINI_AVAILABLE = False

# Configuration
MODEL_NAME = "gemini-2.0-flash-exp"
TOKEN_LIMIT = 1000000  # Gemini 2.0 Flash supports 1M tokens
MAX_RETRIES = 3
RETRY_DELAY = 2
ROUND_ROBIN_THRESHOLD = 5  # Switch key every 5 requests

# Multiple API keys for round-robin (5 keys for better distribution)
API_KEYS = [
    "AIzaSyDo2vO8BYoa4TwDtZyjGDvhqWy5kFvtkxI",
    "AIzaSyDumRCiulhPvGYHxTgkKDhJgNaJ5a4YZfI",
    "AIzaSyChVqT8tqsaXQgOX3DvabdEIGcFrWr40GI",
    "AIzaSyDlKXGLc7uXlGO4tp59eQhkqK3Y1Kd8rN0",
    "AIzaSyD-horARUkSzr0pRSxTtOS6xuAYTv0LVHE"
]

if GEMINI_AVAILABLE:
    genai.configure(api_key=API_KEYS[0])

class Gemini20Tester:
    def __init__(self):
        if not GEMINI_AVAILABLE:
            print("❌ Gemini API not available")
            sys.exit(1)
        
        print("🚀 Initializing Gemini 2.0 Flash (Multi-Key Round-Robin)...")
        print(f"   📝 Using {len(API_KEYS)} API keys in rotation")
        self.models = [genai.GenerativeModel(MODEL_NAME) for _ in API_KEYS]
        self.current_key_idx = 0
        self.requests_on_current_key = 0
        self.results = []
        self.stats = {'total_tests': 0, 'successful': 0, 'failed': 0, 'parse_errors': 0}
        self.failed_requests = []  # Track failed requests for retry at end
        self.consecutive_failures = 0  # Track consecutive failures across all keys
        
        # Initialize output paths early
        output_dir = Path(__file__).parent / 'results'
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.results_file = output_dir / f'gemini_results_20_convo_{timestamp}.json'
        self.results_file_simple = output_dir / 'gemini_results_20_convo.json'
        
        print(f"   💾 Results will be saved to: {self.results_file}")
        
        # Setup signal handler for graceful exit
        def save_and_exit(signum, frame):
            print("\n\n⚠️  Interrupted! Saving partial results...")
            self.save_partial_results()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, save_and_exit)
    
    def get_current_model(self):
        """Get the current model based on round-robin"""
        return self.models[self.current_key_idx]
    
    def rotate_key_if_needed(self):
        """Rotate to next API key every N requests"""
        self.requests_on_current_key += 1
        if self.requests_on_current_key >= ROUND_ROBIN_THRESHOLD:
            self.current_key_idx = (self.current_key_idx + 1) % len(API_KEYS)
            self.requests_on_current_key = 0
            print(f"   🔄 Switched to API key {self.current_key_idx + 1}/{len(API_KEYS)}")
    
    def refresh_model(self):
        """Reconfigure genai with current key"""
        genai.configure(api_key=API_KEYS[self.current_key_idx])
    
    def validate_token_limit(self, prompt, conversation):
        # Gemini 2.0 Flash supports up to 1M tokens - no validation needed
        total_approx = len(prompt + conversation) / 4  # Rough estimate
        print(f"   ✓ Token check: ~{int(total_approx)} tokens (well within 1M limit)")
        return int(total_approx), True
    
    def make_request(self, prompt, conversation_text, guideline, data_type, conversation_id):
        for attempt in range(MAX_RETRIES):
            try:
                # Use round-robin to select current model
                current_model = self.get_current_model()
                
                start_time = time.time()
                
                # Prepare the full prompt
                full_prompt = f"{prompt}\n\nConversation:\n{conversation_text}\n\nRespond with JSON only."
                
                # Generate content
                response = current_model.generate_content(
                    full_prompt,
                    generation_config={
                        'temperature': 0.1,
                        'max_output_tokens': 500,
                    }
                )
                
                end_time = time.time()
                duration = end_time - start_time
                content = response.text
                
                # Parse JSON response
                try:
                    cleaned_content = content.strip()
                    if cleaned_content.startswith('```json'):
                        cleaned_content = cleaned_content[7:]
                    if cleaned_content.startswith('```'):
                        cleaned_content = cleaned_content[3:]
                    if cleaned_content.endswith('```'):
                        cleaned_content = cleaned_content[:-3]
                    cleaned_content = cleaned_content.strip()
                    
                    parsed_response = json.loads(cleaned_content)
                    
                    status = (parsed_response.get('status') or parsed_response.get('Status') or 
                             parsed_response.get('value') or parsed_response.get('Value') or 'unknown')
                    value = (parsed_response.get('value') or parsed_response.get('Value') or 'unknown')
                    evidence = (parsed_response.get('evidence') or parsed_response.get('Evidence') or '')
                    
                    self.stats['successful'] += 1
                    parse_error = False
                    
                except json.JSONDecodeError:
                    status = 'Parse Error'
                    value = 'Parse Error'
                    evidence = content
                    self.stats['parse_errors'] += 1
                    parse_error = True
                
                # Rotate key after successful request
                self.rotate_key_if_needed()
                
                return {
                    'conversation_id': conversation_id,
                    'guideline': guideline,
                    'data_type': data_type,
                    'status': status,
                    'value': value,
                    'evidence': evidence,
                    'response': content,
                    'duration': duration,
                    'attempt': attempt + 1,
                    'success': True,
                    'parse_error': parse_error
                }
                
            except Exception as e:
                error_msg = str(e).lower()
                print(f"   ⚠️  Error on attempt {attempt + 1}: {str(e)[:100]}")
                
                # Detect rate limit or quota errors
                is_rate_limit = any(keyword in error_msg for keyword in ['rate limit', 'quota', 'exceeded', 'too many requests'])
                
                if is_rate_limit:
                    print(f"   🚫 Rate limit detected - rotating key immediately")
                    self.current_key_idx = (self.current_key_idx + 1) % len(API_KEYS)
                    self.requests_on_current_key = 0
                    self.refresh_model()
                    print(f"   🔄 Switched to API key {self.current_key_idx + 1}/{len(API_KEYS)}")
                
                if attempt < MAX_RETRIES - 1:
                    if not is_rate_limit:
                        # Rotate key on failure (non-rate-limit)
                        self.current_key_idx = (self.current_key_idx + 1) % len(API_KEYS)
                        self.requests_on_current_key = 0
                        self.refresh_model()
                        print(f"   🔄 Switched to API key {self.current_key_idx + 1}/{len(API_KEYS)} for retry")
                    
                    wait_time = RETRY_DELAY * (attempt + 1)  # Increasing backoff
                    print(f"   ⏳ Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                
                self.stats['failed'] += 1
                
                # Final failure
                if is_rate_limit:
                    return {
                        'conversation_id': conversation_id,
                        'guideline': guideline,
                        'data_type': data_type,
                        'status': 'Rate Limit',
                        'value': 'Rate Limit',
                        'evidence': '',
                        'response': str(e),
                        'duration': 0,
                        'attempt': attempt + 1,
                        'success': False
                    }
                
                return {
                    'conversation_id': conversation_id,
                    'guideline': guideline,
                    'data_type': data_type,
                    'status': 'Failed',
                    'value': 'Failed',
                    'evidence': '',
                    'response': str(e),
                    'duration': 0,
                    'attempt': attempt + 1,
                    'success': False
                }
    
    def test_conversations(self, data_path, guideline):
        print(f"\n{'='*60}\nTesting Guideline: {guideline.upper()}\n{'='*60}")
        conversations = []
        with open(data_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                conversations.append(row)
        
        print(f"Loaded {len(conversations)} conversations")
        prompt = ASSESSMENT_PROMPTS[guideline]
        
        for idx, row in enumerate(conversations, 1):
            conversation_id = row.get('conversation_id', '')
            conversation_text = row.get('transcript', '')
            
            print(f"\n📝 Testing conversation {idx}/{len(conversations)}: {conversation_id[:8]}...")
            
            # Token check (informational only for Gemini)
            self.validate_token_limit(prompt, conversation_text)
            
            print(f"   🔄 Sending request to Gemini API...")
            result = self.make_request(prompt, conversation_text, guideline, 'type2b', conversation_id)
            self.results.append(result)
            self.stats['total_tests'] += 1
            
            status_icon = "✓" if result['success'] and not result.get('parse_error') else "✗"
            print(f"   {status_icon} Response: {result['status']} ({result['duration']:.2f}s)")
            
            # Track consecutive failures
            if not result['success']:
                self.consecutive_failures += 1
                self.failed_requests.append({
                    'prompt': prompt,
                    'conversation_text': conversation_text,
                    'guideline': guideline,
                    'data_type': 'type2b',
                    'conversation_id': conversation_id,
                    'idx': idx
                })
                
                # If 5 consecutive failures, all keys exhausted - stop and save
                if self.consecutive_failures >= 5:
                    print(f"\n⚠️  {self.consecutive_failures} consecutive failures - all keys exhausted!")
                    print("💾 Saving progress and stopping...")
                    self.save_partial_results()
                    print("\n✅ Results saved. Please wait 15+ minutes before resuming.")
                    return False  # Signal to stop testing
            else:
                self.consecutive_failures = 0  # Reset on success
            
            # Rate limiting: 10 sec after each conversation, 30 sec after every 5 conversations
            if idx % 5 == 0:
                print(f"   ⏸️  Buffer time: 30 seconds (rate limit protection)...")
                time.sleep(30)
            else:
                print(f"   ⏸️  Buffer time: 10 seconds...")
                time.sleep(10)
        
        # Save progress after each guideline
        print(f"\n💾 Saving progress after {guideline.upper()} guideline...")
        self.save_progress()
        
        return True  # Continue testing
    
    def retry_failed_requests(self):
        """Retry all failed requests at the end with key rotation"""
        if not self.failed_requests:
            print("\n✅ No failed requests to retry!")
            return
        
        print(f"\n🔄 Retrying {len(self.failed_requests)} failed requests...")
        print("="*60)
        
        # Reset to first key
        self.current_key_idx = 0
        self.requests_on_current_key = 0
        
        retry_results = []
        for i, failed_req in enumerate(self.failed_requests, 1):
            print(f"\n🔄 Retry {i}/{len(self.failed_requests)}: {failed_req['conversation_id'][:8]}...")
            print(f"   📋 Guideline: {failed_req['guideline'].upper()}")
            
            # Rotate key at start of each retry
            self.current_key_idx = (i - 1) % len(API_KEYS)
            self.requests_on_current_key = 0
            self.refresh_model()
            print(f"   🔑 Using API key {self.current_key_idx + 1}/{len(API_KEYS)}")
            
            result = self.make_request(
                failed_req['prompt'],
                failed_req['conversation_text'],
                failed_req['guideline'],
                failed_req['data_type'],
                failed_req['conversation_id']
            )
            
            # Update the original result in results list
            for orig_result in self.results:
                if (orig_result['conversation_id'] == failed_req['conversation_id'] and
                    orig_result['guideline'] == failed_req['guideline']):
                    # Replace with retry result
                    orig_result.update({
                        'status': result['status'],
                        'value': result['value'],
                        'evidence': result['evidence'],
                        'response': result['response'],
                        'duration': result['duration'],
                        'attempt': result['attempt'],
                        'success': result['success'],
                        'parse_error': result.get('parse_error', False)
                    })
                    break
            
            retry_results.append(result)
            
            status_icon = "✓" if result['success'] else "✗"
            print(f"   {status_icon} Retry result: {result['status']} ({result['duration']:.2f}s)")
            
            # Wait between retries
            time.sleep(10)
        
        # Update stats
        successful_retries = sum(1 for r in retry_results if r['success'])
        print(f"\n✅ Retry Summary: {successful_retries}/{len(retry_results)} successful")
    
    def save_progress(self):
        """Save current progress"""
        if self.results_file_simple:
            output_data = {
                'model': MODEL_NAME,
                'provider': 'Google AI (Gemini API)',
                'test_date': datetime.now().isoformat(),
                'total_tests': len(self.results),
                'stats': self.stats,
                'status': 'IN PROGRESS',
                'free_tier_info': {
                    'requests_per_minute': 60,
                    'requests_per_day': 1500,
                    'context_length': '1M tokens',
                    'cost': 'Free forever'
                },
                'results': self.results
            }
            
            with open(self.results_file_simple, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"   ✓ Progress saved to: {self.results_file_simple}")
    
    def save_partial_results(self):
        """Save partial results on interruption"""
        if self.results_file:
            partial_file = str(self.results_file).replace('.json', '_PARTIAL.json')
            output_data = {
                'model': MODEL_NAME,
                'provider': 'Google AI (Gemini API)',
                'test_date': datetime.now().isoformat(),
                'total_tests': len(self.results),
                'stats': self.stats,
                'status': 'PARTIAL - Interrupted',
                'free_tier_info': {
                    'requests_per_minute': 60,
                    'requests_per_day': 1500,
                    'context_length': '1M tokens',
                    'cost': 'Free forever'
                },
                'results': self.results
            }
            
            with open(partial_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Partial results saved to: {partial_file}")
        
        # Also save to simple filename
        if self.results_file_simple:
            output_data = {
                'model': MODEL_NAME,
                'provider': 'Google AI (Gemini API)',
                'test_date': datetime.now().isoformat(),
                'total_tests': len(self.results),
                'stats': self.stats,
                'status': 'PARTIAL - Interrupted',
                'free_tier_info': {
                    'requests_per_minute': 60,
                    'requests_per_day': 1500,
                    'context_length': '1M tokens',
                    'cost': 'Free forever'
                },
                'results': self.results
            }
            
            with open(self.results_file_simple, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Partial results also saved to: {self.results_file_simple}")
    
    def save_results(self, output_path):
        output_data = {
            'model': MODEL_NAME,
            'provider': 'Google AI (Gemini API)',
            'test_date': datetime.now().isoformat(),
            'total_tests': len(self.results),
            'stats': self.stats,
            'free_tier_info': {
                'requests_per_minute': 60,
                'requests_per_day': 1500,
                'context_length': '1M tokens',
                'cost': 'Free forever'
            },
            'results': self.results
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Results saved to: {output_path}")
        return output_path

def main():
    print("🚀 Starting Gemini 2.0 Flash Test (20 Conversations)")
    print("="*60)
    print(f"Model: {MODEL_NAME}")
    print(f"Provider: Google AI (Free Tier)")
    print("="*60)
    print("\n💰 FREE TIER INFO (2025):")
    print("   • 60 requests per minute")
    print("   • 1,500 requests per day")
    print("   • Free forever (no credit card)")
    print("   • 1M token context length")
    print("="*60)
    
    if not GEMINI_AVAILABLE:
        print("\n❌ Please install: pip install google-generativeai")
        return
    
    tester = Gemini20Tester()
    data_path = Path(__file__).parent / 'DATA' / 'type2b_20_conversations.csv'
    
    guidelines = ['opening', 'closing', 'reassurance', 'hold', 'further_assistance']
    for guideline in guidelines:
        continue_testing = tester.test_conversations(str(data_path), guideline)
        if not continue_testing:
            print("\n⚠️  Testing stopped due to exhausted API keys.")
            print("💾 Final results saved.")
            return
    
    # Retry all failed requests at the end
    if tester.failed_requests:
        print("\n" + "="*60)
        print("RETRY PHASE")
        print("="*60)
        tester.retry_failed_requests()
    
    # Save final results
    tester.save_results(str(tester.results_file))
    tester.save_results(str(tester.results_file_simple))
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Total Tests: {tester.stats['total_tests']}")
    print(f"Successful: {tester.stats['successful']}")
    print(f"Failed: {tester.stats['failed']}")
    print(f"Parse Errors: {tester.stats['parse_errors']}")
    print("\n🎉 Test completed!")

if __name__ == '__main__':
    main()

