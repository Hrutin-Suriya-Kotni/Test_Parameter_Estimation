#!/usr/bin/env python3
"""
Qwen2.5-7B-Instruct Comprehensive Testing Script
Tests all guidelines across all data types with token validation
Server: RTX 4000 at localhost:8000
Model: Qwen/Qwen2.5-7B-Instruct (better for Hindi-English code-mixed transcripts)
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
SERVER_URL = "http://27.111.72.51:8000/v1/chat/completions"
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
TOKEN_LIMIT = 8100
MAX_RETRIES = 3
RETRY_DELAY = 2

class QwenTester:
    def __init__(self):
        print("Loading tokenizer...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct", trust_remote_code=True)
        except ValueError as e:
            if "sentencepiece" in str(e):
                print("\n⚠️  sentencepiece not installed. Installing now...")
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", "sentencepiece", "protobuf"])
                print("✅ sentencepiece installed. Retrying tokenizer load...")
                self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct", trust_remote_code=True)
            else:
                raise
        self.results = []
        self.stats = {
            'total_tests': 0,
            'successful': 0,
            'failed': 0,
            'token_limit_exceeded': 0,
            'by_guideline': {},
            'by_data_type': {}
        }

    def count_tokens(self, text):
        """Count tokens using Qwen tokenizer"""
        if not text:
            return 0
        try:
            tokens = self.tokenizer.encode(text, add_special_tokens=True)
            return len(tokens)
        except Exception as e:
            print(f"⚠️  Token counting error: {e}")
            return 0

    def check_token_limit(self, prompt, conversation_text):
        """Check if total tokens exceed limit"""
        prompt_tokens = self.count_tokens(prompt)
        conversation_tokens = self.count_tokens(conversation_text)
        total_tokens = prompt_tokens + conversation_tokens
        
        print(f"   ✓ Token check passed: {total_tokens} tokens", end="")
        
        if total_tokens > TOKEN_LIMIT:
            print(f" → Token limit exceeded ({total_tokens} > {TOKEN_LIMIT})")
            return False, total_tokens
        else:
            print(f" → Token check passed")
            return True, total_tokens

    def make_request(self, prompt, conversation_text, guideline, data_type, conversation_id):
        """Make API request with retry logic"""
        for attempt in range(MAX_RETRIES):
            try:
                start_time = time.time()
                
                payload = {
                    "model": MODEL_NAME,
                    "messages": [
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": conversation_text}
                    ],
                    "max_tokens": 500,
                    "temperature": 0.1
                }
                
                response = requests.post(SERVER_URL, json=payload, timeout=30)
                response.raise_for_status()
                
                end_time = time.time()
                duration = end_time - start_time
                
                result_data = response.json()
                content = result_data['choices'][0]['message']['content']
                
                # Parse the response
                try:
                    # Clean the content - remove markdown code blocks if present
                    cleaned_content = content.strip()
                    if cleaned_content.startswith('```json'):
                        cleaned_content = cleaned_content[7:]  # Remove ```json
                    if cleaned_content.startswith('```'):
                        cleaned_content = cleaned_content[3:]   # Remove ```
                    if cleaned_content.endswith('```'):
                        cleaned_content = cleaned_content[:-3]  # Remove trailing ```
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
                    
                    # Debug: Print first few responses to see what's happening
                    if len(self.results) < 3:
                        print(f"    🔍 Debug - Raw: {repr(content[:100])}")
                        print(f"    🔍 Debug - Cleaned: {repr(cleaned_content[:100])}")
                        print(f"    🔍 Debug - Status: {status}, Value: {value}")
                        print(f"    🔍 Debug - All keys: {list(parsed_response.keys())}")
                        
                except json.JSONDecodeError as e:
                    status = 'Parse Error'
                    value = 'Parse Error'
                    evidence = content
                    print(f"    ❌ JSON Parse Error: {e}")
                    print(f"    ❌ Content: {repr(content[:200])}")
                
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
                
            except requests.exceptions.RequestException as e:
                print(f" → Retry {attempt + 1}...")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                else:
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
            except Exception as e:
                return {
                    'conversation_id': conversation_id,
                    'guideline': guideline,
                    'data_type': data_type,
                    'status': 'Error',
                    'value': 'Error',
                    'evidence': '',
                    'response': str(e),
                    'duration': 0,
                    'attempt': attempt + 1,
                    'success': False
                }

    def test_type1_conversations(self, guideline, data_dir):
        """Test Type1 conversations"""
        print(f"Testing Type1 - {guideline.upper()}")
        
        csv_file = data_dir / 'type1_overall_paragraph.csv'
        if not csv_file.exists():
            print(f"❌ File not found: {csv_file}")
            return
        
        prompt = ASSESSMENT_PROMPTS[guideline]
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            total_rows = len(rows)
            
            for i, row in enumerate(rows, 1):
                conversation_id = row.get('conversation_id', f'unknown_{i}')
                conversation_text = row.get('transcript', '')
                
                if not conversation_text:
                    continue
                
                # Check token limit
                token_ok, token_count = self.check_token_limit(prompt, conversation_text)
                if not token_ok:
                    self.stats['token_limit_exceeded'] += 1
                    print(f"[{i:2d}/{total_rows}] {conversation_id[:8]}...   → Token limit exceeded ({token_count} tokens)")
                    continue
                
                # Make request
                result = self.make_request(prompt, conversation_text, guideline, 'type1', conversation_id)
                self.results.append(result)
                
                if result['success']:
                    self.stats['successful'] += 1
                    print(f"[{i:2d}/{total_rows}] {conversation_id[:8]}...   → {result['status']} ({result['duration']:.2f}s)")
                else:
                    self.stats['failed'] += 1
                    print(f"[{i:2d}/{total_rows}] {conversation_id[:8]}...   → Failed ({result['duration']:.2f}s)")
                
                self.stats['total_tests'] += 1
                
                # Show progress every 10 tests
                if i % 10 == 0:
                    success_rate = (self.stats['successful'] / max(self.stats['total_tests'], 1)) * 100
                    print(f"    📊 Progress: {i}/{total_rows} | Success: {self.stats['successful']}/{self.stats['total_tests']} ({success_rate:.1f}%)")

    def test_type2a_conversations(self, guideline, data_dir):
        """Test Type2a conversations"""
        print(f"Testing Type2a - {guideline.upper()}")
        
        json_dir = data_dir / 'type2a_json'
        if not json_dir.exists():
            print(f"❌ Directory not found: {json_dir}")
            return
        
        prompt = ASSESSMENT_PROMPTS[guideline]
        
        json_files = list(json_dir.glob('*.json'))
        total_files = len(json_files)
        
        for i, json_file in enumerate(json_files, 1):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                conversation_id = data.get('conversation_id', f'unknown_{i}')
                conversation_text = json.dumps(data, ensure_ascii=False)
                
                # Check token limit
                token_ok, token_count = self.check_token_limit(prompt, conversation_text)
                if not token_ok:
                    self.stats['token_limit_exceeded'] += 1
                    print(f"[{i:2d}/{total_files}] {conversation_id[:8]}...   → Token limit exceeded ({token_count} tokens)")
                    continue
                
                # Make request
                result = self.make_request(prompt, conversation_text, guideline, 'type2a', conversation_id)
                self.results.append(result)
                
                if result['success']:
                    self.stats['successful'] += 1
                    print(f"[{i:2d}/{total_files}] {conversation_id[:8]}...   → {result['status']} ({result['duration']:.2f}s)")
                else:
                    self.stats['failed'] += 1
                    print(f"[{i:2d}/{total_files}] {conversation_id[:8]}...   → Failed ({result['duration']:.2f}s)")
                
                self.stats['total_tests'] += 1
                
                # Show progress every 10 tests
                if i % 10 == 0:
                    success_rate = (self.stats['successful'] / max(self.stats['total_tests'], 1)) * 100
                    print(f"    📊 Progress: {i}/{total_files} | Success: {self.stats['successful']}/{self.stats['total_tests']} ({success_rate:.1f}%)")
                
            except Exception as e:
                print(f"[{i:2d}/{total_files}] {json_file.name}...   → Error: {e}")

    def test_type2b_conversations(self, guideline, data_dir):
        """Test Type2b conversations"""
        print(f"Testing Type2b - {guideline.upper()}")
        
        csv_file = data_dir / 'type2b_labeled_paragraph.csv'
        if not csv_file.exists():
            print(f"❌ File not found: {csv_file}")
            return
        
        prompt = ASSESSMENT_PROMPTS[guideline]
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            total_rows = len(rows)
            
            for i, row in enumerate(rows, 1):
                conversation_id = row.get('conversation_id', f'unknown_{i}')
                conversation_text = row.get('transcript', '')
                
                if not conversation_text:
                    continue
                
                # Check token limit
                token_ok, token_count = self.check_token_limit(prompt, conversation_text)
                if not token_ok:
                    self.stats['token_limit_exceeded'] += 1
                    print(f"[{i:2d}/{total_rows}] {conversation_id[:8]}...   → Token limit exceeded ({token_count} tokens)")
                    continue
                
                # Make request
                result = self.make_request(prompt, conversation_text, guideline, 'type2b', conversation_id)
                self.results.append(result)
                
                if result['success']:
                    self.stats['successful'] += 1
                    print(f"[{i:2d}/{total_rows}] {conversation_id[:8]}...   → {result['status']} ({result['duration']:.2f}s)")
                else:
                    self.stats['failed'] += 1
                    print(f"[{i:2d}/{total_rows}] {conversation_id[:8]}...   → Failed ({result['duration']:.2f}s)")
                
                self.stats['total_tests'] += 1
                
                # Show progress every 10 tests
                if i % 10 == 0:
                    success_rate = (self.stats['successful'] / max(self.stats['total_tests'], 1)) * 100
                    print(f"    📊 Progress: {i}/{total_rows} | Success: {self.stats['successful']}/{self.stats['total_tests']} ({success_rate:.1f}%)")

    def run_comprehensive_test(self, data_dir, output_dir):
        """Run comprehensive test across all guidelines and data types"""
        print("="*80)
        print("Qwen2.5-7B-Instruct Comprehensive Test")
        print("Server: 27.111.72.51:8000 (RTX 4000)")
        print("Model: Qwen/Qwen2.5-7B-Instruct")
        print("Token Limit: 8100")
        print("="*80)
        
        # Calculate total expected tests
        total_expected = 0
        for guideline in ASSESSMENT_PROMPTS.keys():
            # Count Type1 conversations
            csv_file = data_dir / 'type1_overall_paragraph.csv'
            if csv_file.exists():
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    total_expected += len(list(reader))
            
            # Count Type2a conversations
            json_dir = data_dir / 'type2a_json'
            if json_dir.exists():
                total_expected += len(list(json_dir.glob('*.json')))
            
            # Count Type2b conversations
            csv_file = data_dir / 'type2b_labeled_paragraph.csv'
            if csv_file.exists():
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    total_expected += len(list(reader))
        
        print(f"📊 Expected Total Tests: {total_expected}")
        print("="*80)
        
        # Test all guidelines across all data types
        for guideline in ASSESSMENT_PROMPTS.keys():
            print(f"\n{'='*80}")
            print(f"Testing Guideline: {guideline.upper()}")
            print(f"{'='*80}")
            
            # Initialize stats for this guideline
            self.stats['by_guideline'][guideline] = {
                'total': 0, 'successful': 0, 'failed': 0, 'exceeded': 0
            }
            
            # Test Type1
            self.test_type1_conversations(guideline, data_dir)
            
            # Test Type2a
            self.test_type2a_conversations(guideline, data_dir)
            
            # Test Type2b
            self.test_type2b_conversations(guideline, data_dir)
            
            # Show guideline summary
            guideline_stats = self.stats['by_guideline'][guideline]
            success_rate = (guideline_stats['successful'] / max(guideline_stats['total'], 1)) * 100
            print(f"\n📈 {guideline.upper()} Summary:")
            print(f"   Total: {guideline_stats['total']} | Success: {guideline_stats['successful']} ({success_rate:.1f}%) | Failed: {guideline_stats['failed']} | Exceeded: {guideline_stats['exceeded']}")
            
            # Show overall progress
            overall_success_rate = (self.stats['successful'] / max(self.stats['total_tests'], 1)) * 100
            print(f"\n🎯 Overall Progress: {self.stats['total_tests']}/{total_expected} | Success: {self.stats['successful']} ({overall_success_rate:.1f}%) | Failed: {self.stats['failed']} | Exceeded: {self.stats['token_limit_exceeded']}")
        
        # Calculate final stats
        self.calculate_final_stats()
        
        # Save results
        results_file = self.save_results(output_dir)
        
        # Print summary
        self.print_summary()
        
        return results_file

    def calculate_final_stats(self):
        """Calculate final statistics"""
        for result in self.results:
            guideline = result['guideline']
            data_type = result['data_type']
            
            # Update guideline stats
            if guideline not in self.stats['by_guideline']:
                self.stats['by_guideline'][guideline] = {'total': 0, 'successful': 0, 'failed': 0, 'exceeded': 0}
            
            self.stats['by_guideline'][guideline]['total'] += 1
            if result['success']:
                self.stats['by_guideline'][guideline]['successful'] += 1
            else:
                self.stats['by_guideline'][guideline]['failed'] += 1
            
            # Update data type stats
            if data_type not in self.stats['by_data_type']:
                self.stats['by_data_type'][data_type] = {'total': 0, 'successful': 0, 'failed': 0, 'exceeded': 0}
            
            self.stats['by_data_type'][data_type]['total'] += 1
            if result['success']:
                self.stats['by_data_type'][data_type]['successful'] += 1
            else:
                self.stats['by_data_type'][data_type]['failed'] += 1

    def save_results(self, output_dir):
        """Save results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = output_dir / f"qwen2.5_7b_test_results_{timestamp}.json"
        
        output_data = {
            'metadata': {
                'model': MODEL_NAME,
                'server_url': SERVER_URL,
                'token_limit': TOKEN_LIMIT,
                'timestamp': timestamp,
                'total_tests': len(self.results)
            },
            'stats': self.stats,
            'results': self.results
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Results saved to: {results_file}")
        return results_file

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"Total Tests: {self.stats['total_tests']}")
        print(f"Successful: {self.stats['successful']} ({self.stats['successful']/max(self.stats['total_tests'], 1)*100:.1f}%)")
        print(f"Failed: {self.stats['failed']}")
        print(f"Token Limit Exceeded: {self.stats['token_limit_exceeded']}")
        
        print("\nBy Guideline:")
        for guideline, stats in self.stats['by_guideline'].items():
            success_rate = stats['successful'] / max(stats['total'], 1) * 100
            print(f"  {guideline:<20} : {stats['successful']}/{stats['total']} success, {stats['exceeded']} exceeded")
        
        print("\nBy Data Type:")
        for data_type, stats in self.stats['by_data_type'].items():
            success_rate = stats['successful'] / max(stats['total'], 1) * 100
            print(f"  {data_type:<10} : {stats['successful']}/{stats['total']} success, {stats['exceeded']} exceeded")

def main():
    print("🚀 Starting Qwen2.5-7B-Instruct Test...")
    print("="*80)
    print("Qwen2.5-7B-Instruct Comprehensive Test")
    print("Server: 27.111.72.51:8000 (RTX 4000)")
    print("Model: Qwen/Qwen2.5-7B-Instruct")
    print("Token Limit: 8100")
    print("="*80)
    
    # Test connectivity first
    print("\nTesting Qwen2.5-7B-Instruct server connectivity...")
    try:
        response = requests.get("http://27.111.72.51:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is reachable!")
        else:
            print(f"⚠️  Server responded with status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot reach server: {e}")
        print("\nNOTE: Make sure Qwen2.5-7B-Instruct is running on 27.111.72.51:8000")
        return
    
    tester = QwenTester()
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'pre-processed-data'
    output_dir = base_dir / 'Mistarl-qwen-testing' / 'results'
    output_dir.mkdir(exist_ok=True)
    
    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir}")
        return
    
    # Run comprehensive test
    results_file = tester.run_comprehensive_test(data_dir, output_dir)
    
    print(f"\n🎉 Test completed! Results saved to: {results_file}")

if __name__ == "__main__":
    main()
