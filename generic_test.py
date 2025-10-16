#!/usr/bin/env python3
"""
Generic test runner for ANY AI model - Zero Code Duplication!

This single file replaces:
- test_mistral.py
- test_gemini.py  
- run_all_models.py (partially)
- test_comparison.py (partially)

HOW TO USE:
-----------
1. Add your model to model_config.py
2. Run this script: python3 generic_test.py
3. Select your model from the menu
4. Done! No need to create separate test files

BENEFITS:
---------
✅ Works with ANY model in model_config.py automatically
✅ No code duplication - one file for all models
✅ Easy to maintain - change once, affects all models
✅ Automatically discovers new models from config
"""

import os
import sys
import importlib
from datetime import datetime
from typing import Dict, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from test_runners.base_test_runner import BaseTestRunner
from prompts import ASSESSMENT_PROMPTS
from model_config import ModelConfig


class GenericTestRunner:
    """
    Universal test runner that works with ANY model
    Eliminates need for model-specific test files
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize generic test runner
        
        Args:
            model_name: Model identifier from model_config.py (e.g., 'mistral', 'gemini')
                       If None, will prompt user to select
        """
        self.model_name = model_name
        self.model_client = None
        self.test_runners = {}
        
        if model_name:
            self._initialize_model(model_name)
    
    def _initialize_model(self, model_name: str) -> bool:
        """
        Dynamically initialize any model from config
        No hardcoded model names - works with ANY model!
        """
        print(f"\n🔧 Initializing {model_name} model...")
        
        # Get model configuration
        model_config = ModelConfig.get_model_config(model_name)
        if not model_config:
            print(f"❌ Model '{model_name}' not found in configuration")
            return False
        
        # Check requirements (API keys, etc.)
        requirements = ModelConfig.check_model_requirements(model_name)
        if not requirements['available']:
            print(f"❌ Model requirements not met: {requirements['reason']}")
            return False
        
        try:
            # Dynamically import the model client class
            module_path = model_config['module_path']
            class_name = model_config['class_name']
            
            # Import the module
            module = importlib.import_module(module_path)
            
            # Get the class
            client_class = getattr(module, class_name)
            
            # Initialize the client
            self.model_client = client_class()
            
            if self.model_client.initialize():
                print(f"✅ {model_config['display_name']} initialized successfully")
                
                # Initialize test runners for each assessment type
                for test_type in ASSESSMENT_PROMPTS.keys():
                    self.test_runners[test_type] = BaseTestRunner(self.model_client, test_type)
                
                return True
            else:
                print(f"❌ {model_config['display_name']} initialization failed")
                return False
                
        except Exception as e:
            print(f"❌ Failed to initialize {model_name}: {e}")
            return False
    
    def test_single_type(self, test_type: str, max_conversations: int = None) -> str:
        """Test a single conversation type"""
        if not self.model_client:
            print("❌ No model initialized")
            return None
        
        if test_type not in self.test_runners:
            print(f"❌ Unknown test type: {test_type}")
            return None
        
        print(f"\n🧪 Running {test_type} test with {self.model_client.model_name}...")
        prompt = ASSESSMENT_PROMPTS[test_type]
        return self.test_runners[test_type].run_full_test(prompt, max_conversations)
    
    def test_all_types(self, max_conversations: int = None) -> Dict[str, str]:
        """Test all conversation types"""
        if not self.model_client:
            print("❌ No model initialized")
            return {}
        
        print(f"\n🚀 Running ALL conversation tests with {self.model_client.model_name}")
        print("=" * 60)
        
        results = {}
        
        for test_type in ASSESSMENT_PROMPTS.keys():
            print(f"\n{'='*50}")
            print(f"Testing {test_type.upper()} with {self.model_client.model_name}")
            print(f"{'='*50}")
            
            try:
                filepath = self.test_single_type(test_type, max_conversations)
                if filepath:
                    results[test_type] = filepath
                    print(f"✅ {test_type} test completed successfully!")
                else:
                    print(f"❌ {test_type} test failed!")
                    
            except Exception as e:
                print(f"❌ {test_type} test failed with error: {str(e)}")
                results[test_type] = None
            
            # Wait between tests
            import time
            time.sleep(3)
        
        return results
    
    def run_interactive(self):
        """Run interactive test selection"""
        print(f"\n🤖 {self.model_client.model_name if self.model_client else 'Generic'} Model Test Runner")
        print("=" * 40)
        
        if not self.model_client:
            print("❌ No model initialized. Please initialize a model first.")
            return
        
        test_types = list(ASSESSMENT_PROMPTS.keys())
        
        while True:
            print("\nAvailable test types:")
            for i, test_type in enumerate(test_types, 1):
                print(f"  {i}. {test_type}")
            
            print("\nOptions:")
            print("  1. Run all tests")
            print("  2. Run specific test type")
            print("  3. Exit")
            
            try:
                choice = input("\nEnter your choice (1-3): ").strip()
                
                if choice == '1':
                    max_conv = input("Enter max conversations (or press Enter for all): ").strip()
                    max_conv = int(max_conv) if max_conv.isdigit() else None
                    
                    start_time = datetime.now()
                    results = self.test_all_types(max_conv)
                    end_time = datetime.now()
                    
                    print(f"\n{'='*60}")
                    print(f"🎯 ALL {self.model_client.model_name.upper()} TESTS COMPLETED!")
                    print(f"⏱️  Total time: {end_time - start_time}")
                    print(f"📁 Results saved in: results/{self.model_name}/")
                    print(f"{'='*60}")
                    break
                    
                elif choice == '2':
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
                            
                            self.test_single_type(test_type, max_conv)
                        else:
                            print("Invalid test number!")
                    except ValueError:
                        print("Please enter a valid number!")
                        
                elif choice == '3':
                    print("👋 Goodbye!")
                    break
                    
                else:
                    print("Please enter a valid choice (1-3)")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  Test interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}")


def compare_models(model_names: List[str], test_type: str = None, max_conversations: int = None):
    """
    Compare multiple models on same conversations
    
    Args:
        model_names: List of model names to compare
        test_type: Specific test type to compare (None = all types)
        max_conversations: Max conversations to test
    """
    print(f"\n🔍 Comparing Models: {', '.join(model_names)}")
    print("=" * 60)
    
    # Initialize all models
    runners = {}
    for model_name in model_names:
        runner = GenericTestRunner(model_name)
        if runner.model_client:
            runners[model_name] = runner
        else:
            print(f"⚠️  Skipping {model_name} - initialization failed")
    
    if len(runners) < 2:
        print("❌ Need at least 2 models for comparison")
        return
    
    # Run tests
    test_types = [test_type] if test_type else list(ASSESSMENT_PROMPTS.keys())
    
    for t_type in test_types:
        print(f"\n{'='*60}")
        print(f"Comparing models on {t_type.upper()}")
        print(f"{'='*60}")
        
        for model_name, runner in runners.items():
            print(f"\n🧪 Testing with {model_name}...")
            runner.test_single_type(t_type, max_conversations)


def list_available_models():
    """Display all available models from config"""
    print("\n📋 Available Models")
    print("=" * 60)
    
    models_status = ModelConfig.get_available_models_with_status()
    
    available_models = []
    unavailable_models = []
    
    for model_name, info in models_status.items():
        if info['status']['available']:
            available_models.append((model_name, info))
        else:
            unavailable_models.append((model_name, info))
    
    # Show available models
    if available_models:
        print("\n✅ READY TO USE:")
        for model_name, info in available_models:
            print(f"   • {info['display_name']} ({model_name})")
            print(f"     {info['description']}")
    
    # Show unavailable models
    if unavailable_models:
        print("\n❌ NOT READY (Missing Requirements):")
        for model_name, info in unavailable_models:
            print(f"   • {info['display_name']} ({model_name})")
            print(f"     Issue: {info['status']['reason']}")
    
    print("\n" + "=" * 60)
    return available_models, unavailable_models


def main():
    """Main interactive launcher"""
    print("=" * 70)
    print("🎯 GENERIC TEST RUNNER - Works with ANY Model!")
    print("=" * 70)
    
    # List available models
    available_models, unavailable_models = list_available_models()
    
    if not available_models:
        print("\n❌ No models available! Please:")
        print("   1. Add API keys to .env file")
        print("   2. Check model configuration in model_config.py")
        print("   3. Ensure model servers are running (for local models)")
        return
    
    while True:
        print("\n📋 Main Menu")
        print("-" * 40)
        print("  1. Test single model")
        print("  2. Test all available models")
        print("  3. Compare models")
        print("  4. Show model status")
        print("  5. Exit")
        
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                # Test single model
                print("\nAvailable models:")
                for i, (model_name, info) in enumerate(available_models, 1):
                    print(f"  {i}. {info['display_name']} ({model_name})")
                
                model_choice = input(f"\nSelect model (1-{len(available_models)}): ").strip()
                try:
                    model_index = int(model_choice) - 1
                    if 0 <= model_index < len(available_models):
                        model_name = available_models[model_index][0]
                        runner = GenericTestRunner(model_name)
                        if runner.model_client:
                            runner.run_interactive()
                    else:
                        print("Invalid model number!")
                except ValueError:
                    print("Please enter a valid number!")
            
            elif choice == '2':
                # Test all models
                max_conv = input("\nEnter max conversations (or press Enter for all): ").strip()
                max_conv = int(max_conv) if max_conv.isdigit() else None
                
                print("\n🚀 Testing ALL Available Models")
                print("=" * 60)
                
                for model_name, info in available_models:
                    print(f"\n{'='*60}")
                    print(f"Testing {info['display_name']}")
                    print(f"{'='*60}")
                    
                    runner = GenericTestRunner(model_name)
                    if runner.model_client:
                        runner.test_all_types(max_conv)
                    
                    import time
                    time.sleep(5)
                
                print("\n✅ All models tested!")
            
            elif choice == '3':
                # Compare models
                if len(available_models) < 2:
                    print("\n❌ Need at least 2 models for comparison")
                    continue
                
                print("\nAvailable models:")
                for i, (model_name, info) in enumerate(available_models, 1):
                    print(f"  {i}. {info['display_name']} ({model_name})")
                
                print("\nEnter model numbers to compare (comma-separated, e.g., 1,2):")
                model_choices = input("Models: ").strip().split(',')
                
                selected_models = []
                for choice_str in model_choices:
                    try:
                        idx = int(choice_str.strip()) - 1
                        if 0 <= idx < len(available_models):
                            selected_models.append(available_models[idx][0])
                    except ValueError:
                        pass
                
                if len(selected_models) >= 2:
                    max_conv = input("\nEnter max conversations (or press Enter for all): ").strip()
                    max_conv = int(max_conv) if max_conv.isdigit() else None
                    
                    compare_models(selected_models, max_conversations=max_conv)
                else:
                    print("❌ Need at least 2 valid models for comparison")
            
            elif choice == '4':
                # Show model status
                ModelConfig.print_model_status()
            
            elif choice == '5':
                print("\n👋 Goodbye!")
                break
            
            else:
                print("Please enter a valid choice (1-5)")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()


