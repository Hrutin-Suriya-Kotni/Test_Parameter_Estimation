#!/usr/bin/env python3
"""
Script to track and store failed conversations in error results folder
"""

import pandas as pd
import os
import json
from datetime import datetime
from data_loader import data_loader
from processor import processor
from api_client import api_client

def create_error_folder():
    """Create error results folder if it doesn't exist"""
    error_dir = "error_results"
    if not os.path.exists(error_dir):
        os.makedirs(error_dir)
        print(f"Created error results directory: {error_dir}")
    return error_dir

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

def find_failed_conversations(transcript_df, existing_results):
    """Find conversations that failed to process"""
    all_request_ids = set(transcript_df['request_id'].tolist())
    
    failed_conversations = {}
    for assessment_type in ['opening', 'closing', 'reassurance', 'hold', 'further_assistance']:
        if assessment_type in existing_results:
            failed_ids = all_request_ids - existing_results[assessment_type]
        else:
            failed_ids = all_request_ids
        
        failed_conversations[assessment_type] = transcript_df[
            transcript_df['request_id'].isin(failed_ids)
        ].copy()
        
        print(f"{assessment_type}: {len(failed_conversations[assessment_type])} failed conversations")
    
    return failed_conversations

def test_conversations_and_track_failures(failed_conversations):
    """Test conversations and track which ones fail"""
    error_dir = create_error_folder()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    all_failures = {}
    
    for assessment_type, df in failed_conversations.items():
        if len(df) == 0:
            continue
            
        print(f"\n{'='*50}")
        print(f"Testing {len(df)} failed conversations for {assessment_type}")
        print(f"{'='*50}")
        
        failures = []
        
        for index, row in df.iterrows():
            conversation = row["transcript"]
            request_id = row["request_id"]
            
            print(f"Testing conversation {index + 1}/{len(df)} (ID: {request_id[:8]}...)")
            print(f"Length: {len(conversation)} characters")
            
            # Test with a simple prompt
            test_prompt = conversation[:500] + " [test]"
            response = api_client.call_api(user_prompt=test_prompt)
            
            if response:
                print("✅ API call successful")
            else:
                print("❌ API call failed")
                failures.append({
                    'request_id': request_id,
                    'conversation_length': len(conversation),
                    'assessment_type': assessment_type,
                    'error_type': 'API_500_ERROR',
                    'timestamp': datetime.now().isoformat(),
                    'conversation_preview': conversation[:200] + "..." if len(conversation) > 200 else conversation
                })
        
        all_failures[assessment_type] = failures
        print(f"Failed conversations for {assessment_type}: {len(failures)}")
    
    return all_failures

def save_failure_reports(all_failures, error_dir, timestamp):
    """Save failure reports to error results folder"""
    
    # Save individual assessment type failures
    for assessment_type, failures in all_failures.items():
        if failures:
            # Save as CSV
            df = pd.DataFrame(failures)
            csv_filename = f"{error_dir}/{assessment_type}_failures_{timestamp}.csv"
            df.to_csv(csv_filename, index=False)
            print(f"✅ Saved {assessment_type} failures to: {csv_filename}")
            
            # Save as JSON for detailed analysis
            json_filename = f"{error_dir}/{assessment_type}_failures_{timestamp}.json"
            with open(json_filename, 'w') as f:
                json.dump(failures, f, indent=2)
            print(f"✅ Saved {assessment_type} failures (JSON) to: {json_filename}")
    
    # Save combined failure report
    all_failures_flat = []
    for assessment_type, failures in all_failures.items():
        all_failures_flat.extend(failures)
    
    if all_failures_flat:
        # Combined CSV
        combined_df = pd.DataFrame(all_failures_flat)
        combined_csv = f"{error_dir}/all_failures_{timestamp}.csv"
        combined_df.to_csv(combined_csv, index=False)
        print(f"✅ Saved combined failures to: {combined_csv}")
        
        # Combined JSON
        combined_json = f"{error_dir}/all_failures_{timestamp}.json"
        with open(combined_json, 'w') as f:
            json.dump(all_failures_flat, f, indent=2)
        print(f"✅ Saved combined failures (JSON) to: {combined_json}")
        
        # Summary report
        summary = {
            'timestamp': timestamp,
            'total_failures': len(all_failures_flat),
            'failures_by_type': {k: len(v) for k, v in all_failures.items()},
            'unique_conversations': len(set(f['request_id'] for f in all_failures_flat)),
            'error_types': list(set(f['error_type'] for f in all_failures_flat))
        }
        
        summary_file = f"{error_dir}/failure_summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"✅ Saved failure summary to: {summary_file}")

def create_retry_script(all_failures, error_dir, timestamp):
    """Create a script to retry failed conversations"""
    if not any(all_failures.values()):
        return
    
    retry_script = f"{error_dir}/retry_failed_conversations_{timestamp}.py"
    
    script_content = f'''#!/usr/bin/env python3
"""
Auto-generated script to retry failed conversations
Generated on: {timestamp}
"""

import pandas as pd
from data_loader import data_loader
from processor import processor

def retry_failed_conversations():
    """Retry conversations that failed in the previous run"""
    
    # Load the original data
    transcript_df, _ = data_loader.load_data()
    
    # Failed conversation IDs from the analysis
    failed_ids = {list(set(f['request_id'] for failures in {all_failures}.values() for f in failures))}
    
    # Filter to only failed conversations
    failed_df = transcript_df[transcript_df['request_id'].isin(failed_ids)].copy()
    
    print(f"Retrying {len(failed_df)} failed conversations...")
    
    # Process each assessment type
    for assessment_type in ['opening', 'closing', 'reassurance', 'hold', 'further_assistance']:
        print(f"\\nProcessing {assessment_type}...")
        
        # Process with longer timeouts and more retries
        results, failed_chats = processor.process_conversation_with_prompt(
            failed_df, assessment_type
        )
        
        # Multiple retry attempts
        for attempt in range(3):
            if failed_chats:
                print(f"Retry attempt {attempt + 1} for {assessment_type}...")
                retry_results = processor.process_failed_chats(failed_chats, assessment_type)
                results.extend(retry_results)
                failed_chats = [(idx, rid, conv) for idx, rid, conv in failed_chats 
                               if not any(r['request_id'] == rid for r in retry_results)]
        
        # Save results
        if results:
            df = pd.DataFrame(results)
            df.to_csv(f"results/{assessment_type}_retry_{timestamp}.csv", index=False)
            print(f"Saved {len(results)} retry results for {assessment_type}")

if __name__ == "__main__":
    retry_failed_conversations()
'''
    
    with open(retry_script, 'w') as f:
        f.write(script_content)
    
    print(f"✅ Created retry script: {retry_script}")

def main():
    """Main function"""
    print("=" * 60)
    print("Tracking Failed Conversations")
    print("=" * 60)
    
    # Load data
    print("Loading conversation data...")
    transcript_df, _ = data_loader.load_data()
    print(f"Total conversations in dataset: {len(transcript_df)}")
    
    # Load existing results
    print("\nLoading existing results...")
    existing_results = load_existing_results()
    
    # Find failed conversations
    print("\nFinding failed conversations...")
    failed_conversations = find_failed_conversations(transcript_df, existing_results)
    
    total_failed = sum(len(df) for df in failed_conversations.values())
    if total_failed == 0:
        print("✅ All conversations have been processed successfully!")
        return
    
    print(f"\nTotal failed conversations: {total_failed}")
    
    # Test and track failures
    print("\nTesting failed conversations...")
    all_failures = test_conversations_and_track_failures(failed_conversations)
    
    # Save failure reports
    error_dir = create_error_folder()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("\nSaving failure reports...")
    save_failure_reports(all_failures, error_dir, timestamp)
    
    # Create retry script
    print("\nCreating retry script...")
    create_retry_script(all_failures, error_dir, timestamp)
    
    # Summary
    print("\n" + "=" * 60)
    print("FAILURE TRACKING COMPLETE")
    print("=" * 60)
    
    total_failures = sum(len(failures) for failures in all_failures.values())
    print(f"Total failures tracked: {total_failures}")
    
    for assessment_type, failures in all_failures.items():
        print(f"{assessment_type.upper()}: {len(failures)} failures")
    
    print(f"\nAll failure reports saved in: {error_dir}/")
    print("You can use the generated retry script to attempt processing failed conversations again.")

if __name__ == "__main__":
    main() 