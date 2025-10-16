#!/usr/bin/env python3
"""
Run comprehensive Gemini API tests
Tests Gemini on all data types and all guidelines

Features:
- 5 retry attempts with exponential backoff (2s → 4s → 8s → 16s → 32s)
- Temperature: 0.1 (for consistent output)
- Max Output Tokens: 512
- Data type explanations in system prompts
- Tests all 5 guidelines on all 3 data types
"""

import sys
import os
import time
import json
import pandas as pd
from datetime import datetime
from typing import Dict, Any, Optional, List

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from boom_boom_data_loader import BoomBoomDataLoader
from prompts import ASSESSMENT_PROMPTS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Data type explanations for context
DATA_TYPE_EXPLANATIONS = {
    'type1': """
DATA TYPE CONTEXT:
You are analyzing a complete conversation paragraph from a call center. 
The text is a continuous narrative without speaker labels or timestamps.
The conversation flows naturally as a single block of text.
""",
    
    'type2a': """
DATA TYPE CONTEXT:
You are analyzing structured call data in JSON format.
Each entry contains speaker identification (Agent/Customer), timestamps, and dialogue content.
The conversation is formatted with clear speaker labels and turn-by-turn structure.
""",
    
    'type2b': """
DATA TYPE CONTEXT:
You are analyzing a conversation transcript where each line is prefixed with speaker labels.
Format: "Agent: [text]" or "Customer: [text]"
Each turn in the conversation is clearly marked with who is speaking.
"""
}


class GeminiTestRunner:
    """Test runner specifically for Gemini API with retry logic"""
    
    def __init__(self):
        """Initialize Gemini test runner"""
        self.data_loader = BoomBoomDataLoader()
        self.results_base_dir = "gemini_results"
        self.model = None
        self.genai = None
        
        # Gemini configuration
        self.temperature = 0.1
        self.max_output_tokens = 512
        self.model_name = "gemini-2.0-flash-exp"
        
        # Retry configuration
        self.max_retries = 5
        self.retry_delays = [2, 4, 8, 16, 32]  # Exponential backoff
        
        print("🎉 Gemini Test Runner Initialized!")
        print(f"   Model: {self.model_name}")
        print(f"   Temperature: {self.temperature}")
        print(f"   Max Output Tokens: {self.max_output_tokens}")
        print(f"   Retry Strategy: {self.max_retries} attempts with exponential backoff")
    
    def initialize_gemini(self) -> bool:
        """Initialize Gemini client"""
        try:
            import google.generativeai as genai
            self.genai = genai
            
            # Load API key
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                print("❌ GEMINI_API_KEY not found in .env file!")
                print("   Please see GEMINI_ENV_SETUP.txt for instructions")
                return False
            
            # Configure Gemini
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(self.model_name)
            
            # Test connection
            print("🔍 Testing Gemini connection...")
            test_response = self.model.generate_content(
                "Hello, this is a test.",
                generation_config={
                    'temperature': self.temperature,
                    'max_output_tokens': 100
                }
            )
            
            if test_response.text:
                print("✅ Gemini API connection successful!")
                return True
            else:
                print("❌ Gemini API test failed")
                return False
                
        except ImportError:
            print("❌ google-generativeai package not installed!")
            print("   Run: pip install google-generativeai")
            return False
        except Exception as e:
            print(f"❌ Gemini initialization error: {e}")
            return False
    
    def analyze_with_retry(self, prompt: str, transcript: str, 
                          conversation_id: str) -> tuple[Optional[str], int, float]:
        """
        Analyze conversation with retry logic
        
        Returns:
            (response_text, attempts_used, total_time)
        """
        start_time = time.time()
        
        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"      🔄 Attempt {attempt}/{self.max_retries}...")
                
                # Safety settings to avoid blocking
                safety_settings = {
                    'HATE': 'BLOCK_NONE',
                    'HARASSMENT': 'BLOCK_NONE',
                    'SEXUAL': 'BLOCK_NONE',
                    'DANGEROUS': 'BLOCK_NONE'
                }
                
                response = self.model.generate_content(
                    prompt,
                    safety_settings=safety_settings,
                    generation_config={
                        'temperature': self.temperature,
                        'max_output_tokens': self.max_output_tokens
                    }
                )
                
                total_time = time.time() - start_time
                print(f"      ✅ Success on attempt {attempt}")
                return response.text, attempt, total_time
                
            except Exception as e:
                error_str = str(e).lower()
                print(f"      ⚠️  Attempt {attempt} failed: {str(e)[:100]}")
                
                # Check if it's a rate limit error
                is_rate_limit = any(term in error_str for term in 
                                   ['rate limit', 'quota', 'too many requests', '429'])
                
                if attempt < self.max_retries:
                    delay = self.retry_delays[attempt - 1]
                    print(f"      ⏳ Waiting {delay}s before retry...")
                    time.sleep(delay)
                else:
                    print(f"      ❌ All {self.max_retries} attempts failed")
                    total_time = time.time() - start_time
                    return None, attempt, total_time
        
        total_time = time.time() - start_time
        return None, self.max_retries, total_time
    
    def parse_json_response(self, response_text: str) -> Optional[Dict]:
        """Parse JSON from response text"""
        try:
            # Remove markdown code blocks if present
            text = response_text.strip()
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                text = text.split('```')[1].split('```')[0].strip()
            
            # Try to find JSON object
            if '{' in text and '}' in text:
                start = text.find('{')
                end = text.rfind('}') + 1
                json_str = text[start:end]
                parsed = json.loads(json_str)
                
                # Normalize 'Yes' to 'Met', 'No' to 'Not Met'
                if 'Value' in parsed:
                    if parsed['Value'].lower() in ['yes', 'met']:
                        parsed['Value'] = 'Met'
                    elif parsed['Value'].lower() in ['no', 'not met']:
                        parsed['Value'] = 'Not Met'
                
                return parsed
            
            return None
            
        except Exception as e:
            print(f"      ⚠️  JSON parse error: {e}")
            return None
    
    def test_single_conversation(self, conv: Dict[str, Any], 
                                 test_type: str,
                                 data_type: str) -> Dict[str, Any]:
        """
        Test a single conversation
        
        Args:
            conv: Conversation dictionary
            test_type: Assessment type (opening, closing, etc.)
            data_type: Data type (type1, type2a, type2b)
            
        Returns:
            Result dictionary
        """
        # Get base prompt
        base_prompt = ASSESSMENT_PROMPTS.get(test_type, ASSESSMENT_PROMPTS['opening'])
        
        # Add data type explanation at the beginning
        data_context = DATA_TYPE_EXPLANATIONS.get(data_type, "")
        
        # Construct full prompt
        full_prompt = f"""{data_context}

{base_prompt}

CRITICAL: You must respond with ONLY a valid JSON object. No additional text before or after.

Required JSON format:
{{"Value": "Met" or "Not Met", "Evidence": "detailed explanation"}}

Transcript:
{conv['transcript']}"""
        
        try:
            print(f"\n      🔍 Processing: {conv['id'][:40]}...")
            print(f"      📏 Transcript length: {len(conv['transcript'])} chars")
            print(f"      📊 Data type: {data_type}")
            
            # Analyze with retry logic
            response_text, attempts_used, total_time = self.analyze_with_retry(
                full_prompt, 
                conv['transcript'],
                conv['id']
            )
            
            if response_text is None:
                return {
                    'conversation_id': conv['id'],
                    'data_type': data_type,
                    'parameter_tested': test_type.upper(),
                    'parameter_name': test_type.replace('_', ' ').title(),
                    'model_name': self.model_name,
                    'timestamp': datetime.now().isoformat(),
                    'temperature': self.temperature,
                    'max_output_tokens': self.max_output_tokens,
                    'success': False,
                    'result_value': 'Error',
                    'evidence': f'Failed after {attempts_used} attempts',
                    'attempts_used': attempts_used,
                    'total_latency': round(total_time, 3),
                    'transcript_length': len(conv['transcript']),
                    'response_length': 0
                }
            
            # Parse response
            print(f"      🔄 Parsing JSON response...")
            print(f"      📝 Response length: {len(response_text)} chars")
            
            parsed = self.parse_json_response(response_text)
            
            if parsed:
                print(f"      ✅ Parse successful: {parsed.get('Value', 'Unknown')}")
            else:
                print(f"      ⚠️  Parse failed")
            
            # Build result
            result = {
                'conversation_id': conv['id'],
                'data_type': data_type,
                'parameter_tested': test_type.upper(),
                'parameter_name': test_type.replace('_', ' ').title(),
                'model_name': self.model_name,
                'timestamp': datetime.now().isoformat(),
                
                # API Configuration
                'temperature': self.temperature,
                'max_output_tokens': self.max_output_tokens,
                
                # Results
                'success': parsed is not None,
                'result_value': parsed.get('Value', 'Parse Error') if parsed else 'Parse Error',
                'evidence': parsed.get('Evidence', 'N/A') if parsed else 'Failed to parse JSON',
                
                # Metrics
                'attempts_used': attempts_used,
                'transcript_length': len(conv['transcript']),
                'response_length': len(response_text),
                'total_latency': round(total_time, 3),
            }
            
            return result
            
        except Exception as e:
            return {
                'conversation_id': conv['id'],
                'data_type': data_type,
                'parameter_tested': test_type.upper(),
                'parameter_name': test_type.replace('_', ' ').title(),
                'model_name': self.model_name,
                'timestamp': datetime.now().isoformat(),
                'temperature': self.temperature,
                'max_output_tokens': self.max_output_tokens,
                'success': False,
                'result_value': 'Error',
                'evidence': str(e),
                'error': str(e),
                'attempts_used': 0,
                'total_latency': 0,
                'transcript_length': len(conv['transcript']),
                'response_length': 0
            }
    
    def test_data_type(self, data_type: str, test_type: str, 
                       max_conversations: int = None) -> Optional[str]:
        """
        Test Gemini on a specific data type
        
        Args:
            data_type: 'type1', 'type2a', or 'type2b'
            test_type: Assessment type (opening, closing, etc.)
            max_conversations: Max conversations to test
            
        Returns:
            Path to results file or None
        """
        print(f"\n{'='*70}")
        print(f"🧪 Testing Gemini | Data: {data_type} | Guideline: {test_type}")
        print(f"{'='*70}")
        
        # Load data
        print(f"📂 Loading {data_type} data...")
        conversations = self.data_loader.get_data_by_type(data_type, max_conversations)
        if not conversations:
            print(f"❌ No data loaded for {data_type}")
            return None
        
        print(f"✅ Loaded {len(conversations)} conversations")
        print(f"📊 Starting conversation testing...")
        print(f"{'='*70}\n")
        
        # Run tests
        results = []
        successful_tests = 0
        failed_tests = 0
        
        for i, conv in enumerate(conversations):
            print(f"\n   ╔{'='*66}╗")
            print(f"   ║  Test [{i+1}/{len(conversations)}]" + " " * (66 - len(f"  Test [{i+1}/{len(conversations)}]")) + "║")
            print(f"   ╚{'='*66}╝")
            
            result = self.test_single_conversation(conv, test_type, data_type)
            results.append(result)
            
            # Print result summary
            print(f"\n      📊 RESULT:")
            if result['success']:
                print(f"      ✅ Status: SUCCESS")
                print(f"      🎯 Value: {result['result_value']}")
                print(f"      🔄 Attempts: {result.get('attempts_used', 1)}")
                print(f"      ⏱️  Latency: {result.get('total_latency', 0):.2f}s")
                successful_tests += 1
            else:
                print(f"      ❌ Status: FAILED")
                print(f"      💥 Error: {result.get('evidence', 'Unknown error')}")
                failed_tests += 1
            
            print(f"\n      📈 Progress: {successful_tests} passed, {failed_tests} failed, {len(conversations) - i - 1} remaining")
            
            # Rate limiting - 1 second between conversations
            if i < len(conversations) - 1:
                print(f"      ⏸️  Sleeping 1s before next test...")
                time.sleep(1)
        
        # Save results
        print(f"\n{'='*70}")
        print(f"💾 SAVING RESULTS")
        print(f"{'='*70}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_dir = os.path.join(self.results_base_dir, data_type)
        
        print(f"📁 Creating directory: {results_dir}")
        os.makedirs(results_dir, exist_ok=True)
        
        filename = f"{test_type}_results_{timestamp}.csv"
        filepath = os.path.join(results_dir, filename)
        
        print(f"📝 Converting {len(results)} results to DataFrame...")
        df = pd.DataFrame(results)
        
        print(f"💾 Writing to CSV: {filepath}")
        df.to_csv(filepath, index=False)
        print(f"✅ File saved successfully!")
        
        # Print summary
        self._print_summary(results, data_type, test_type)
        
        print(f"\n{'='*70}")
        print(f"✅ TEST BATCH COMPLETE!")
        print(f"{'='*70}")
        print(f"📂 Results location: {filepath}")
        print(f"{'='*70}\n")
        
        return filepath
    
    def _print_summary(self, results: List[Dict], data_type: str, test_type: str):
        """Print test summary"""
        print(f"\n{'='*70}")
        print(f"📊 SUMMARY: Gemini | {data_type} | {test_type}")
        print(f"{'='*70}")
        
        total = len(results)
        successful = sum(1 for r in results if r['success'])
        met = sum(1 for r in results if r.get('result_value') == 'Met')
        not_met = sum(1 for r in results if r.get('result_value') == 'Not Met')
        
        print(f"Total conversations: {total}")
        print(f"Successful calls: {successful}/{total} ({(successful/total)*100:.1f}%)")
        print(f"Results - Met: {met}, Not Met: {not_met}")
        
        # Retry statistics
        total_attempts = sum(r.get('attempts_used', 1) for r in results)
        avg_attempts = total_attempts / total if total > 0 else 0
        max_attempts = max((r.get('attempts_used', 1) for r in results), default=1)
        
        print(f"\nRetry Stats:")
        print(f"  Average attempts: {avg_attempts:.2f}")
        print(f"  Max attempts needed: {max_attempts}")
        print(f"  Total API calls: {total_attempts}")
        
        # Latency stats
        latencies = [r.get('total_latency', 0) for r in results if r['success']]
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            print(f"\nLatency Stats:")
            print(f"  Average: {avg_latency:.3f}s")
            print(f"  Min: {min_latency:.3f}s")
            print(f"  Max: {max_latency:.3f}s")


def main():
    """Main function to run comprehensive Gemini tests"""
    print("\n" + "="*70)
    print("="*70)
    print("🚀 GEMINI API COMPREHENSIVE TEST")
    print("="*70)
    print("="*70)
    
    # Initialize runner
    runner = GeminiTestRunner()
    
    # Initialize Gemini
    print("\n🔧 Initializing Gemini API...")
    if not runner.initialize_gemini():
        print("\n❌ Failed to initialize Gemini API")
        print("   Please check GEMINI_ENV_SETUP.txt for setup instructions")
        return
    
    # All data types
    data_types = ['type1', 'type2a', 'type2b']
    
    # All parameters/guidelines
    all_parameters = list(ASSESSMENT_PROMPTS.keys())
    
    max_conversations = 20  # Default, can be changed
    
    total_tests = len(data_types) * len(all_parameters)
    current_test = 0
    
    print("\n📋 TEST CONFIGURATION:")
    print("="*70)
    print(f"  🤖 Model: {runner.model_name}")
    print(f"  🌡️  Temperature: {runner.temperature}")
    print(f"  📝 Max Output Tokens: {runner.max_output_tokens}")
    print(f"  🔄 Retry Strategy: {runner.max_retries} attempts with exponential backoff")
    print(f"  📂 Data Types: {', '.join(data_types)}")
    print(f"  🔍 Guidelines to test:")
    for i, param in enumerate(all_parameters, 1):
        print(f"      {i}. {param.replace('_', ' ').title()}")
    print(f"  💬 Conversations per test: {max_conversations}")
    print(f"  🎯 Total tests: {total_tests} ({len(data_types)} types × {len(all_parameters)} guidelines)")
    print("="*70)
    
    print("\n⚠️  IMPORTANT NOTES:")
    print("  • Using Gemini Free Tier with retry logic")
    print("  • Each conversation will retry up to 5 times if it fails")
    print("  • Exponential backoff: 2s → 4s → 8s → 16s → 32s")
    print("  • 1 second delay between conversations")
    print("  • 2 second delay between test batches")
    print("="*70)
    
    print("\n🚀 STARTING TESTS...")
    print("="*70)
    
    start_time = time.time()
    
    for data_type in data_types:
        print(f"\n{'#'*70}")
        print(f"{'#'*70}")
        print(f"###  DATA TYPE: {data_type.upper()}")
        print(f"{'#'*70}")
        print(f"{'#'*70}\n")
        
        for parameter in all_parameters:
            current_test += 1
            
            elapsed_time = time.time() - start_time
            avg_time_per_test = elapsed_time / current_test if current_test > 1 else 0
            estimated_remaining = avg_time_per_test * (total_tests - current_test)
            
            print(f"\n{'='*70}")
            print(f"{'='*70}")
            print(f"   🎯 TEST {current_test}/{total_tests}")
            print(f"{'='*70}")
            print(f"   📊 Model: Gemini")
            print(f"   📂 Data Type: {data_type}")
            print(f"   🔍 Guideline: {parameter.replace('_', ' ').title()}")
            print(f"   📈 Progress: {(current_test/total_tests)*100:.1f}%")
            if current_test > 1:
                print(f"   ⏱️  Elapsed: {elapsed_time/60:.1f} min")
                print(f"   ⏳ Est. Remaining: {estimated_remaining/60:.1f} min")
            print(f"{'='*70}")
            print(f"{'='*70}\n")
            
            try:
                test_start = time.time()
                runner.test_data_type(
                    data_type=data_type,
                    test_type=parameter,
                    max_conversations=max_conversations
                )
                test_duration = time.time() - test_start
                
                print(f"\n{'='*70}")
                print(f"✅ TEST {current_test}/{total_tests} COMPLETED!")
                print(f"   Duration: {test_duration/60:.1f} minutes")
                print(f"{'='*70}\n")
                
            except Exception as e:
                print(f"\n{'='*70}")
                print(f"❌ TEST {current_test}/{total_tests} FAILED!")
                print(f"   Error: {e}")
                print(f"{'='*70}")
                import traceback
                traceback.print_exc()
            
            # Small delay between tests
            if current_test < total_tests:
                print(f"⏸️  Pausing 2 seconds before next test...\n")
                time.sleep(2)
    
    end_time = time.time()
    total_minutes = (end_time - start_time) / 60
    
    print("\n" + "="*70)
    print("="*70)
    print("🎉 ALL GEMINI TESTS COMPLETED!")
    print("="*70)
    print("="*70)
    
    print(f"\n📊 FINAL SUMMARY:")
    print("="*70)
    print(f"  ✅ Tests completed: {current_test}/{total_tests}")
    print(f"  ⏱️  Total time: {total_minutes:.1f} minutes ({total_minutes/60:.2f} hours)")
    print(f"  ⚡ Average time per test: {total_minutes/total_tests:.2f} minutes")
    print("="*70)
    
    print(f"\n📁 RESULTS LOCATION:")
    print("="*70)
    print(f"  Base directory: gemini_results/")
    print(f"\n  Detailed results by data type:")
    for dtype in data_types:
        print(f"    📂 {dtype}:")
        print(f"    Location: gemini_results/{dtype}/")
        print()
    print("="*70)
    
    print("\n✨ ALL DONE! ✨\n")


if __name__ == "__main__":
    main()

