#!/usr/bin/env python3
"""
Model comparison test runner
Compares results between different models for the same conversations
"""

import os
import sys
import pandas as pd
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_clients.mistral_client import MistralClient
from model_clients.gemini_client import GeminiClient
from test_runners.base_test_runner import BaseTestRunner
from prompts import ASSESSMENT_PROMPTS
from model_config import ModelConfig


class ComparisonTestRunner:
    """Test runner for comparing models"""
    
    def __init__(self):
        self.available_models = {}
        self.results_dir = "results/comparison"
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Initialize available models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize all available models"""
        print("🔧 Initializing models for comparison...")
        
        # Try to initialize Mistral
        try:
            mistral_client = MistralClient()
            if mistral_client.initialize():
                self.available_models['mistral'] = mistral_client
                print("✅ Mistral model initialized successfully")
            else:
                print("❌ Mistral model initialization failed")
        except Exception as e:
            print(f"❌ Mistral model error: {e}")
        
        # Try to initialize Gemini
        try:
            gemini_client = GeminiClient()
            if gemini_client.initialize():
                self.available_models['gemini'] = gemini_client
                print("✅ Gemini model initialized successfully")
            else:
                print("❌ Gemini model initialization failed")
        except Exception as e:
            print(f"❌ Gemini model error: {e}")
        
        print(f"\n📊 Available models for comparison: {list(self.available_models.keys())}")
    
    def compare_models_single_type(self, test_type: str, max_conversations: Optional[int] = None) -> str:
        """Compare all models on a single conversation type"""
        if test_type not in ASSESSMENT_PROMPTS:
            print(f"❌ Test type '{test_type}' not available")
            return None
        
        if len(self.available_models) < 2:
            print("❌ Need at least 2 models for comparison")
            return None
        
        print(f"\n🔍 Comparing models on {test_type.upper()} analysis")
        print("=" * 60)
        
        # Load conversations
        from data_loader import load_all_conversations
        try:
            conversations = load_all_conversations()
            if max_conversations:
                conversations = conversations[:max_conversations]
            print(f"📚 Loaded {len(conversations)} conversations for comparison")
        except Exception as e:
            print(f"❌ Failed to load conversations: {e}")
            return None
        
        # Run tests with each model
        model_results = {}
        
        for model_name, model_client in self.available_models.items():
            print(f"\n🧪 Testing with {model_name.upper()}...")
            
            test_runner = BaseTestRunner(model_client, test_type)
            prompt = ASSESSMENT_PROMPTS[test_type]
            
            try:
                # Test connectivity
                if not test_runner.test_api_connectivity():
                    print(f"❌ {model_name} API not accessible")
                    continue
                
                # Run tests
                results = test_runner.run_tests(conversations, prompt, max_conversations)
                model_results[model_name] = results
                
                print(f"✅ {model_name} completed {len(results)} tests")
                
            except Exception as e:
                print(f"❌ {model_name} failed: {e}")
                continue
            
            # Wait between models
            time.sleep(3)
        
        if len(model_results) < 2:
            print("❌ Not enough successful model runs for comparison")
            return None
        
        # Create comparison results
        comparison_results = self._create_comparison_results(model_results, test_type)
        
        # Save comparison results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_type}_comparison_results_{timestamp}.csv"
        filepath = os.path.join(self.results_dir, filename)
        
        df = pd.DataFrame(comparison_results)
        df.to_csv(filepath, index=False)
        
        print(f"\n💾 Comparison results saved to: {filepath}")
        
        # Print comparison summary
        self._print_comparison_summary(df, test_type)
        
        return filepath
    
    def _create_comparison_results(self, model_results: Dict[str, List[Dict]], test_type: str) -> List[Dict]:
        """Create comparison results from individual model results"""
        comparison_results = []
        
        # Get all conversation IDs
        all_conversation_ids = set()
        for results in model_results.values():
            for result in results:
                all_conversation_ids.add(result['conversation_id'])
        
        # Create comparison for each conversation
        for conv_id in all_conversation_ids:
            comparison_row = {
                'conversation_id': conv_id,
                'test_type': test_type,
                'timestamp': datetime.now().isoformat()
            }
            
            # Add results from each model
            for model_name, results in model_results.items():
                # Find result for this conversation
                conv_result = next((r for r in results if r['conversation_id'] == conv_id), None)
                
                if conv_result:
                    comparison_row.update({
                        f'{model_name}_result': conv_result['result'],
                        f'{model_name}_evidence': conv_result['evidence'],
                        f'{model_name}_response_time': conv_result['response_time'],
                        f'{model_name}_success': conv_result['success']
                    })
                else:
                    comparison_row.update({
                        f'{model_name}_result': 'Not Tested',
                        f'{model_name}_evidence': 'Not Tested',
                        f'{model_name}_response_time': 0,
                        f'{model_name}_success': False
                    })
            
            # Calculate agreement between models
            model_names = list(model_results.keys())
            if len(model_names) >= 2:
                results_match = self._check_results_agreement(comparison_row, model_names)
                comparison_row['results_agree'] = results_match
            
            comparison_results.append(comparison_row)
        
        return comparison_results
    
    def _check_results_agreement(self, comparison_row: Dict, model_names: List[str]) -> bool:
        """Check if results from different models agree"""
        results = []
        for model_name in model_names:
            result = comparison_row.get(f'{model_name}_result', 'Not Tested')
            if result not in ['Not Tested', 'Error', 'JSON Error']:
                results.append(result)
        
        if len(results) < 2:
            return False
        
        # Check if all results are the same
        return len(set(results)) == 1
    
    def _print_comparison_summary(self, df: pd.DataFrame, test_type: str):
        """Print comparison summary"""
        print("\n" + "=" * 60)
        print(f"📊 {test_type.upper()} COMPARISON SUMMARY")
        print("=" * 60)
        
        total_conversations = len(df)
        model_names = [col.replace('_result', '') for col in df.columns if col.endswith('_result')]
        
        print(f"Total conversations compared: {total_conversations}")
        print(f"Models compared: {', '.join(model_names)}")
        
        # Agreement analysis
        if 'results_agree' in df.columns:
            agreements = df['results_agree'].sum()
            agreement_rate = (agreements / total_conversations) * 100
            print(f"Results agreement: {agreements}/{total_conversations} ({agreement_rate:.1f}%)")
        
        # Success rates
        for model_name in model_names:
            success_col = f'{model_name}_success'
            if success_col in df.columns:
                successes = df[success_col].sum()
                success_rate = (successes / total_conversations) * 100
                print(f"{model_name.upper()} success rate: {successes}/{total_conversations} ({success_rate:.1f}%)")
        
        # Performance comparison
        print(f"\n⏱️  Performance Comparison:")
        for model_name in model_names:
            time_col = f'{model_name}_response_time'
            if time_col in df.columns:
                successful_times = df[df[f'{model_name}_success']][time_col]
                if len(successful_times) > 0:
                    avg_time = successful_times.mean()
                    print(f"  {model_name.upper()}: {avg_time:.2f}s average")
        
        # Results breakdown
        print(f"\n📊 Results Breakdown:")
        for model_name in model_names:
            result_col = f'{model_name}_result'
            if result_col in df.columns:
                met_count = len(df[df[result_col] == 'Met'])
                not_met_count = len(df[df[result_col] == 'Not Met'])
                print(f"  {model_name.upper()}: Met={met_count}, Not Met={not_met_count}")
    
    def compare_all_types(self, max_conversations: Optional[int] = None) -> Dict[str, str]:
        """Compare models on all conversation types"""
        print(f"\n🚀 Comparing ALL conversation types")
        print("=" * 60)
        
        results = {}
        
        for test_type in ASSESSMENT_PROMPTS.keys():
            print(f"\n{'='*50}")
            print(f"Comparing {test_type.upper()}")
            print(f"{'='*50}")
            
            try:
                filepath = self.compare_models_single_type(test_type, max_conversations)
                if filepath:
                    results[test_type] = filepath
                    print(f"✅ {test_type} comparison completed successfully!")
                else:
                    print(f"❌ {test_type} comparison failed!")
                    
            except Exception as e:
                print(f"❌ {test_type} comparison failed with error: {str(e)}")
                results[test_type] = None
            
            # Wait between comparisons
            time.sleep(5)
        
        return results
    
    def run_interactive(self):
        """Run interactive comparison selection"""
        print("🔍 Model Comparison Test Runner")
        print("=" * 40)
        
        if len(self.available_models) < 2:
            print("❌ Need at least 2 models for comparison!")
            print(f"Available models: {list(self.available_models.keys())}")
            return
        
        test_types = list(ASSESSMENT_PROMPTS.keys())
        
        while True:
            print(f"\nAvailable models: {', '.join(self.available_models.keys())}")
            print(f"Available test types: {', '.join(test_types)}")
            
            print("\nOptions:")
            print("  1. Compare all models on single test type")
            print("  2. Compare all models on all test types")
            print("  3. Exit")
            
            try:
                choice = input("\nEnter your choice (1-3): ").strip()
                
                if choice == '1':
                    print("\nSelect test type:")
                    for i, test_type in enumerate(test_types, 1):
                        print(f"  {i}. {test_type}")
                    
                    test_choice = input(f"Enter test number (1-{len(test_types)}): ").strip()
                    try:
                        test_index = int(test_choice) - 1
                        if 0 <= test_index < len(test_types):
                            test_type = test_types[test_index]
                            max_conv = input("Enter max conversations (or press Enter for all): ").strip()
                            max_conv = int(max_conv) if max_conv.isdigit() else None
                            
                            self.compare_models_single_type(test_type, max_conv)
                        else:
                            print("Invalid test number!")
                    except ValueError:
                        print("Please enter a valid number!")
                        
                elif choice == '2':
                    max_conv = input("Enter max conversations (or press Enter for all): ").strip()
                    max_conv = int(max_conv) if max_conv.isdigit() else None
                    
                    start_time = datetime.now()
                    results = self.compare_all_types(max_conv)
                    end_time = datetime.now()
                    
                    print(f"\n🎯 ALL COMPARISONS COMPLETED!")
                    print(f"⏱️  Total time: {end_time - start_time}")
                    print(f"📁 Results saved in: results/comparison/")
                    
                elif choice == '3':
                    print("👋 Goodbye!")
                    break
                    
                else:
                    print("Please enter a valid choice (1-3)")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  Comparison interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}")


def main():
    """Main function"""
    runner = ComparisonTestRunner()
    runner.run_interactive()


if __name__ == "__main__":
    main()
