#!/usr/bin/env python3
"""
OpenChat-3.5-1210 testing for 20 conversations with Important prompts
Runs 4 separate guidelines: Apology, Empathy, Feedback Pitch, Rude/Sarcastic
Saves results with `_important_parameters` suffix.
"""

import sys
import json
import csv
import time
import requests
from pathlib import Path
from datetime import datetime
from transformers import AutoTokenizer
import re

# Add project root to path to import prompts modules
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from Important_prompts import (
    APOLOGY_PROMPT,
    EMPATHY_PROMPT,
    FEEDBACK_PITCH_PROMPT,
    RUDE_SARCASTIC_PROMPT,
)


SERVER_URL = "http://27.111.72.51:3333/v1/chat/completions"
MODEL_NAME = "openchat/openchat-3.5-1210"
TOKEN_LIMIT = 8100
MAX_RETRIES = 3
RETRY_DELAY = 2


GUIDELINES = {
    'apology': APOLOGY_PROMPT,
    'empathy': EMPATHY_PROMPT,
    'feedback_pitch': FEEDBACK_PITCH_PROMPT,
    'rude_sarcastic': RUDE_SARCASTIC_PROMPT,
}


class OpenChatImportantTester:
    def __init__(self):
        print("🚀 Loading tokenizer...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
        except Exception as e:
            print(f"⚠️  Error loading tokenizer: {e}")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "sentencepiece", "protobuf"])
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)

        self.results = []
        self.stats = {
            'total_tests': 0,
            'successful': 0,
            'failed': 0,
            'token_limit_exceeded': 0
        }

    def count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))

    def validate_token_limit(self, prompt: str, conversation: str):
        prompt_tokens = self.count_tokens(prompt)
        conv_tokens = self.count_tokens(conversation)
        total_tokens = prompt_tokens + conv_tokens + 500  # buffer for output
        return total_tokens, total_tokens <= TOKEN_LIMIT

    @staticmethod
    def _clean_response(content: str) -> str:
        cleaned = content.strip()
        if cleaned.startswith('```json'):
            cleaned = cleaned[7:]
        if cleaned.startswith('```'):
            cleaned = cleaned[3:]
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]
        return cleaned.strip()

    @staticmethod
    def _try_parse_with_fixes(text: str):
        """Attempt to parse near-JSON by applying small fixes."""
        s = text.strip()
        # Extract JSON substring if possible
        if '{' in s and '}' in s:
            s = s[s.find('{'):s.rfind('}')+1]
        # Common key truncation fix
        s = re.sub(r'"Supporting_Evi\w*"', '"Supporting_Evidence"', s)
        # Remove trailing commas before } or ]
        s = re.sub(r',\s*([}\]])', r'\1', s)
        # If still not valid JSON-like, build from key: value lines
        try:
            return json.loads(s)
        except Exception:
            pass
        # Fallback: parse lines like Key: Value
        keys = [
            'Apology_result','Apology_evidence','Apology_Category',
            'Empathy_result','Empathy_evidence','Empathy_Category',
            'Category','Summary','Supporting_Evidence',
            'Sarcasm_rude_behaviour','Sarcasm_rude_behaviour_evidence'
        ]
        result = {}
        for k in keys:
            m = re.search(rf'\b{k}\s*:\s*(.+)', text)
            if m:
                val = m.group(1).strip()
                # stop at next key if multiple on same line
                val = re.split(r'\b(' + '|'.join(map(re.escape, keys)) + r')\s*:', val)[0].strip()
                # trim surrounding quotes if present
                if len(val) >= 2 and ((val[0]==val[-1]=="\"") or (val[0]==val[-1]=="'")):
                    val = val[1:-1]
                result[k] = val
        return result if result else None

    @staticmethod
    def _extract_fields(guideline: str, parsed: dict):
        """Map guideline-specific fields into a common structure."""
        if guideline == 'apology':
            value = parsed.get('Apology_result') or parsed.get('apology_result')
            evidence = parsed.get('Apology_evidence') or parsed.get('apology_evidence')
            category = parsed.get('Apology_Category') or parsed.get('apology_category')
            return value, evidence, category
        if guideline == 'empathy':
            value = parsed.get('Empathy_result') or parsed.get('empathy_result')
            evidence = parsed.get('Empathy_evidence') or parsed.get('empathy_evidence')
            category = parsed.get('Empathy_Category') or parsed.get('empathy_category')
            return value, evidence, category
        if guideline == 'feedback_pitch':
            value = parsed.get('Category') or parsed.get('category')
            evidence = parsed.get('Supporting_Evidence') or parsed.get('supporting_evidence')
            category = parsed.get('Summary') or parsed.get('summary')
            return value, evidence, category
        if guideline == 'rude_sarcastic':
            value = parsed.get('Sarcasm_rude_behaviour') or parsed.get('sarcasm_rude_behaviour')
            evidence = parsed.get('Sarcasm_rude_behaviour_evidence') or parsed.get('sarcasm_rude_behaviour_evidence')
            return value, evidence, None
        return None, None, None

    def make_request(self, prompt: str, conversation_text: str, guideline: str, conversation_id: str):
        total_tokens, is_valid = self.validate_token_limit(prompt, conversation_text)
        if not is_valid:
            print(f"   ⚠️  Token limit exceeded: {total_tokens} tokens (limit: {TOKEN_LIMIT})")
            self.stats['token_limit_exceeded'] += 1
            return {
                'conversation_id': conversation_id,
                'guideline': guideline,
                'data_type': 'type2b',
                'status': 'Exceeded',
                'value': 'Exceeded',
                'evidence': '',
                'category': None,
                'response': '',
                'duration': 0,
                'attempt': 0,
                'success': False,
            }

        messages = [
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': conversation_text},
        ]

        payload = {
            'model': MODEL_NAME,
            'messages': messages,
            'max_tokens': 700,
            'temperature': 0.1,
        }

        for attempt in range(MAX_RETRIES):
            try:
                start_time = time.time()
                resp = requests.post(SERVER_URL, json=payload, timeout=45)
                duration = time.time() - start_time
                data = resp.json()

                if 'error' in data:
                    raise Exception(data['error'].get('message', 'Unknown API error'))
                if 'choices' not in data or not data['choices']:
                    raise Exception(f"Invalid response structure: {list(data.keys())}")

                content = data['choices'][0]['message']['content']

                try:
                    cleaned = self._clean_response(content)
                    parsed = json.loads(cleaned)
                    value, evidence, category = self._extract_fields(guideline, parsed)
                    # Normalize status to align with existing results format
                    if guideline in ('apology', 'empathy', 'rude_sarcastic'):
                        val_norm = (value or '').strip().lower()
                        status = 'met' if val_norm == 'met' else 'not met'
                    elif guideline == 'feedback_pitch':
                        # Treat customer agreed to feedback as Met; everything else Not Met
                        cat_norm = (value or '').strip().lower()
                        status = 'met' if 'customer agreed to give feedback' in cat_norm else 'not met'
                    else:
                        status = 'met' if (value or '').strip().lower() == 'met' else 'not met'
                except json.JSONDecodeError:
                    # Try to repair
                    repaired = self._try_parse_with_fixes(content)
                    if isinstance(repaired, dict) and repaired:
                        value, evidence, category = self._extract_fields(guideline, repaired)
                        if guideline in ('apology', 'empathy', 'rude_sarcastic'):
                            val_norm = (value or '').strip().lower()
                            status = 'met' if val_norm == 'met' else 'not met'
                        elif guideline == 'feedback_pitch':
                            cat_norm = (value or '').strip().lower()
                            status = 'met' if 'customer agreed to give feedback' in cat_norm else 'not met'
                        else:
                            status = 'met' if (value or '').strip().lower() == 'met' else 'not met'
                    else:
                        status = 'Parse Error'
                        value, evidence, category = None, None, None

                return {
                    'conversation_id': conversation_id,
                    'guideline': guideline,
                    'data_type': 'type2b',
                    'status': status,
                    'value': value,
                    'evidence': evidence,
                    'category': category,
                    'response': content,
                    'duration': duration,
                    'attempt': attempt + 1,
                    'success': status not in ('Parse Error', 'Failed', 'Exceeded'),
                }

            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                    continue
                return {
                    'conversation_id': conversation_id,
                    'guideline': guideline,
                    'data_type': 'type2b',
                    'status': 'Failed',
                    'value': None,
                    'evidence': None,
                    'category': None,
                    'response': str(e),
                    'duration': 0,
                    'attempt': attempt + 1,
                    'success': False,
                }

    def test_conversations(self, data_path: str, guideline: str):
        print(f"\n{'='*60}")
        print(f"Testing Important Guideline: {guideline.upper()}")
        print('='*60)

        conversations = []
        with open(data_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                conversations.append(row)

        print(f"Loaded {len(conversations)} conversations")

        prompt = GUIDELINES[guideline]

        for idx, row in enumerate(conversations, 1):
            conversation_id = row.get('conversation_id', '')
            conversation_text = row.get('transcript', '')

            print(f"\n📝 Testing conversation {idx}/{len(conversations)}: {conversation_id[:8]}...")

            total_tokens, is_valid = self.validate_token_limit(prompt, conversation_text)
            if is_valid:
                print(f"   ✓ Token check passed: {total_tokens} tokens")
            else:
                print(f"   ⚠️  Token limit exceeded: {total_tokens} tokens")

            print(f"   🔄 Sending request to {SERVER_URL}...")
            result = self.make_request(prompt, conversation_text, guideline, conversation_id)
            self.results.append(result)
            self.stats['total_tests'] += 1
            if result['success']:
                self.stats['successful'] += 1
            else:
                self.stats['failed'] += 1

            icon = '✓' if result['success'] else '✗'
            print(f"   {icon} Response: {result['status']} ({result['duration']:.2f}s)")

    def save_results(self, output_path: str):
        output_data = {
            'model': MODEL_NAME,
            'server': SERVER_URL,
            'timestamp': datetime.now().isoformat(),
            'total_tests': len(self.results),
            'stats': self.stats,
            'results': self.results,
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Results saved to: {output_path}")
        return output_path


def main():
    print("🚀 Starting OpenChat-3.5-1210 Important Prompts Test (20 Conversations)")
    print("="*60)
    print("Server: 27.111.72.51:3333")
    print(f"Model: {MODEL_NAME}")
    print("="*60)

    tester = OpenChatImportantTester()
    data_path = Path(__file__).parent / 'DATA' / 'type2b_20_conversations.csv'

    for guideline in ['apology', 'empathy', 'feedback_pitch', 'rude_sarcastic']:
        tester.test_conversations(str(data_path), guideline)

    # Save results with the required suffix
    output_dir = Path(__file__).parent / 'results'
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # file_ts = output_dir / f'openchat_results_20_convo_{timestamp}_important_parameters.json'
    file_simple = output_dir / 'openchat_results_20_important_parameters.json'
    # tester.save_results(str(file_ts))
    tester.save_results(str(file_simple))

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


