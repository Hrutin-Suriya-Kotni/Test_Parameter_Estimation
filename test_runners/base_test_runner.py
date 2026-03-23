#!/usr/bin/env python3
"""
Base test runner for conversation analysis
Provides common functionality for all test runners
"""

import os
import sys
import pandas as pd
import time
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import json
import re

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_clients.base_client import BaseModelClient
from data_loader import load_all_conversations


class BaseTestRunner:
    """Base class for all test runners"""
    
    def __init__(self, model_client: BaseModelClient, test_type: str):
        self.model_client = model_client
        self.test_type = test_type
        self.results = []
        self.model_name = model_client.model_name.lower()
        
        # Create results directory structure
        self.results_dir = f"results/{self.model_name}"
        os.makedirs(self.results_dir, exist_ok=True)
    
    def test_api_connectivity(self) -> bool:
        """Test if the model API is accessible"""
        print(f"🔌 Testing {self.model_client.model_name} API connectivity...")
        
        try:
            if not self.model_client.initialized:
                if not self.model_client.initialize():
                    print(f"❌ {self.model_client.model_name} client initialization failed")
                    return False
            
            if self.model_client.test_connection():
                print(f"✅ {self.model_client.model_name} API connected successfully")
                return True
            else:
                print(f"❌ {self.model_client.model_name} API connection failed")
                return False
                
        except Exception as e:
            print(f"❌ {self.model_client.model_name} API test failed: {e}")
            return False
    
    def load_conversations(self, max_conversations: Optional[int] = None) -> List[Dict[str, Any]]:
        """Load conversations for testing"""
        try:
            conversations = load_all_conversations()
            print(f"📚 Loaded {len(conversations)} conversations for testing")
            
            if max_conversations:
                conversations = conversations[:max_conversations]
                print(f"📝 Using first {len(conversations)} conversations for testing")
            
            return conversations
            
        except Exception as e:
            print(f"❌ Failed to load conversations: {e}")
            print("💡 Using sample conversation for testing...")
            return [{
                'id': 'sample_1',
                'transcript': """Agent: Good morning, this is John calling from Cred. Am I speaking with Sarah?
Customer: Yes, this is Sarah.
Agent: Thank you Sarah. I'm calling regarding your recent transaction."""
            }]
    
    def run_single_conversation_test(self, conversation: Dict[str, Any], prompt: str) -> Dict[str, Any]:
        """Run test on a single conversation"""
        conversation_id = conversation.get('id', 'unknown')
        transcript = conversation.get('transcript', '')
        
        print(f"  🧠 Testing with {self.model_client.model_name}...")
        
        try:
            start_time = time.time()
            response = self.model_client.analyze_conversation(prompt, transcript)
            response_time = time.time() - start_time
            
            result = self.model_client.parse_json_response(response)
            if result:
                primary_result = self._extract_primary_result(result)
                print(f"    ✅ {self.model_client.model_name}: {primary_result or 'Parsed'} ({response_time:.2f}s)")
                success = True
            else:
                print(f"    ⚠️  {self.model_client.model_name}: JSON parsing failed")
                result = {"Value": "JSON Error", "Evidence": response[:200]}
                success = False
                
        except Exception as e:
            print(f"    ❌ {self.model_client.model_name}: Error - {str(e)}")
            result = {"Value": "Error", "Evidence": str(e)}
            response_time = 0
            success = False
        
        return {
            'conversation_id': conversation_id,
            'transcript_length': len(transcript),
            'transcript_preview': transcript[:200] + '...' if len(transcript) > 200 else transcript,
            'timestamp': datetime.now().isoformat(),
            'model_name': self.model_client.model_name,
            'test_type': self.test_type,
            'result': self._extract_primary_result(result) or result.get('Value', 'Error'),
            'evidence': self._extract_primary_evidence(result) or result.get('Evidence', 'Error'),
            'parsed_json': json.dumps(result, ensure_ascii=False),
            'response_time': response_time,
            'success': success,
            'raw_response': response
        }

    def _extract_primary_result(self, parsed: Dict[str, Any]) -> Optional[str]:
        """Extract a primary Met/Not Met style result from arbitrary JSON output."""
        if not isinstance(parsed, dict):
            return None

        # Reassurance prompt variants may return {"step": <int>, "evidence": "..."}
        # Step 8 means Not Met; all earlier steps indicate Met per rubric.
        step_val = parsed.get("step")
        if isinstance(step_val, (int, float)):
            return "Not Met" if int(step_val) >= 8 else "Met"
        if isinstance(step_val, str) and step_val.strip().isdigit():
            return "Not Met" if int(step_val.strip()) >= 8 else "Met"

        if isinstance(parsed.get("Value"), str):
            return parsed.get("Value")

        # Prefer fields ending with "_result"
        for k in parsed.keys():
            if isinstance(k, str) and k.lower().endswith("_result") and isinstance(parsed.get(k), str):
                return parsed.get(k)

        # Common field names
        for k in ("result", "Result", "status", "Status"):
            if isinstance(parsed.get(k), str):
                return parsed.get(k)

        # If multiple Met/Not Met fields exist (e.g., closing has 3), summarize
        met_like = []
        for k, v in parsed.items():
            if isinstance(v, str) and v in {"Met", "Not Met"}:
                met_like.append(v)
        if met_like:
            return "Met" if all(v == "Met" for v in met_like) else "Not Met"

        return None

    def _extract_primary_evidence(self, parsed: Dict[str, Any]) -> Optional[str]:
        """Extract primary evidence from arbitrary JSON output."""
        if not isinstance(parsed, dict):
            return None

        if isinstance(parsed.get("Evidence"), str):
            return parsed.get("Evidence")

        # If there's a *_result key, try matching *_evidence
        result_keys = [k for k in parsed.keys() if isinstance(k, str) and k.lower().endswith("_result")]
        for rk in result_keys:
            prefix = re.sub(r"(?i)_result$", "", rk)
            candidate_keys = [
                f"{prefix}_evidence",
                f"{prefix}_Evidence",
                f"{prefix}_EVIDENCE",
            ]
            for ck in candidate_keys:
                if isinstance(parsed.get(ck), str):
                    return parsed.get(ck)

        # Otherwise pick the first string field containing "evidence"
        for k, v in parsed.items():
            if isinstance(k, str) and "evidence" in k.lower() and isinstance(v, str):
                return v

        # Fallback: compact summary
        return json.dumps(parsed, ensure_ascii=False)[:500]
    
    def run_tests(self, conversations: List[Dict[str, Any]], prompt: str, max_conversations: Optional[int] = None) -> List[Dict[str, Any]]:
        """Run tests on all conversations"""
        if max_conversations:
            conversations = conversations[:max_conversations]
        
        print(f"\n🧪 Testing {len(conversations)} conversations for {self.test_type} analysis with {self.model_client.model_name}...")
        
        results = []
        
        for i, conv in enumerate(conversations):
            print(f"\n📝 Processing conversation {i+1}/{len(conversations)} (ID: {conv.get('id', f'conv_{i+1}')})")
            
            result = self.run_single_conversation_test(conv, prompt)
            results.append(result)
            
            # Rate limiting
            time.sleep(2)
        
        self.results = results
        return results
    
    def save_results(self, results: List[Dict[str, Any]]) -> str:
        """Save results to CSV file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.test_type}_test_results_{timestamp}.csv"
        filepath = os.path.join(self.results_dir, filename)
        
        df = pd.DataFrame(results)
        df.to_csv(filepath, index=False)
        
        print(f"\n💾 Results saved to: {filepath}")
        return filepath
    
    def print_summary(self, results: List[Dict[str, Any]]):
        """Print test summary"""
        print("\n" + "=" * 60)
        print(f"📊 {self.test_type.upper()} TEST SUMMARY - {self.model_client.model_name.upper()}")
        print("=" * 60)
        
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r['success'])
        met_count = sum(1 for r in results if r['result'] == 'Met')
        not_met_count = sum(1 for r in results if r['result'] == 'Not Met')
        
        # Calculate average response time for successful tests
        successful_times = [r['response_time'] for r in results if r['success']]
        avg_response_time = sum(successful_times) / len(successful_times) if successful_times else 0
        
        print(f"Total conversations tested: {total_tests}")
        print(f"Successful API calls: {successful_tests}/{total_tests} ({(successful_tests/total_tests)*100:.1f}%)")
        print(f"Average response time: {avg_response_time:.2f}s")
        print(f"Results - Met: {met_count}, Not Met: {not_met_count}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if successful_tests < total_tests * 0.9:
            print(f"• {self.model_client.model_name} has {total_tests - successful_tests} failures - check API status")
        if avg_response_time > 10:
            print(f"• Response time is slow ({avg_response_time:.2f}s) - consider optimization")
    
    def run_full_test(self, prompt: str, max_conversations: Optional[int] = None) -> str:
        """Run complete test suite"""
        print(f"🚀 Testing {self.test_type} Conversations - {self.model_client.model_name}")
        print("=" * 60)
        
        # Test connectivity
        if not self.test_api_connectivity():
            return None
        
        # Load conversations
        conversations = self.load_conversations(max_conversations)
        
        # Run tests
        results = self.run_tests(conversations, prompt)
        
        # Save results
        filepath = self.save_results(results)
        
        # Print summary
        self.print_summary(results)
        
        return filepath
