#!/usr/bin/env python3
"""
Qwen2.5-7B-Instruct Testing Script for 20 Conversations
Tests all 5 guidelines on the 20 conversation dataset
Server: RTX 4000 at 27.111.72.51:3333
"""

import sys
import json
import csv
import time
import requests
from pathlib import Path
from datetime import datetime
from transformers import AutoTokenizer

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from prompts import ASSESSMENT_PROMPTS

# Configuration
SERVER_URL = "http://27.111.72.51:3333/v1/chat/completions"
MODEL_NAME = "openchat/openchat-3.5-1210"  # Actually running OpenChat on port 3333
TOKEN_LIMIT = 8100
MAX_RETRIES = 3
RETRY_DELAY = 2

class OpenChat20Tester:
    def __init__(self):
        print("🚀 Loading tokenizer...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("openchat/openchat-3.5-1210", trust_remote_code=True)
        except Exception as e:
            print(f"⚠️  Error loading tokenizer: {e}")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "sentencepiece", "protobuf"])
            self.tokenizer = AutoTokenizer.from_pretrained("openchat/openchat-3.5-1210", trust_remote_code=True)
        
        self.results = []
        self.stats = {
            'total_tests': 0,
            'successful': 0,
            'failed': 0,
            'token_limit_exceeded': 0
        }
        
    def count_tokens(self, text):
        """Count tokens in text"""
        return len(self.tokenizer.encode(text))
    
    def validate_token_limit(self, prompt, conversation):
        """Check if total tokens exceed limit"""
        prompt_tokens = self.count_tokens(prompt)
        conv_tokens = self.count_tokens(conversation)
        total_tokens = prompt_tokens + conv_tokens + 500  # +500 for output buffer
        
        return total_tokens, total_tokens <= TOKEN_LIMIT
    
    def make_request(self, prompt, conversation_text, guideline, data_type, conversation_id):
        """Make API request with retry logic"""
        # Validate token limit
        total_tokens, is_valid = self.validate_token_limit(prompt, conversation_text)
        
        if not is_valid:
            print(f"   ⚠️  Token limit exceeded: {total_tokens} tokens (limit: {TOKEN_LIMIT})")
            self.stats['token_limit_exceeded'] += 1
            return {
                'conversation_id': conversation_id,
                'guideline': guideline,
                'data_type': data_type,
                'status': 'Exceeded',
                'value': 'Exceeded',
                'evidence': '',
                'response': '',
                'duration': 0,
                'attempt': 0,
                'success': False
            }
        
        # Prepare messages
        messages = [
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': conversation_text}
        ]
        
        payload = {
            'model': MODEL_NAME,
            'messages': messages,
            'max_tokens': 500,
            'temperature': 0.1
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                start_time = time.time()
                response = requests.post(SERVER_URL, json=payload, timeout=30)
                end_time = time.time()
                duration = end_time - start_time
                
                result_data = response.json()
                
                # Check for errors
                if 'error' in result_data:
                    raise Exception(f"API Error: {result_data['error'].get('message', 'Unknown error')}")
                
                if 'choices' not in result_data or not result_data['choices']:
                    raise Exception(f"Invalid response structure: {result_data.keys()}")
                
                content = result_data['choices'][0]['message']['content']
                
                # Parse the response
                try:
                    # Clean markdown code blocks if present
                    cleaned_content = content.strip()
                    if cleaned_content.startswith('```json'):
                        cleaned_content = cleaned_content[7:]
                    if cleaned_content.startswith('```'):
                        cleaned_content = cleaned_content[3:]
                    if cleaned_content.endswith('```'):
                        cleaned_content = cleaned_content[:-3]
                    cleaned_content = cleaned_content.strip()
                    
                    parsed_response = json.loads(cleaned_content)
                    
                    # Handle both lowercase and capitalized field names
                    status = (parsed_response.get('status') or 
                             parsed_response.get('Status') or 
                             parsed_response.get('value') or 
                             parsed_response.get('Value') or 
                             'unknown')
                    
                    value = (parsed_response.get('value') or 
                            parsed_response.get('Value') or 
                            parsed_response.get('guideline') or 
                            parsed_response.get('Guideline') or 
                            'unknown')
                    
                    evidence = (parsed_response.get('evidence') or 
                               parsed_response.get('Evidence') or 
                               '')
                    
                except json.JSONDecodeError as e:
                    status = 'Parse Error'
                    value = 'Parse Error'
                    evidence = content
                
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
                    'success': True
                }
                
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                    continue
                else:
                    return {
                        'conversation_id': conversation_id,
                        'guideline': guideline,
                        'data_type': data_type,
                        'status': 'Failed',
                        'value': 'Failed',
                        'evidence': '',
                        'response': str(e),
                        'duration': duration,
                        'attempt': attempt + 1,
                        'success': False
                    }
    
    def test_conversations(self, data_path, guideline):
        """Test conversations for a specific guideline"""
        print(f"\n{'='*60}")
        print(f"Testing Guideline: {guideline.upper()}")
        print('='*60)
        
        # Load conversations
        conversations = []
        with open(data_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                conversations.append(row)
        
        print(f"Loaded {len(conversations)} conversations")
        
        # Get prompt
        prompt = ASSESSMENT_PROMPTS[guideline]
        
        for idx, row in enumerate(conversations, 1):
            conversation_id = row.get('conversation_id', '')
            conversation_text = row.get('transcript', '')
            
            print(f"\n📝 Testing conversation {idx}/{len(conversations)}: {conversation_id[:8]}...")
            
            # Validate tokens
            total_tokens, is_valid = self.validate_token_limit(prompt, conversation_text)
            if is_valid:
                print(f"   ✓ Token check passed: {total_tokens} tokens")
            else:
                print(f"   ⚠️  Token limit exceeded: {total_tokens} tokens")
            
            # Make request
            print(f"   🔄 Sending request to {SERVER_URL}...")
            result = self.make_request(prompt, conversation_text, guideline, 'type2b', conversation_id)
            self.results.append(result)
            self.stats['total_tests'] += 1
            
            if result['success']:
                self.stats['successful'] += 1
            else:
                self.stats['failed'] += 1
            
            # Print progress
            status_icon = "✓" if result['success'] else "✗"
            status_text = result['status']
            print(f"   {status_icon} Response: {status_text} ({result['duration']:.2f}s)")
    
    def save_results(self, output_path):
        """Save results to JSON file"""
        output_data = {
            'model': MODEL_NAME,
            'server': SERVER_URL,
            'test_date': datetime.now().isoformat(),
            'total_tests': len(self.results),
            'stats': self.stats,
            'results': self.results
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Results saved to: {output_path}")
        return output_path

def main():
    print("🚀 Starting OpenChat-3.5-1210 Test (20 Conversations)")
    print("="*60)
    print(f"Server: 27.111.72.51:3333")
    print(f"Model: {MODEL_NAME}")
    print("="*60)
    
    # Initialize tester
    tester = OpenChat20Tester()
    
    # Data path - using type2b instead
    data_path = Path(__file__).parent / 'DATA' / 'type2b_20_conversations.csv'
    
    # Test all guidelines
    guidelines = ['opening', 'closing', 'reassurance', 'hold', 'further_assistance']
    
    for guideline in guidelines:
        tester.test_conversations(str(data_path), guideline)
    
    # Save results
    output_dir = Path(__file__).parent / 'results'
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # results_file = output_dir / f'openchat_results_20_convo_{timestamp}.json'
    # Save with simpler name
    results_file_simple = output_dir / 'openchat_results_20_convo.json'
    
    # tester.save_results(str(results_file))
    tester.save_results(str(results_file_simple))  # Also save with simple name
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Total Tests: {tester.stats['total_tests']}")
    print(f"Successful: {tester.stats['successful']}")
    print(f"Failed: {tester.stats['failed']}")
    print(f"Token Limit Exceeded: {tester.stats['token_limit_exceeded']}")
    print("\n🎉 Test completed!")

if __name__ == '__main__':
    main()

