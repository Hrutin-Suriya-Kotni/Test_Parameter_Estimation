#!/usr/bin/env python3
"""
Mistral CRED Tuned - 20 conversations, Important prompts (4 guidelines)
Saves to results/mistral_cred_tuned_results_important_parameters.json
"""

import sys
import json
import csv
import time
import requests
from pathlib import Path
from datetime import datetime
import re

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from Important_prompts import (
    APOLOGY_PROMPT,
    EMPATHY_PROMPT,
    FEEDBACK_PITCH_PROMPT,
    RUDE_SARCASTIC_PROMPT,
)

SERVER_URL = "http://27.111.72.51:8000/generate"
MODEL_NAME = "mistral_cred_tuned"
MAX_RETRIES = 3
RETRY_DELAY = 2
MAX_NEW_TOKENS = 700
TEMPERATURE = 0.1

GUIDELINES = {
    'apology': APOLOGY_PROMPT,
    'empathy': EMPATHY_PROMPT,
    'feedback_pitch': FEEDBACK_PITCH_PROMPT,
    'rude_sarcastic': RUDE_SARCASTIC_PROMPT,
}


class MistralCredImportantTester:
    def __init__(self):
        self.results = []
        self.stats = {'total_tests': 0, 'successful': 0, 'failed': 0, 'token_limit_exceeded': 0}

    @staticmethod
    def _json_template(guideline: str) -> str:
        return '{"Value":"Met or Not Met","Evidence":"..."}'

    @staticmethod
    def _build_prompt(task_prompt: str, conversation_text: str, guideline: str) -> str:
        json_rule = (
            "CRITICAL: Return ONLY a valid JSON object. No extra text or code fences. "
            "Use double quotes and valid JSON syntax. Begin JSON now:")
        template = MistralCredImportantTester._json_template(guideline)
        return (
            f"{json_rule}\n{template}\n\n"
            f"{task_prompt}\n\nTranscript:\n{conversation_text.strip()}"
        )

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
    def _extract_last_json(text: str):
        s = text
        candidates = []
        stack = []
        start = None
        for i,ch in enumerate(s):
            if ch == '{':
                if not stack:
                    start = i
                stack.append('{')
            elif ch == '}' and stack:
                stack.pop()
                if not stack and start is not None:
                    candidates.append(s[start:i+1])
                    start = None
        for cand in reversed(candidates):
            try:
                return json.loads(cand)
            except Exception:
                continue
        return None


    @staticmethod
    def _extract_fields(guideline: str, parsed: dict):
        if guideline == 'apology':
            # Preferred keys for important prompt
            res = parsed.get('Apology_result') or parsed.get('apology_result')
            ev = parsed.get('Apology_evidence') or parsed.get('apology_evidence')
            cat = parsed.get('Apology_Category') or parsed.get('apology_category')
            # Fallback to generic Value/Evidence if model emits that
            if not res and 'Value' in parsed:
                res = parsed.get('Value')
                ev = ev or parsed.get('Evidence')
            return res, ev, cat
        if guideline == 'empathy':
            res = parsed.get('Empathy_result') or parsed.get('empathy_result')
            ev = parsed.get('Empathy_evidence') or parsed.get('empathy_evidence')
            cat = parsed.get('Empathy_Category') or parsed.get('empathy_category')
            if not res and 'Value' in parsed:
                res = parsed.get('Value')
                ev = ev or parsed.get('Evidence')
            return res, ev, cat
        if guideline == 'feedback_pitch':
            return parsed.get('Category'), parsed.get('Supporting_Evidence'), parsed.get('Summary')
        if guideline == 'rude_sarcastic':
            return parsed.get('Sarcasm_rude_behaviour'), parsed.get('Sarcasm_rude_behaviour_evidence'), None
        return None, None, None

    def _normalize_status(self, guideline: str, value: str) -> str:
        v = (value or '').strip().lower()
        if guideline in ('apology', 'empathy', 'rude_sarcastic'):
            return 'met' if v == 'met' else 'not met'
        if guideline == 'feedback_pitch':
            return 'met' if 'customer agreed to give feedback' in v else 'not met'
        return 'not met'

    def make_request(self, prompt: str, conversation_text: str, guideline: str, conversation_id: str):
        payload = {
            'prompt': self._build_prompt(prompt, conversation_text, guideline),
            'max_new_tokens': MAX_NEW_TOKENS,
            'temperature': TEMPERATURE,
        }

        for attempt in range(MAX_RETRIES):
            try:
                start = time.time()
                resp = requests.post(SERVER_URL, json=payload, timeout=60)
                dur = time.time() - start
                data = resp.json()
                content = (data.get('text') or data.get('generated_text') or 
                           data.get('content') or data.get('response') or '')

                try:
                    cleaned = self._clean_response(content)
                    parsed = self._extract_last_json(cleaned)
                    if parsed is None:
                        raise ValueError('No JSON found')
                    value, evidence, category = self._extract_fields(guideline, parsed)
                    status = self._normalize_status(guideline, value)
                except Exception:
                    value, evidence, category = None, None, None
                    status = 'Parse Error'

                return {
                    'conversation_id': conversation_id,
                    'guideline': guideline,
                    'data_type': 'type2b',
                    'status': status,
                    'value': value,
                    'evidence': evidence,
                    'category': category,
                    'response': content,
                    'duration': dur,
                    'attempt': attempt + 1,
                    'success': status not in ('Parse Error', 'Failed', 'Exceeded')
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
                    'success': False
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
        task_prompt = GUIDELINES[guideline]

        for idx, row in enumerate(conversations, 1):
            conv_id = row.get('conversation_id', '')
            txt = row.get('transcript', '')
            print(f"\n📝 Testing conversation {idx}/{len(conversations)}: {conv_id[:8]}...")
            print(f"   🔄 Sending request to {SERVER_URL}...")
            res = self.make_request(task_prompt, txt, guideline, conv_id)
            self.results.append(res)
            self.stats['total_tests'] += 1
            if res['success']:
                self.stats['successful'] += 1
                print(f"   ✓ Response: {res['status']} ({res['duration']:.2f}s)")
            else:
                self.stats['failed'] += 1
                print(f"   ✗ Response: {res['status']} ({res['duration']:.2f}s)")

    def save_results(self, output_path: str):
        output = {
            'model': MODEL_NAME,
            'server': SERVER_URL,
            'timestamp': datetime.now().isoformat(),
            'total_tests': len(self.results),
            'stats': self.stats,
            'results': self.results
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Results saved to: {output_path}")
        return output_path


def main():
    print("🚀 Starting Mistral CRED Tuned - Important Prompts (20 Conversations)")
    print("="*60)
    print(f"Server: {SERVER_URL}")
    print(f"Model: {MODEL_NAME}")
    print("="*60)

    tester = MistralCredImportantTester()
    data_path = Path(__file__).parent / 'DATA' / 'type2b_20_conversations.csv'
    for g in ['apology', 'empathy', 'feedback_pitch', 'rude_sarcastic']:
        tester.test_conversations(str(data_path), g)

    out_dir = Path(__file__).parent / 'results'
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / 'mistral_cred_tuned_results_important_parameters.json'
    tester.save_results(str(out_file))

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


