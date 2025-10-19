"""
Ultimate Test Runner - Core testing engine
Orchestrates testing across models, data types, and categories
"""

import time
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd
import yaml

from .data_handler import DataHandler
from .model_client import ModelClientFactory
from .json_extractor import extract_and_validate
from prompts import ASSESSMENT_PROMPTS

logger = logging.getLogger(__name__)


class TestRunner:
    """Main test runner for the framework"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize test runner with configuration"""
        logger.info("Initializing Ultimate Test Runner")
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize data handler
        data_path = self.config['data']['base_path']
        self.data_handler = DataHandler(data_path)
        
        # Setup output directory
        self.results_dir = Path(self.config['output']['results_dir'])
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Get test configuration
        self.test_config = self.config['testing']
        self.rate_limit_delay = self.test_config.get('rate_limit_delay', 1)
        
        logger.info(f"Results will be saved to: {self.results_dir}")
    
    def get_enabled_models(self) -> Dict[str, Dict[str, Any]]:
        """Get list of enabled models from config"""
        enabled = {}
        for model_id, model_config in self.config['models'].items():
            if model_config.get('enabled', False):
                enabled[model_id] = model_config
        
        logger.info(f"Found {len(enabled)} enabled model(s): {list(enabled.keys())}")
        return enabled
    
    def run_single_test(
        self,
        model_client,
        conversation: Dict[str, Any],
        category: str
    ) -> Dict[str, Any]:
        """
        Run a single test: one conversation + one category
        
        Args:
            model_client: Model client instance
            conversation: Conversation dict with transcript
            category: Test category (opening, closing, etc.)
        
        Returns:
            Dict with test results
        """
        conversation_id = conversation['conversation_id']
        transcript = conversation['transcript']
        data_type = conversation.get('data_type', 'unknown')
        
        # Get the prompt for this category
        prompt = ASSESSMENT_PROMPTS.get(category)
        if not prompt:
            return {
                'conversation_id': conversation_id,
                'data_type': data_type,
                'category': category,
                'success': False,
                'error': f"Unknown category: {category}"
            }
        
        # Construct full prompt
        full_prompt = f"{transcript}\n\n{prompt}"
        
        # Call model
        start_time = time.time()
        response = model_client.generate(full_prompt)
        
        if not response['success']:
            return {
                'conversation_id': conversation_id,
                'data_type': data_type,
                'category': category,
                'model': model_client.name,
                'success': False,
                'error': response.get('error', 'Unknown error'),
                'latency': response.get('latency', 0),
                'timestamp': datetime.now().isoformat()
            }
        
        # Extract and validate JSON
        extraction_result = extract_and_validate(response['response'])
        
        result = {
            'conversation_id': conversation_id,
            'data_type': data_type,
            'category': category,
            'model': model_client.name,
            'success': extraction_result['success'],
            'latency': response['latency'],
            'timestamp': datetime.now().isoformat()
        }
        
        if extraction_result['success']:
            result['value'] = extraction_result['data']['Value']
            result['evidence'] = extraction_result['data']['Evidence']
            result['error'] = None
        else:
            result['value'] = None
            result['evidence'] = None
            result['error'] = extraction_result['error']
        
        # Include raw response if configured
        if self.config['output'].get('include_raw_responses', True):
            result['raw_response'] = response['response']
        
        return result
    
    def run_model_on_data_type(
        self,
        model_id: str,
        model_config: Dict[str, Any],
        data_type: str,
        categories: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Run one model on one data type across multiple categories
        
        Args:
            model_id: Model identifier
            model_config: Model configuration dict
            data_type: Data type (type1, type2a, type2b)
            categories: List of categories to test (None = all)
        
        Returns:
            List of result dicts
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Testing: {model_config['name']} on {data_type}")
        logger.info(f"{'='*60}")
        
        # Load data
        conversations = self.data_handler.load_specific_type(data_type)
        logger.info(f"Loaded {len(conversations)} conversations")
        
        # Get categories to test
        if categories is None:
            categories = self.config['test_categories']
        
        # Create model client
        try:
            model_client = ModelClientFactory.create_client(model_config)
        except Exception as e:
            logger.error(f"Failed to create model client: {e}")
            return []
        
        # Run tests
        all_results = []
        total_tests = len(conversations) * len(categories)
        completed = 0
        
        for conversation in conversations:
            for category in categories:
                completed += 1
                logger.info(f"\nProgress: {completed}/{total_tests} - " +
                          f"Conv: {conversation['conversation_id'][:8]}... " +
                          f"Category: {category}")
                
                # Run test with retry logic
                result = self._run_with_retry(model_client, conversation, category)
                all_results.append(result)
                
                # Log result
                if result['success']:
                    logger.info(f"✅ Success - Value: {result['value']}, " +
                              f"Latency: {result['latency']:.2f}s")
                else:
                    logger.warning(f"❌ Failed - Error: {result['error']}")
                
                # Rate limiting
                time.sleep(self.rate_limit_delay)
        
        # Save results
        self._save_results(model_id, data_type, all_results)
        
        # Print summary
        self._print_summary(all_results)
        
        return all_results
    
    def _run_with_retry(
        self,
        model_client,
        conversation: Dict[str, Any],
        category: str
    ) -> Dict[str, Any]:
        """Run test with retry logic"""
        max_retries = self.test_config.get('max_retries', 3)
        retry_delay = self.test_config.get('retry_delay_seconds', 2)
        
        for attempt in range(max_retries):
            result = self.run_single_test(model_client, conversation, category)
            
            if result['success']:
                return result
            
            if attempt < max_retries - 1:
                logger.warning(f"Attempt {attempt + 1} failed, retrying in {retry_delay}s...")
                time.sleep(retry_delay)
        
        return result
    
    def _save_results(
        self,
        model_id: str,
        data_type: str,
        results: List[Dict[str, Any]]
    ):
        """Save results to CSV file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{model_id}_{data_type}_{timestamp}.csv"
        filepath = self.results_dir / filename
        
        df = pd.DataFrame(results)
        df.to_csv(filepath, index=False)
        
        logger.info(f"\n📊 Results saved to: {filepath}")
    
    def _print_summary(self, results: List[Dict[str, Any]]):
        """Print summary statistics"""
        df = pd.DataFrame(results)
        
        total = len(df)
        successful = len(df[df['success'] == True])
        failed = len(df[df['success'] == False])
        
        success_rate = (successful / total * 100) if total > 0 else 0
        avg_latency = df[df['success'] == True]['latency'].mean() if successful > 0 else 0
        
        logger.info(f"\n{'='*60}")
        logger.info("📊 TEST SUMMARY")
        logger.info(f"{'='*60}")
        logger.info(f"Total Tests: {total}")
        logger.info(f"Successful: {successful} ({success_rate:.1f}%)")
        logger.info(f"Failed: {failed}")
        logger.info(f"Avg Latency: {avg_latency:.2f}s")
        
        if successful > 0:
            # Count Met vs Not Met
            value_counts = df[df['success'] == True]['value'].value_counts()
            logger.info(f"\nValue Distribution:")
            for value, count in value_counts.items():
                logger.info(f"  {value}: {count}")
        
        logger.info(f"{'='*60}\n")
    
    def run_full_test(
        self,
        model_id: Optional[str] = None,
        data_types: Optional[List[str]] = None,
        categories: Optional[List[str]] = None
    ):
        """
        Run complete test suite
        
        Args:
            model_id: Specific model to test (None = all enabled)
            data_types: List of data types to test (None = all)
            categories: List of categories to test (None = all)
        """
        # Get models to test
        if model_id:
            models = {model_id: self.config['models'][model_id]}
        else:
            models = self.get_enabled_models()
        
        if not models:
            logger.error("No enabled models found!")
            return
        
        # Get data types to test
        if data_types is None:
            data_types = ['type1', 'type2a', 'type2b']
        
        # Run tests
        for mid, mconfig in models.items():
            for dtype in data_types:
                try:
                    self.run_model_on_data_type(mid, mconfig, dtype, categories)
                except Exception as e:
                    logger.error(f"Error testing {mid} on {dtype}: {e}", exc_info=True)


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run tests
    runner = TestRunner()
    
    # Test only enabled models on type1 data
    runner.run_full_test(data_types=['type1'], categories=['opening'])

