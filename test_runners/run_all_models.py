#!/usr/bin/env python3
"""
Master test runner for all models
Runs tests for all available models and conversation types
"""

import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_clients.mistral_client import MistralClient
from model_clients.gemini_client import GeminiClient
from test_runners.base_test_runner import BaseTestRunner
from prompts import ASSESSMENT_PROMPTS


class MasterTestRunner:
    """Master test runner for all models"""
    
    def __init__(self):
        self.available_models = {}
        self.test_results = {}
        
        # Initialize available models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize all available models"""
        print("🔧 Initializing available models...")
        
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
        
        print(f"\n📊 Available models: {list(self.available_models.keys())}")
    
    def test_single_model_single_type(self, model_name: str, test_type: str, max_conversations: Optional[int] = None) -> Optional[str]:
        """Test a single model with a single conversation type"""
        if model_name not in self.available_models:
            print(f"❌ Model '{model_name}' not available")
            return None
        
        if test_type not in ASSESSMENT_PROMPTS:
            print(f"❌ Test type '{test_type}' not available")
            return None
        
        print(f"\n🧪 Testing {test_type} with {model_name.upper()}")
        print("-" * 50)
        
        model_client = self.available_models[model_name]
        test_runner = BaseTestRunner(model_client, test_type)
        prompt = ASSESSMENT_PROMPTS[test_type]
        
        try:
            filepath = test_runner.run_full_test(prompt, max_conversations)
            return filepath
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return None
    
    def test_single_model_all_types(self, model_name: str, max_conversations: Optional[int] = None) -> Dict[str, Optional[str]]:
        """Test a single model with all conversation types"""
        if model_name not in self.available_models:
            print(f"❌ Model '{model_name}' not available")
            return {}
        
        print(f"\n🚀 Testing ALL conversation types with {model_name.upper()}")
        print("=" * 60)
        
        results = {}
        
        for test_type in ASSESSMENT_PROMPTS.keys():
            try:
                filepath = self.test_single_model_single_type(model_name, test_type, max_conversations)
                results[test_type] = filepath
                
                if filepath:
                    print(f"✅ {test_type} completed successfully")
                else:
                    print(f"❌ {test_type} failed")
                    
            except Exception as e:
                print(f"❌ {test_type} failed with error: {e}")
                results[test_type] = None
            
            # Wait between tests
            time.sleep(3)
        
        return results
    
    def test_all_models_single_type(self, test_type: str, max_conversations: Optional[int] = None) -> Dict[str, Optional[str]]:
        """Test all models with a single conversation type"""
        if test_type not in ASSESSMENT_PROMPTS:
            print(f"❌ Test type '{test_type}' not available")
            return {}
        
        print(f"\n🚀 Testing {test_type.upper()} with ALL models")
        print("=" * 60)
        
        results = {}
        
        for model_name in self.available_models.keys():
            try:
                filepath = self.test_single_model_single_type(model_name, test_type, max_conversations)
                results[model_name] = filepath
                
                if filepath:
                    print(f"✅ {model_name} completed successfully")
                else:
                    print(f"❌ {model_name} failed")
                    
            except Exception as e:
                print(f"❌ {model_name} failed with error: {e}")
                results[model_name] = None
            
            # Wait between models
            time.sleep(5)
        
        return results
    
    def test_all_models_all_types(self, max_conversations: Optional[int] = None) -> Dict[str, Dict[str, Optional[str]]]:
        """Test all models with all conversation types"""
        print(f"\n🚀 Testing ALL models with ALL conversation types")
        print("=" * 60)
        
        all_results = {}
        
        for model_name in self.available_models.keys():
            print(f"\n{'='*60}")
            print(f"Testing {model_name.upper()} model")
            print(f"{'='*60}")
            
            model_results = self.test_single_model_all_types(model_name, max_conversations)
            all_results[model_name] = model_results
            
            # Wait between models
            time.sleep(5)
        
        return all_results
    
    def print_available_options(self):
        """Print available test options"""
        print("\n📋 Available Test Options:")
        print("=" * 40)
        
        print(f"Available Models: {', '.join(self.available_models.keys())}")
        print(f"Available Test Types: {', '.join(ASSESSMENT_PROMPTS.keys())}")
        
        print("\nTest Combinations:")
        print("  1. Single model, single test type")
        print("  2. Single model, all test types")
        print("  3. All models, single test type")
        print("  4. All models, all test types")
        print("  5. Exit")
    
    def run_interactive(self):
        """Run interactive test selection"""
        print("🎯 Master Test Runner - All Models")
        print("=" * 50)
        
        if not self.available_models:
            print("❌ No models available! Please check your configuration.")
            return
        
        while True:
            self.print_available_options()
            
            try:
                choice = input("\nEnter your choice (1-5): ").strip()
                
                if choice == '1':
                    # Single model, single test type
                    print(f"\nAvailable models: {', '.join(self.available_models.keys())}")
                    model = input("Enter model name: ").strip().lower()
                    
                    print(f"\nAvailable test types: {', '.join(ASSESSMENT_PROMPTS.keys())}")
                    test_type = input("Enter test type: ").strip().lower()
                    
                    max_conv = input("Enter max conversations (or press Enter for all): ").strip()
                    max_conv = int(max_conv) if max_conv.isdigit() else None
                    
                    self.test_single_model_single_type(model, test_type, max_conv)
                    
                elif choice == '2':
                    # Single model, all test types
                    print(f"\nAvailable models: {', '.join(self.available_models.keys())}")
                    model = input("Enter model name: ").strip().lower()
                    
                    max_conv = input("Enter max conversations (or press Enter for all): ").strip()
                    max_conv = int(max_conv) if max_conv.isdigit() else None
                    
                    start_time = datetime.now()
                    results = self.test_single_model_all_types(model, max_conv)
                    end_time = datetime.now()
                    
                    print(f"\n🎯 {model.upper()} ALL TESTS COMPLETED!")
                    print(f"⏱️  Total time: {end_time - start_time}")
                    print(f"📁 Results saved in: results/{model}/")
                    
                elif choice == '3':
                    # All models, single test type
                    print(f"\nAvailable test types: {', '.join(ASSESSMENT_PROMPTS.keys())}")
                    test_type = input("Enter test type: ").strip().lower()
                    
                    max_conv = input("Enter max conversations (or press Enter for all): ").strip()
                    max_conv = int(max_conv) if max_conv.isdigit() else None
                    
                    start_time = datetime.now()
                    results = self.test_all_models_single_type(test_type, max_conv)
                    end_time = datetime.now()
                    
                    print(f"\n🎯 ALL MODELS {test_type.upper()} TESTS COMPLETED!")
                    print(f"⏱️  Total time: {end_time - start_time}")
                    print(f"📁 Results saved in: results/[model]/")
                    
                elif choice == '4':
                    # All models, all test types
                    max_conv = input("Enter max conversations (or press Enter for all): ").strip()
                    max_conv = int(max_conv) if max_conv.isdigit() else None
                    
                    start_time = datetime.now()
                    results = self.test_all_models_all_types(max_conv)
                    end_time = datetime.now()
                    
                    print(f"\n🎯 ALL MODELS ALL TESTS COMPLETED!")
                    print(f"⏱️  Total time: {end_time - start_time}")
                    print(f"📁 Results saved in: results/[model]/")
                    
                elif choice == '5':
                    print("👋 Goodbye!")
                    break
                    
                else:
                    print("Please enter a valid choice (1-5)")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  Test interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}")


def main():
    """Main function"""
    runner = MasterTestRunner()
    runner.run_interactive()


if __name__ == "__main__":
    main()
