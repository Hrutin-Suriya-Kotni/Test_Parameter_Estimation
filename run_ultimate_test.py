#!/usr/bin/env python3
"""
Main entry point for the Ultimate Testing Framework
Run tests easily from command line
"""

import argparse
import logging
import sys
from pathlib import Path

# Add ultimate_framework to path
sys.path.insert(0, str(Path(__file__).parent))

from ultimate_framework.test_runner import TestRunner


def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('ultimate_test.log')
        ]
    )


def main():
    parser = argparse.ArgumentParser(
        description='Ultimate Testing Framework - Multi-Model Call Center Analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test all enabled models on all data types
  python run_ultimate_test.py
  
  # Test specific model only
  python run_ultimate_test.py --model multi_gpu_v100
  
  # Test specific data type(s)
  python run_ultimate_test.py --data-types type1 type2a
  
  # Test specific categories
  python run_ultimate_test.py --categories opening closing
  
  # Combine options
  python run_ultimate_test.py --model multi_gpu_v100 --data-types type1 --categories opening
  
  # Verbose output
  python run_ultimate_test.py --verbose
        """
    )
    
    parser.add_argument(
        '--model',
        type=str,
        help='Specific model to test (from config.yaml). If not specified, tests all enabled models.'
    )
    
    parser.add_argument(
        '--data-types',
        nargs='+',
        choices=['type1', 'type2a', 'type2b'],
        help='Data types to test. Default: all types'
    )
    
    parser.add_argument(
        '--categories',
        nargs='+',
        choices=['opening', 'closing', 'hold', 'reassurance', 'further_assistance'],
        help='Categories to test. Default: all categories'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file. Default: config.yaml'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose (DEBUG) logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    logger.info("="*70)
    logger.info("🚀 ULTIMATE TESTING FRAMEWORK")
    logger.info("="*70)
    
    try:
        # Initialize test runner
        runner = TestRunner(config_path=args.config)
        
        # Run tests
        runner.run_full_test(
            model_id=args.model,
            data_types=args.data_types,
            categories=args.categories
        )
        
        logger.info("\n" + "="*70)
        logger.info("✅ Testing Complete!")
        logger.info("="*70)
        
    except KeyboardInterrupt:
        logger.warning("\n\n⚠️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n\n❌ Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

