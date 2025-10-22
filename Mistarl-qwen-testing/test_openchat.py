#!/usr/bin/env python3
"""
OpenChat Comprehensive Testing Script
Tests all guidelines across all data types with token validation
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
TOKEN_LIMIT = 8100
MAX_RETRIES = 3
RETRY_DELAY = 2

class OpenChatTester:
    def __init__(self):
        print("Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained("openchat/openchat-3.5-1210", trust_remote_code=True)
        self.results = []
        self.stats = {
            'total_tests': 0,
            'successful': 0,
            'failed': 0,
            'token_limit_exceeded': 0,
            'by_guideline': {},
            'by_type': {}
        }
        
    def count_tokens(self, text):
        """Count tokens in text"""
        return len(self.tokenizer.encode(text))
    
    def validate_token_limit(self, prompt, conversation):
        """Check if total tokens exceed limit"""
        prompt_tokens = self.count_tokens(prompt)
        conv_tokens = self.count_tokens(conversation)
        total_tokens = prompt_tokens + conv_tokens + 200  # +200 for output buffer
        
        return total_tokens, total_tokens <= TOKEN_LIMIT
    
    def call_llm(self, prompt, conversation, conv_id, guideline, data_type):
        """Make API call with retry logic"""
        
        # Token validation
        total_tokens, is_valid = self.validate_token_limit(prompt, conversation)
        
        if not is_valid:
            print(f"  ⚠️  LIMIT EXCEEDED: {total_tokens} tokens (limit: {TOKEN_LIMIT})")
            self.stats['token_limit_exceeded'] += 1
            return {
                'conversation_id': conv_id,
                'guideline': guideline,
                'data_type': data_type,
                'status': 'token_limit_exceeded',
                'tokens': total_tokens,
                'error': f'Token limit exceeded: {total_tokens} > {TOKEN_LIMIT}'
            }
        
        print(f"  ✓ Token check passed: {total_tokens} tokens", end='', flush=True)
        
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": conversation}
        ]
        
        payload = {
            "model": "openchat/openchat-3.5-1210",
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 200
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                start_time = time.time()
                response = requests.post(SERVER_URL, json=payload, timeout=60)
                latency = time.time() - start_time
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    
                    # Try to extract JSON
                    try:
                        # Find JSON in response
                        start_idx = content.find('{')
                        end_idx = content.rfind('}') + 1
                        if start_idx != -1 and end_idx > start_idx:
                            json_str = content[start_idx:end_idx]
                            parsed = json.loads(json_str)
                            value = parsed.get('Value', 'Unknown')
                        else:
                            value = 'Parse Error'
                    except:
                        value = 'Parse Error'
                    
                    print(f" → {value} ({latency:.2f}s)")
                    self.stats['successful'] += 1
                    
                    return {
                        'conversation_id': conv_id,
                        'guideline': guideline,
                        'data_type': data_type,
                        'status': 'success',
                        'value': value,
                        'latency': round(latency, 2),
                        'tokens': total_tokens,
                        'response': content
                    }
                else:
                    if attempt < MAX_RETRIES - 1:
                        print(f" → Retry {attempt + 1}...", end='', flush=True)
                        time.sleep(RETRY_DELAY)
                    else:
                        print(f" → Failed: {response.status_code}")
                        self.stats['failed'] += 1
                        return {
                            'conversation_id': conv_id,
                            'guideline': guideline,
                            'data_type': data_type,
                            'status': 'failed',
                            'tokens': total_tokens,
                            'error': f'HTTP {response.status_code}: {response.text[:100]}'
                        }
                        
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f" → Retry {attempt + 1}...", end='', flush=True)
                    time.sleep(RETRY_DELAY)
                else:
                    print(f" → Error: {str(e)[:50]}")
                    self.stats['failed'] += 1
                    return {
                        'conversation_id': conv_id,
                        'guideline': guideline,
                        'data_type': data_type,
                        'status': 'failed',
                        'tokens': total_tokens,
                        'error': str(e)
                    }
    
    def test_type1(self, guideline, csv_path):
        """Test Type1 (plain text) data"""
        print(f"\n{'='*80}")
        print(f"Testing Type1 - {guideline.upper()}")
        print(f"{'='*80}")
        
        prompt = ASSESSMENT_PROMPTS[guideline]
        results = []
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, 1):
                conv_id = row['conversation_id']
                conversation = row.get('transcript', '')
                
                print(f"[{idx}] {conv_id[:8]}...", end=' ')
                self.stats['total_tests'] += 1
                
                result = self.call_llm(prompt, conversation, conv_id, guideline, 'type1')
                results.append(result)
                self.results.append(result)
                
                time.sleep(0.5)  # Rate limiting
        
        return results
    
    def test_type2a(self, guideline, json_dir):
        """Test Type2a (JSON) data"""
        print(f"\n{'='*80}")
        print(f"Testing Type2a - {guideline.upper()}")
        print(f"{'='*80}")
        
        prompt = ASSESSMENT_PROMPTS[guideline]
        results = []
        
        json_files = sorted(Path(json_dir).glob('*.json'))
        
        for idx, json_file in enumerate(json_files, 1):
            conv_id = json_file.stem
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                conversation = json.dumps(data, ensure_ascii=False)
            
            print(f"[{idx}] {conv_id[:8]}...", end=' ')
            self.stats['total_tests'] += 1
            
            result = self.call_llm(prompt, conversation, conv_id, guideline, 'type2a')
            results.append(result)
            self.results.append(result)
            
            time.sleep(0.5)
        
        return results
    
    def test_type2b(self, guideline, csv_path):
        """Test Type2b (labeled) data"""
        print(f"\n{'='*80}")
        print(f"Testing Type2b - {guideline.upper()}")
        print(f"{'='*80}")
        
        prompt = ASSESSMENT_PROMPTS[guideline]
        results = []
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, 1):
                conv_id = row['conversation_id']
                conversation = row.get('transcript', '')
                
                print(f"[{idx}] {conv_id[:8]}...", end=' ')
                self.stats['total_tests'] += 1
                
                result = self.call_llm(prompt, conversation, conv_id, guideline, 'type2b')
                results.append(result)
                self.results.append(result)
                
                time.sleep(0.5)
        
        return results
    
    def generate_report(self, output_dir):
        """Generate comprehensive test report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Calculate stats by guideline and type
        for result in self.results:
            guideline = result['guideline']
            data_type = result['data_type']
            status = result['status']
            
            # By guideline
            if guideline not in self.stats['by_guideline']:
                self.stats['by_guideline'][guideline] = {'success': 0, 'failed': 0, 'exceeded': 0}
            
            if status == 'success':
                self.stats['by_guideline'][guideline]['success'] += 1
            elif status == 'token_limit_exceeded':
                self.stats['by_guideline'][guideline]['exceeded'] += 1
            else:
                self.stats['by_guideline'][guideline]['failed'] += 1
            
            # By type
            if data_type not in self.stats['by_type']:
                self.stats['by_type'][data_type] = {'success': 0, 'failed': 0, 'exceeded': 0}
            
            if status == 'success':
                self.stats['by_type'][data_type]['success'] += 1
            elif status == 'token_limit_exceeded':
                self.stats['by_type'][data_type]['exceeded'] += 1
            else:
                self.stats['by_type'][data_type]['failed'] += 1
        
        # Save detailed results
        results_file = output_dir / f'openchat_test_results_{timestamp}.json'
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                'stats': self.stats,
                'results': self.results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*80}")
        print("TEST SUMMARY")
        print(f"{'='*80}")
        print(f"Total Tests: {self.stats['total_tests']}")
        print(f"Successful: {self.stats['successful']} ({self.stats['successful']/self.stats['total_tests']*100:.1f}%)")
        print(f"Failed: {self.stats['failed']}")
        print(f"Token Limit Exceeded: {self.stats['token_limit_exceeded']}")
        
        print(f"\nBy Guideline:")
        for guideline, counts in self.stats['by_guideline'].items():
            total = counts['success'] + counts['failed'] + counts['exceeded']
            print(f"  {guideline:20s}: {counts['success']}/{total} success, {counts['exceeded']} exceeded")
        
        print(f"\nBy Data Type:")
        for dtype, counts in self.stats['by_type'].items():
            total = counts['success'] + counts['failed'] + counts['exceeded']
            print(f"  {dtype:10s}: {counts['success']}/{total} success, {counts['exceeded']} exceeded")
        
        print(f"\n✅ Results saved to: {results_file}")
        
        return results_file

def main():
    print("="*80)
    print("OpenChat Comprehensive Test")
    print("Server: 27.111.72.51:3333")
    print("Token Limit: 8100")
    print("="*80)
    
    tester = OpenChatTester()
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'pre-processed-data'
    output_dir = base_dir / 'Mistarl-qwen-testing' / 'results'
    output_dir.mkdir(exist_ok=True)
    
    guidelines = ['opening', 'closing', 'reassurance', 'hold', 'further_assistance']
    
    # Test all combinations
    for guideline in guidelines:
        # Type1
        tester.test_type1(guideline, data_dir / 'type1_overall_paragraph.csv')
        
        # Type2a
        tester.test_type2a(guideline, data_dir / 'type2a_json')
        
        # Type2b
        tester.test_type2b(guideline, data_dir / 'type2b_labeled_paragraph.csv')
    
    # Generate report
    tester.generate_report(output_dir)

if __name__ == "__main__":
    main()

