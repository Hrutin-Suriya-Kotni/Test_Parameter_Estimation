#!/usr/bin/env python3
"""
MISTRAL_BOOM_BOOM Test Runner
Tests 4 APIs on 3 data types with full metadata tracking
"""

import os
import sys
import pandas as pd
import time
import importlib
from datetime import datetime
from typing import Dict, List, Any, Optional

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from boom_boom_data_loader import BoomBoomDataLoader
from model_config import ModelConfig
from prompts import ASSESSMENT_PROMPTS


class BoomBoomTestRunner:
    """Test runner for MISTRAL_BOOM_BOOM project"""
    
    def __init__(self):
        """Initialize BOOM BOOM test runner"""
        self.data_loader = BoomBoomDataLoader()
        self.results_base_dir = "MISTRAL_BOOM_BOOM"
        
        # BOOM BOOM models
        self.boom_boom_models = [
            'server3_base_openchat_mistral',
            'server5_base_mistral',
            'karvalo_base_openchat_mistal',
            'gemini_api'
        ]
        
        # Data types
        self.data_types = ['type1', 'type2a', 'type2b']
        
        print("🎉 MISTRAL_BOOM_BOOM Test Runner Initialized!")
        print(f"   Models: {len(self.boom_boom_models)}")
        print(f"   Data Types: {len(self.data_types)}")
    
    def _initialize_model(self, model_name: str):
        """Initialize a model client"""
        try:
            config = ModelConfig.get_model_config(model_name)
            if not config:
                print(f"❌ Model '{model_name}' not found in config")
                return None
            
            # Check if model is ready (Karvalo is TBD)
            if config.get('config', {}).get('api_url') == 'TBD':
                print(f"⚠️  {config['display_name']} API not configured yet (TBD)")
                return None
            
            # Check requirements
            requirements = ModelConfig.check_model_requirements(model_name)
            if not requirements['available']:
                print(f"❌ {config['display_name']}: {requirements['reason']}")
                return None
            
            # Dynamically import and initialize
            module_path = config['module_path']
            class_name = config['class_name']
            
            module = importlib.import_module(module_path)
            client_class = getattr(module, class_name)
            client = client_class()
            
            if client.initialize():
                print(f"✅ {config['display_name']} initialized")
                return client
            else:
                print(f"❌ {config['display_name']} initialization failed")
                return None
                
        except Exception as e:
            print(f"❌ Error initializing {model_name}: {e}")
            return None
    
    def test_single_conversation(self, client, conv: Dict[str, Any], 
                                 test_type: str = 'opening') -> Dict[str, Any]:
        """
        Test a single conversation with metadata tracking
        
        Args:
            client: Model client
            conv: Conversation dictionary
            test_type: Type of test (opening, closing, etc.)
            
        Returns:
            Result dictionary with metadata
        """
        prompt = ASSESSMENT_PROMPTS.get(test_type, ASSESSMENT_PROMPTS['opening'])
        
        try:
            print(f"\n      🔍 Processing conversation: {conv['id'][:30]}...")
            print(f"      📏 Transcript length: {len(conv['transcript'])} chars")
            
            # Get model info first
            model_info = {}
            if hasattr(client, 'get_model_info'):
                model_info = client.get_model_info()
                print(f"      🤖 Model: {model_info.get('model', 'N/A')}")
                print(f"      🌡️  Temperature: {model_info.get('temperature', 'N/A')}")
            
            # Make API call
            print(f"      ⏳ Sending request to API...")
            start_time = time.time()
            response = client.analyze_conversation(prompt, conv['transcript'])
            end_time = time.time()
            latency = end_time - start_time
            print(f"      ⚡ Response received in {latency:.2f}s")
            
            # Parse response
            print(f"      🔄 Parsing JSON response...")
            print(f"      📝 Response length: {len(response)} chars")
            print(f"      📝 Response preview (first 200 chars): {response[:200]}...")
            print(f"      📝 Response preview (last 200 chars): ...{response[-200:]}")
            
            parsed = client.parse_json_response(response)
            
            if parsed:
                print(f"      ✅ Parse successful: {parsed.get('Value', 'Unknown')}")
            else:
                print(f"      ⚠️  Parse failed!")
                print(f"      🔍 Checking for JSON markers...")
                print(f"      📝 Contains '{{': {'{' in response}")
                print(f"      📝 Contains '}}': {'}' in response}")
                if '{' in response and '}' in response:
                    start = response.find('{')
                    end = response.rfind('}') + 1
                    print(f"      📝 JSON substring (first 300 chars): {response[start:start+300]}...")
            
            # Get metadata from client (if available)
            metadata = {}
            if hasattr(client, 'get_last_metadata'):
                metadata = client.get_last_metadata()
            
            # Build result
            result = {
                'conversation_id': conv['id'],
                'data_type': conv.get('type', 'unknown'),
                
                # Parameter being tested (what guideline we're checking)
                'parameter_tested': test_type.upper(),
                'parameter_name': test_type.replace('_', ' ').title(),
                
                'model_name': client.model_name,
                'timestamp': datetime.now().isoformat(),
                
                # Model API Parameters
                'api_temperature': model_info.get('temperature', metadata.get('temperature', 'N/A')),
                'api_max_tokens': model_info.get('max_tokens', model_info.get('max_output_tokens', 
                                  model_info.get('max_new_tokens', metadata.get('max_tokens', 
                                  metadata.get('max_new_tokens', 'N/A'))))),
                'api_endpoint': model_info.get('api_url', metadata.get('api_endpoint', 'N/A')),
                'model_version': model_info.get('model', 'N/A'),
                
                # Results
                'success': parsed is not None,
                'result_value': parsed.get('Value', 'Error') if parsed else 'Parse Error',
                'evidence': parsed.get('Evidence', 'N/A') if parsed else 'Failed to parse JSON',
                
                # Metrics
                'transcript_length': len(conv['transcript']),
                'response_length': len(response),
                'total_latency': round(end_time - start_time, 3),
                
                # Add all other metadata from client
                **metadata
            }
            
            return result
            
        except Exception as e:
            return {
                'conversation_id': conv['id'],
                'data_type': conv.get('type', 'unknown'),
                'parameter_tested': test_type.upper(),
                'parameter_name': test_type.replace('_', ' ').title(),
                'model_name': client.model_name,
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'result_value': 'Error',
                'evidence': str(e),
                'error': str(e)
            }
    
    def test_model_on_data_type(self, model_name: str, data_type: str,
                                test_type: str = 'opening', 
                                max_conversations: int = None) -> Optional[str]:
        """
        Test a model on a specific data type
        
        Args:
            model_name: Model to test
            data_type: 'type1', 'type2a', or 'type2b'
            test_type: Assessment type (opening, closing, etc.)
            max_conversations: Max conversations to test
            
        Returns:
            Path to results file or None
        """
        print(f"\n{'='*70}")
        print(f"🧪 Testing: {model_name} | Data: {data_type} | Test: {test_type}")
        print(f"{'='*70}")
        
        # Initialize model
        print(f"🔧 Initializing model client...")
        client = self._initialize_model(model_name)
        if not client:
            print(f"⚠️  Skipping {model_name} - not available")
            return None
        
        print(f"✅ Model client initialized successfully!")
        
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
            
            result = self.test_single_conversation(client, conv, test_type)
            results.append(result)
            
            # Print result summary
            print(f"\n      📊 RESULT:")
            if result['success']:
                print(f"      ✅ Status: SUCCESS")
                print(f"      🎯 Value: {result['result_value']}")
                print(f"      ⏱️  Latency: {result.get('total_latency', 0):.2f}s")
                successful_tests += 1
            else:
                print(f"      ❌ Status: FAILED")
                print(f"      💥 Error: {result.get('error', 'Unknown error')}")
                failed_tests += 1
            
            print(f"\n      📈 Progress: {successful_tests} passed, {failed_tests} failed, {len(conversations) - i - 1} remaining")
            
            # Rate limiting
            if i < len(conversations) - 1:
                print(f"      ⏸️  Sleeping 1s before next test...")
                time.sleep(1)
        
        # Save results with timestamp folder
        print(f"\n{'='*70}")
        print(f"💾 SAVING RESULTS")
        print(f"{'='*70}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_dir = os.path.join(self.results_base_dir, data_type, model_name, timestamp)
        
        print(f"📁 Creating directory: {results_dir}")
        os.makedirs(results_dir, exist_ok=True)
        
        filename = f"{test_type}_results.csv"
        filepath = os.path.join(results_dir, filename)
        
        print(f"📝 Converting {len(results)} results to DataFrame...")
        df = pd.DataFrame(results)
        
        print(f"💾 Writing to CSV: {filepath}")
        df.to_csv(filepath, index=False)
        print(f"✅ File saved successfully!")
        
        # Print summary
        self._print_test_summary(results, model_name, data_type, test_type)
        
        print(f"\n{'='*70}")
        print(f"✅ TEST BATCH COMPLETE!")
        print(f"{'='*70}")
        print(f"📂 Results location: {filepath}")
        print(f"{'='*70}\n")
        
        return filepath
    
    def _print_test_summary(self, results: List[Dict], model_name: str, 
                           data_type: str, test_type: str):
        """Print test summary with metadata"""
        print(f"\n{'='*70}")
        print(f"📊 SUMMARY: {model_name} | {data_type} | {test_type}")
        print(f"{'='*70}")
        
        total = len(results)
        successful = sum(1 for r in results if r['success'])
        met = sum(1 for r in results if r.get('result_value') == 'Met')
        not_met = sum(1 for r in results if r.get('result_value') == 'Not Met')
        
        print(f"Total conversations: {total}")
        print(f"Successful calls: {successful}/{total} ({(successful/total)*100:.1f}%)")
        print(f"Results - Met: {met}, Not Met: {not_met}")
        
        # Calculate average latency
        latencies = [r.get('total_latency', 0) for r in results if r['success']]
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            print(f"\nLatency Stats:")
            print(f"  Average: {avg_latency:.3f}s")
            print(f"  Min: {min_latency:.3f}s")
            print(f"  Max: {max_latency:.3f}s")
        
        # Token stats (if available)
        tokens = [r.get('total_tokens', r.get('total_tokens_estimate', 0)) for r in results if r['success']]
        if tokens and sum(tokens) > 0:
            avg_tokens = sum(tokens) / len(tokens)
            total_tokens = sum(tokens)
            print(f"\nToken Stats:")
            print(f"  Average per conversation: {avg_tokens:.0f}")
            print(f"  Total tokens: {total_tokens}")
    
    def test_all_models_all_data_types(self, test_type: str = 'opening',
                                      max_conversations: int = None):
        """
        Test all available models on all data types
        
        Args:
            test_type: Assessment type
            max_conversations: Max conversations per data type
        """
        print("\n" + "="*70)
        print("🚀 MISTRAL_BOOM_BOOM - FULL TEST SUITE")
        print("="*70)
        print(f"Test Type: {test_type}")
        print(f"Max Conversations: {max_conversations or 'ALL'}")
        print("="*70)
        
        start_time = time.time()
        results_map = {}
        
        for model_name in self.boom_boom_models:
            for data_type in self.data_types:
                key = f"{model_name}_{data_type}"
                filepath = self.test_model_on_data_type(
                    model_name, data_type, test_type, max_conversations
                )
                results_map[key] = filepath
                
                # Small delay between tests
                time.sleep(2)
        
        end_time = time.time()
        
        # Final summary
        print("\n" + "="*70)
        print("🎉 ALL TESTS COMPLETED!")
        print("="*70)
        print(f"Total time: {(end_time - start_time)/60:.1f} minutes")
        print(f"\nResults saved in: {self.results_base_dir}/")
        
        # Show what was completed
        completed = sum(1 for v in results_map.values() if v is not None)
        total = len(results_map)
        print(f"Completed: {completed}/{total} tests")
        
        return results_map


def main():
    """Interactive main function - ALL SERIAL NUMBER BASED"""
    runner = BoomBoomTestRunner()
    
    print("\n" + "="*70)
    print("🎯 MISTRAL_BOOM_BOOM Test Menu")
    print("="*70)
    print("\nAvailable Models:")
    for i, model in enumerate(runner.boom_boom_models, 1):
        config = ModelConfig.get_model_config(model)
        status = "✅" if config and config.get('config', {}).get('api_url') != 'TBD' else "⚠️ "
        print(f"  {i}. {status} {config.get('display_name', model) if config else model}")
    
    print("\nAvailable Data Types:")
    for i, dtype in enumerate(runner.data_types, 1):
        print(f"  {i}. {dtype}")
    
    print("\nAvailable Parameters to Test:")
    test_types_list = list(ASSESSMENT_PROMPTS.keys())
    for i, test_type in enumerate(test_types_list, 1):
        print(f"  {i}. {test_type.replace('_', ' ').title()}")
    print(f"  {len(test_types_list)+1}. ALL PARAMETERS (Run all guidelines)")
    
    print("\n" + "="*70)
    print("Test Options:")
    print("  1. Test single model on single data type")
    print("  2. Test single model on all data types")
    print("  3. Test all models on single data type")
    print("  4. Test all models on all data types (FULL RUN)")
    print("  5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == '5':
        print("👋 Goodbye!")
        return
    
    # Get parameter/test type (serial number)
    print("\nSelect parameter to test:")
    for i, test_type in enumerate(test_types_list, 1):
        print(f"  {i}. {test_type.replace('_', ' ').title()}")
    print(f"  {len(test_types_list)+1}. ALL PARAMETERS (Test all guidelines)")
    test_type_choice = input(f"Enter parameter number (1-{len(test_types_list)+1}, or press Enter for 1-Opening): ").strip()
    
    # Handle parameter selection
    test_all_params = False
    if test_type_choice.isdigit():
        test_type_idx = int(test_type_choice) - 1
        if test_type_idx == len(test_types_list):  # ALL PARAMETERS selected
            test_all_params = True
            test_types_to_run = test_types_list
            print(f"✅ Selected: ALL PARAMETERS ({len(test_types_list)} guidelines)")
        elif 0 <= test_type_idx < len(test_types_list):
            test_type = test_types_list[test_type_idx]
            test_types_to_run = [test_type]
            print(f"✅ Selected: {test_type.replace('_', ' ').title()}")
        else:
            print(f"Invalid choice, using 'opening'")
            test_type = 'opening'
            test_types_to_run = [test_type]
    else:
        test_type = 'opening'
        test_types_to_run = [test_type]
        print(f"✅ Selected: Opening (default)")
    
    # Get max conversations
    max_conv = input("\nEnter max conversations per type (or press Enter for all): ").strip()
    max_conv = int(max_conv) if max_conv.isdigit() else None
    
    if choice == '1':
        # Single model, single data type
        model_choice = input(f"\nSelect model (1-{len(runner.boom_boom_models)}): ").strip()
        try:
            model_idx = int(model_choice) - 1
            if 0 <= model_idx < len(runner.boom_boom_models):
                model_name = runner.boom_boom_models[model_idx]
                print(f"✅ Selected: {ModelConfig.get_model_config(model_name).get('display_name', model_name)}")
            else:
                print("❌ Invalid model number")
                return
        except:
            print("❌ Invalid input")
            return
        
        dtype_choice = input(f"\nSelect data type (1-{len(runner.data_types)}): ").strip()
        try:
            dtype_idx = int(dtype_choice) - 1
            if 0 <= dtype_idx < len(runner.data_types):
                data_type = runner.data_types[dtype_idx]
                print(f"✅ Selected: {data_type}")
            else:
                print("❌ Invalid data type number")
                return
        except:
            print("❌ Invalid input")
            return
        
        # Run tests for all selected parameters
        for test_param in test_types_to_run:
            runner.test_model_on_data_type(model_name, data_type, test_param, max_conv)
            if len(test_types_to_run) > 1:
                time.sleep(2)  # Delay between parameters
    
    elif choice == '2':
        # Single model, all data types
        model_choice = input(f"\nSelect model (1-{len(runner.boom_boom_models)}): ").strip()
        try:
            model_idx = int(model_choice) - 1
            if 0 <= model_idx < len(runner.boom_boom_models):
                model_name = runner.boom_boom_models[model_idx]
                print(f"✅ Selected: {ModelConfig.get_model_config(model_name).get('display_name', model_name)}")
                
                # Test on all data types and parameters
                for data_type in runner.data_types:
                    for test_param in test_types_to_run:
                        runner.test_model_on_data_type(model_name, data_type, test_param, max_conv)
            else:
                print("❌ Invalid model number")
        except:
            print("❌ Invalid input")
    
    elif choice == '3':
        # All models, single data type
        dtype_choice = input(f"\nSelect data type (1-{len(runner.data_types)}): ").strip()
        try:
            dtype_idx = int(dtype_choice) - 1
            if 0 <= dtype_idx < len(runner.data_types):
                data_type = runner.data_types[dtype_idx]
                print(f"✅ Selected: {data_type}")
                
                # Test all models and parameters
                for model_name in runner.boom_boom_models:
                    for test_param in test_types_to_run:
                        runner.test_model_on_data_type(model_name, data_type, test_param, max_conv)
            else:
                print("❌ Invalid data type number")
        except:
            print("❌ Invalid input")
    
    elif choice == '4':
        # Full run
        print("\n⚠️  This will run ALL models on ALL data types!")
        print(f"   Models: {len(runner.boom_boom_models)}")
        print(f"   Data Types: {len(runner.data_types)}")
        print(f"   Parameters: {len(test_types_to_run)} ({'ALL' if test_all_params else test_types_to_run[0].replace('_', ' ').title()})")
        print(f"   Max conversations: {max_conv or 'ALL'}")
        confirm = input("\nContinue? (yes/no): ")
        if confirm.lower() == 'yes':
            for test_param in test_types_to_run:
                runner.test_all_models_all_data_types(test_param, max_conv)
        else:
            print("Cancelled.")


if __name__ == "__main__":
    main()

