#!/usr/bin/env python3
"""
CRED Conversation Analysis Tool

This script analyzes CRED customer service conversations using a local OpenChat API
to assess agent performance across multiple parameters.
"""

import os
import sys
import pandas as pd
from datetime import datetime
from typing import Optional

# Import our modules
from config import CRED_DATA_PATH
from api_client import api_client
from data_loader import data_loader
from processor import processor

def test_api_connection():
    """Test if the OpenChat API is accessible"""
    print("Testing API connection...")
    if api_client.test_connection():
        print("✅ API connection successful!")
        return True
    else:
        print("❌ API connection failed!")
        print("Please ensure your OpenChat API is running at the configured URL")
        return False

def setup_data_directory():
    """Create data directory if it doesn't exist"""
    if not os.path.exists(CRED_DATA_PATH):
        os.makedirs(CRED_DATA_PATH)
        print(f"Created data directory: {CRED_DATA_PATH}")
        print(f"Please place your Excel file in: {CRED_DATA_PATH}")
        return False
    return True

def load_and_prepare_data():
    """Load and prepare the conversation data"""
    try:
        print("Loading CRED conversation data...")
        transcript_df, primary_info_df = data_loader.load_data()
        
        # Optional: Remove short calls (uncomment if needed)
        # transcript_df = data_loader.remove_short_calls(transcript_df, primary_info_df)
        
        print(f"✅ Successfully loaded {len(transcript_df)} conversations")
        return transcript_df
        
    except FileNotFoundError:
        print(f"❌ Excel file not found in {CRED_DATA_PATH}")
        print("Please ensure the file is in the correct location")
        return None
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def save_results(results: dict, output_dir: str = "results"):
    """Save results to CSV files"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for assessment_type, df in results.items():
        filename = f"{output_dir}/{assessment_type}_results_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Saved {assessment_type} results to: {filename}")
    
    # Save combined results
    combined_filename = f"{output_dir}/combined_results_{timestamp}.csv"
    combined_df = pd.concat(results.values(), keys=results.keys(), names=['assessment_type'])
    combined_df.to_csv(combined_filename)
    print(f"✅ Saved combined results to: {combined_filename}")

def main():
    """Main execution function"""
    print("=" * 60)
    print("CRED Conversation Analysis Tool")
    print("=" * 60)
    
    # Test API connection
    if not test_api_connection():
        return
    
    # Setup data directory
    if not setup_data_directory():
        return
    
    # Load data
    transcript_df = load_and_prepare_data()
    if transcript_df is None:
        return
    
    # Ask user for processing options
    print("\nProcessing Options:")
    print("1. Process all conversations")
    print("2. Process sample (first 5 conversations)")
    print("3. Process custom number of conversations")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    max_conversations = None
    if choice == "2":
        max_conversations = 5
        print("Processing first 5 conversations...")
    elif choice == "3":
        try:
            max_conversations = int(input("Enter number of conversations to process: "))
            print(f"Processing first {max_conversations} conversations...")
        except ValueError:
            print("Invalid input. Processing all conversations...")
    else:
        print("Processing all conversations...")
    
    # Process assessments
    print("\nStarting conversation analysis...")
    try:
        results = processor.process_all_assessments(transcript_df, max_conversations)
        
        # Save results
        print("\nSaving results...")
        save_results(results)
        
        # Display summary
        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)
        for assessment_type, df in results.items():
            print(f"{assessment_type.upper()}: {len(df)} assessments completed")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")

if __name__ == "__main__":
    main() 