#!/usr/bin/env python3
"""
Script to process remaining conversations that failed in the previous run
"""

import pandas as pd
import os
from datetime import datetime
from data_loader import data_loader
from processor import processor
from api_client import api_client

def load_existing_results():
    """Load existing results to see what was already processed"""
    results_dir = "results"
    if not os.path.exists(results_dir):
        return {}
    
    existing_results = {}
    for file in os.listdir(results_dir):
        if file.endswith('.csv') and 'combined' not in file:
            assessment_type = file.split('_')[0]
            df = pd.read_csv(os.path.join(results_dir, file))
            existing_results[assessment_type] = set(df['request_id'].tolist())
    
    return existing_results

def find_missing_conversations(transcript_df, existing_results):
    """Find conversations that weren't processed"""
    all_request_ids = set(transcript_df['request_id'].tolist())
    
    missing_conversations = {}
    for assessment_type in ['opening', 'closing', 'reassurance', 'hold', 'further_assistance']:
        if assessment_type in existing_results:
            missing_ids = all_request_ids - existing_results[assessment_type]
        else:
            missing_ids = all_request_ids
        
        missing_conversations[assessment_type] = transcript_df[
            transcript_df['request_id'].isin(missing_ids)
        ].copy()
        
        print(f"{assessment_type}: {len(missing_conversations[assessment_type])} missing conversations")
    
    return missing_conversations

def process_missing_conversations(missing_conversations):
    """Process the missing conversations"""
    results = {}
    
    for assessment_type, df in missing_conversations.items():
        if len(df) == 0:
            print(f"No missing conversations for {assessment_type}")
            continue
            
        print(f"\n{'='*50}")
        print(f"Processing {len(df)} missing conversations for {assessment_type}")
        print(f"{'='*50}")
        
        # Process with longer timeout for longer conversations
        results_list, failed_chats = processor.process_conversation_with_prompt(
            df, assessment_type
        )
        
        # Retry failed chats with more attempts
        retry_results = processor.process_failed_chats(failed_chats, assessment_type)
        
        # Merge results
        final_df = processor.merge_results_and_retries(results_list, retry_results)
        results[assessment_type] = final_df
        
        print(f"Completed {assessment_type}: {len(final_df)} successful assessments")
    
    return results

def merge_with_existing_results(new_results, existing_results):
    """Merge new results with existing ones"""
    results_dir = "results"
    merged_results = {}
    
    for assessment_type, new_df in new_results.items():
        if len(new_df) == 0:
            continue
            
        # Load existing results
        existing_file = None
        for file in os.listdir(results_dir):
            if file.startswith(assessment_type) and file.endswith('.csv'):
                existing_file = os.path.join(results_dir, file)
                break
        
        if existing_file:
            existing_df = pd.read_csv(existing_file)
            # Combine existing and new results
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            # Remove duplicates based on request_id
            combined_df = combined_df.drop_duplicates(subset=['request_id'], keep='first')
        else:
            combined_df = new_df
        
        merged_results[assessment_type] = combined_df
    
    return merged_results

def save_merged_results(merged_results):
    """Save the merged results"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for assessment_type, df in merged_results.items():
        filename = f"results/{assessment_type}_results_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Saved {assessment_type} results to: {filename}")
        print(f"   Total assessments: {len(df)}")

def main():
    """Main function"""
    print("=" * 60)
    print("Processing Remaining Conversations")
    print("=" * 60)
    
    # Load data
    print("Loading conversation data...")
    transcript_df, _ = data_loader.load_data()
    print(f"Total conversations in dataset: {len(transcript_df)}")
    
    # Load existing results
    print("\nLoading existing results...")
    existing_results = load_existing_results()
    
    # Find missing conversations
    print("\nFinding missing conversations...")
    missing_conversations = find_missing_conversations(transcript_df, existing_results)
    
    total_missing = sum(len(df) for df in missing_conversations.values())
    if total_missing == 0:
        print("✅ All conversations have been processed!")
        return
    
    print(f"\nTotal missing conversations: {total_missing}")
    
    # Process missing conversations
    print("\nProcessing missing conversations...")
    new_results = process_missing_conversations(missing_conversations)
    
    # Merge with existing results
    print("\nMerging with existing results...")
    merged_results = merge_with_existing_results(new_results, existing_results)
    
    # Save results
    print("\nSaving merged results...")
    save_merged_results(merged_results)
    
    # Summary
    print("\n" + "=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)
    for assessment_type, df in merged_results.items():
        print(f"{assessment_type.upper()}: {len(df)} total assessments")

if __name__ == "__main__":
    main() 