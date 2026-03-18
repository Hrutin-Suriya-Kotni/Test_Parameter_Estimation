#!/usr/bin/env python3
"""
Gemini 2.0 Flash Testing Script for Important Prompts (20 Conversations Type2b)
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
from Important_prompts import APOLOGY_PROMPT, EMPATHY_PROMPT, FEEDBACK_PITCH_PROMPT, RUDE_SARCASTIC_PROMPT

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
REQUEST_DELAY = 80  # 80 seconds between requests
QUOTA_RETRY_CYCLES = 2  # Try all keys twice before waiting
QUOTA_WAIT_TIME = 900  # 15 minutes wait when all keys exhausted

# Multiple API keys for round-robin (6 fresh keys for better distribution)
API_KEYS = [
    "AIzaSyB4hXmT6VM4rreMIZMFa1sGY7uZZaG7fgY",
    "AIzaSyDy5Xnnt5VaEPonlDVFrDTi6o6pZwu_FU8",
    "AIzaSyB0jT33UWNk9xmSC0Gu6a6-MgusvnD0qj8",
    "AIzaSyC-J1Llfj-NSsDYyi6HKt0M4ohi60jCQDw",
    "AIzaSyDcJnliwEmP9ciutn0sQkm2pywY46QCzss",
    "AIzaSyBHInm_Y1nfx5Q-2upl_2PgdQEvZSAI6ao"
]

if GEMINI_AVAILABLE:
    genai.configure(api_key=API_KEYS[0])

class GeminiImportantTester:
    def __init__(self):
        if not GEMINI_AVAILABLE:
            print("❌ Gemini API not available")
            sys.exit(1)

        print("🚀 Initializing Gemini 2.0 Flash (Multi-Key Round-Robin)...")
        print(f"   📝 Using {len(API_KEYS)} API keys in rotation")
        self.models = [genai.GenerativeModel(MODEL_NAME) for _ in API_KEYS]
        self.current_key_idx = 0
        self.requests_on_current_key = 0

        # Initialize output paths early
        output_dir = Path(__file__).parent / 'results'
        output_dir.mkdir(exist_ok=True)
        self.results_file = output_dir / 'gemini_results_20_important_parameters.json'

        # Load existing results if file exists
        self.results = []
        self.stats = {'total_tests': 0, 'successful': 0, 'failed': 0, 'parse_errors': 0}
        if self.results_file.exists():
            try:
                with open(self.results_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                self.results = existing_data.get('results', [])
                print(f"   📂 Loaded {len(self.results)} existing results")
            except Exception as e:
                print(f"   ⚠️ Could not load existing results: {e}")

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
    
    def _extract_fields(self, guideline: str, parsed: dict):
        if guideline == 'apology':
            res = parsed.get('Apology_result') or parsed.get('apology_result') or parsed.get('Value')
            ev = parsed.get('Apology_evidence') or parsed.get('apology_evidence') or parsed.get('Evidence')
            cat = parsed.get('Apology_Category') or parsed.get('apology_category')
            return res, ev, cat
        if guideline == 'empathy':
            res = parsed.get('Empathy_result') or parsed.get('empathy_result') or parsed.get('Value')
            ev = parsed.get('Empathy_evidence') or parsed.get('empathy_evidence') or parsed.get('Evidence')
            cat = parsed.get('Empathy_Category') or parsed.get('empathy_category')
            return res, ev, cat
        if guideline == 'feedback_pitch':
            return parsed.get('Category'), parsed.get('Supporting_Evidence'), parsed.get('Summary')
        if guideline == 'rude_sarcastic':
            res = parsed.get('Sarcasm_rude_behaviour') or parsed.get('Value')
            ev = parsed.get('Sarcasm_rude_behaviour_evidence') or parsed.get('Evidence')
            return res, ev, None
        return None, None, None
    
    def _normalize_status(self, guideline: str, value: str) -> str:
        v = (value or '').strip().lower()
        if guideline == 'feedback_pitch':
            return 'met' if v else 'not met'  # Categories are met if present
        return 'met' if v == 'met' else 'not met'
    
    def make_request(self, prompt, conversation_text, guideline, conversation_id):
        # Aggressive quota handling: try all keys multiple times, wait if all exhausted
        total_keys = len(API_KEYS)
        max_attempts_per_cycle = total_keys * QUOTA_RETRY_CYCLES  # 12 attempts (6 keys × 2 cycles)
        max_wait_cycles = 5  # Maximum 5 wait cycles

        global_attempt = 0
        wait_cycles = 0

        while global_attempt < max_attempts_per_cycle * (max_wait_cycles + 1):
            # Calculate which key to use in the cycle
            key_index = global_attempt % total_keys
            cycle_in_round = global_attempt // total_keys

            # If we've completed full cycles of all keys, wait before trying again
            if global_attempt > 0 and global_attempt % max_attempts_per_cycle == 0 and wait_cycles < max_wait_cycles:
                print(f"   ⏱️ All keys exhausted for {QUOTA_RETRY_CYCLES} cycles. Waiting {QUOTA_WAIT_TIME//60} minutes...")
                time.sleep(QUOTA_WAIT_TIME)
                wait_cycles += 1
                print(f"   🔄 Starting fresh cycle after wait...")
                global_attempt = 0  # Reset attempt counter for new cycle
                continue

            # Switch to the appropriate key
            self.current_key_idx = key_index
            self.refresh_model()

            try:
                print(f"   🔑 Trying API key {key_index + 1}/{total_keys} (attempt {global_attempt + 1})")

                start_time = time.time()

                # Prepare the full prompt
                full_prompt = f"{prompt}\n\nTranscript:\n{conversation_text}\n\nRespond with JSON only."

                # Get current model (will use the switched key)
                current_model = self.get_current_model()

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

                    value, evidence, category = self._extract_fields(guideline, parsed_response)
                    status = self._normalize_status(guideline, value)

                    self.stats['successful'] += 1
                    parse_error = False

                except json.JSONDecodeError:
                    status = 'Parse Error'
                    value = 'Parse Error'
                    evidence = content
                    category = None
                    self.stats['parse_errors'] += 1
                    parse_error = True

                # Only store successful responses
                if not parse_error:
                    result = {
                        'conversation_id': conversation_id,
                        'guideline': guideline,
                        'data_type': 'type2b',
                        'status': status,
                        'value': value,
                        'evidence': evidence,
                        'category': category,
                        'response': content,
                        'duration': duration,
                        'attempt': global_attempt + 1,
                        'success': True,
                        'parse_error': parse_error
                    }

                    self.results.append(result)
                    self.save_results()  # Save after each success
                    print(f"   💾 Saved result for {conversation_id[:8]} after {global_attempt + 1} attempts")

                    # Reset counters for successful request
                    self.requests_on_current_key += 1
                    self.rotate_key_if_needed()

                    return result

                # If parse error, continue trying next key
                print(f"   ⚠️ Parse error, trying next key...")
                global_attempt += 1
                continue

            except Exception as e:
                error_msg = str(e).lower()
                print(f"   ⚠️  Error on attempt {global_attempt + 1}: {str(e)[:100]}")

                # Check if it's a quota/rate limit error
                is_quota_error = any(keyword in error_msg for keyword in ['rate limit', 'quota', 'exceeded', 'too many requests'])

                if is_quota_error:
                    print(f"   🚫 Quota exceeded on key {key_index + 1}, switching to next key...")
                    global_attempt += 1
                    continue  # Try next key immediately
                else:
                    # Non-quota error, wait a bit and continue
                    print(f"   ⏳ Non-quota error, waiting {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)
                    global_attempt += 1
                    continue

        # If we get here, all attempts failed
        print(f"   ❌ Failed to get result after maximum attempts")
        self.stats['failed'] += 1
        return None
    
    def save_results(self):
        """Save results to JSON file"""
        data = {
            'model': MODEL_NAME,
            'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'total_tests': len(self.results),
            'stats': self.stats,
            'results': self.results
        }
        with open(self.results_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def save_partial_results(self):
        """Save current results in case of interruption"""
        self.save_results()
    
    def test_conversations(self, data_path: str, guideline: str):
        with open(data_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            conversations = list(reader)

        print(f"Loaded {len(conversations)} conversations")

        prompts = {
            'apology': APOLOGY_PROMPT,
            'empathy': EMPATHY_PROMPT,
            'feedback_pitch': FEEDBACK_PITCH_PROMPT,
            'rude_sarcastic': RUDE_SARCASTIC_PROMPT
        }

        for i, row in enumerate(conversations, 1):
            conv_id = row['conversation_id']
            txt = row['transcript']
            print(f"📝 Testing conversation {i}/20: {conv_id[:8]}...")

            res = self.make_request(prompts[guideline], txt, guideline, conv_id)
            if res:
                print(f"   ✓ Response: {res['status']} ({res['duration']:.2f}s)")
            else:
                print(f"   ✗ Response: Failed - not saved")
                # If a request completely fails after all retries, add a small delay
                time.sleep(10)

        self.stats['total_tests'] = len(self.results)

    def test_single_conversation(self, data_path: str, guideline: str, conv_id_short: str):
        with open(data_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            conversations = list(reader)

        # Find the specific conversation
        target_row = None
        for row in conversations:
            if row['conversation_id'].startswith(conv_id_short):
                target_row = row
                break

        if not target_row:
            print(f"❌ Conversation {conv_id_short} not found in data")
            return

        conv_id = target_row['conversation_id']
        txt = target_row['transcript']

        prompts = {
            'apology': APOLOGY_PROMPT,
            'empathy': EMPATHY_PROMPT,
            'feedback_pitch': FEEDBACK_PITCH_PROMPT,
            'rude_sarcastic': RUDE_SARCASTIC_PROMPT
        }

        print(f"📝 Testing conversation: {conv_id[:8]}...")

        res = self.make_request(prompts[guideline], txt, guideline, conv_id)
        if res:
            print(f"   ✓ Response: {res['status']} ({res['duration']:.2f}s)")
        else:
            print(f"   ✗ Response: Failed - not saved")

        # Small delay between tests
        print(f"   ⏱️  Waiting {REQUEST_DELAY} seconds before next request...")
        time.sleep(REQUEST_DELAY)

def main():
    print("🚀 Running All Gemini Important Tests (80 total) - Aggressive Quota Mode")
    print("=" * 60)
    print(f"Model: {MODEL_NAME}")
    print(f"Request Delay: {REQUEST_DELAY} seconds between tests")
    print("Aggressive quota handling: tries all 6 keys × 2 cycles, waits 15 min if exhausted")
    print("Will get ALL results eventually - no failures allowed!")
    print("Will resume from existing results if any")
    print("=" * 60)

    data_path = Path(__file__).parent / 'DATA' / 'type2b_20_conversations.csv'

    # Run all 80 tests in small batches to avoid quota limits
    # First load all actual conversation IDs
    with open(data_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        conversations = list(reader)

    all_tests = []
    guidelines = ['apology', 'empathy', 'feedback_pitch', 'rude_sarcastic']
    for g in guidelines:
        for row in conversations:
            conv_id_short = row['conversation_id'][:8]  # First 8 chars
            all_tests.append((g, conv_id_short))

    tester = GeminiImportantTester()

    batch_size = 1  # Run 1 test at a time to be very conservative
    for i in range(0, len(all_tests), batch_size):
        batch = all_tests[i:i + batch_size]
        print(f"\n{'='*60}")
        print(f"Running batch {i//batch_size + 1}/80 ({len(batch)} test)")
        print('='*60)

        for guideline, conv_id_short in batch:
            print(f"Testing: {guideline.upper()} - {conv_id_short}")
            tester.test_single_conversation(str(data_path), guideline, conv_id_short)

        # Delay is handled in test_single_conversation

    print(f"\n{'='*60}")
    print("FULL TEST SUMMARY")
    print('='*60)
    print(f"Total Tests Completed: {tester.stats['total_tests']}")
    print(f"Successful: {tester.stats['successful']}")
    print(f"Failed: {tester.stats['failed']}")
    print(f"Parse Errors: {tester.stats['parse_errors']}")

    # Load and show final total
    try:
        with open(tester.results_file, 'r', encoding='utf-8') as f:
            final_data = json.load(f)
        final_count = len(final_data['results'])
        print(f"\n📊 FINAL TOTAL: {final_count}/80 tests completed")
        if final_count == 80:
            print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        else:
            print(f"⚠️  {80 - final_count} tests still missing. Can resume later.")
    except Exception as e:
        print(f"\n⚠️ Could not load final results: {e}")

if __name__ == "__main__":
    main()