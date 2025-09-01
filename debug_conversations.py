#!/usr/bin/env python3
"""
Debug script to analyze conversation failures
"""

import pandas as pd
from data_loader import data_loader
from api_client import api_client

def analyze_conversation_lengths():
    """Analyze conversation lengths to identify problematic ones"""
    print("Analyzing conversation lengths...")
    
    transcript_df, _ = data_loader.load_data()
    
    # Add length column
    transcript_df['length'] = transcript_df['transcript'].str.len()
    
    # Sort by length
    sorted_df = transcript_df.sort_values('length', ascending=False)
    
    print(f"\nTotal conversations: {len(transcript_df)}")
    print(f"Average length: {transcript_df['length'].mean():.0f} characters")
    print(f"Min length: {transcript_df['length'].min()} characters")
    print(f"Max length: {transcript_df['length'].max()} characters")
    
    print("\nLongest conversations (top 10):")
    for i, row in sorted_df.head(10).iterrows():
        print(f"ID: {row['request_id'][:8]}... | Length: {row['length']} chars")
    
    print("\nShortest conversations (bottom 5):")
    for i, row in sorted_df.tail(5).iterrows():
        print(f"ID: {row['request_id'][:8]}... | Length: {row['length']} chars")
    
    return sorted_df

def test_specific_conversations():
    """Test specific conversations to see which ones fail"""
    print("\n" + "="*60)
    print("Testing specific conversations...")
    print("="*60)
    
    transcript_df, _ = data_loader.load_data()
    
    # Test the longest conversation
    longest_conv = transcript_df.loc[transcript_df['transcript'].str.len().idxmax()]
    print(f"\nTesting longest conversation (ID: {longest_conv['request_id'][:8]}...)")
    print(f"Length: {len(longest_conv['transcript'])} characters")
    
    # Simple test with just the conversation
    test_prompt = longest_conv['transcript'][:500] + "... [truncated]"
    response = api_client.call_api(user_prompt=test_prompt)
    
    if response:
        print("✅ Long conversation test successful (truncated)")
    else:
        print("❌ Long conversation test failed (truncated)")
    
    # Test a medium conversation
    medium_conv = transcript_df.iloc[len(transcript_df)//2]
    print(f"\nTesting medium conversation (ID: {medium_conv['request_id'][:8]}...)")
    print(f"Length: {len(medium_conv['transcript'])} characters")
    
    response = api_client.call_api(user_prompt=medium_conv['transcript'])
    
    if response:
        print("✅ Medium conversation test successful")
    else:
        print("❌ Medium conversation test failed")
    
    # Test the shortest conversation
    shortest_conv = transcript_df.loc[transcript_df['transcript'].str.len().idxmin()]
    print(f"\nTesting shortest conversation (ID: {shortest_conv['request_id'][:8]}...)")
    print(f"Length: {len(shortest_conv['transcript'])} characters")
    
    response = api_client.call_api(user_prompt=shortest_conv['transcript'])
    
    if response:
        print("✅ Short conversation test successful")
    else:
        print("❌ Short conversation test failed")

def find_failing_conversations():
    """Find which specific conversations are failing"""
    print("\n" + "="*60)
    print("Identifying failing conversations...")
    print("="*60)
    
    transcript_df, _ = data_loader.load_data()
    
    # Sort by length (longest first)
    sorted_df = transcript_df.sort_values('transcript', key=lambda x: x.str.len(), ascending=False)
    
    failing_ids = []
    
    for i, row in sorted_df.iterrows():
        print(f"\nTesting conversation {i+1}/{len(sorted_df)} (ID: {row['request_id'][:8]}...)")
        print(f"Length: {len(row['transcript'])} characters")
        
        # Simple test
        response = api_client.call_api(user_prompt=row['transcript'][:100] + " [test]")
        
        if response:
            print("✅ API call successful")
        else:
            print("❌ API call failed")
            failing_ids.append(row['request_id'])
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: {len(failing_ids)} conversations failed out of {len(sorted_df)}")
    print(f"{'='*60}")
    
    if failing_ids:
        print("Failing conversation IDs:")
        for conv_id in failing_ids:
            print(f"  - {conv_id}")
    
    return failing_ids

def main():
    """Main debug function"""
    print("=" * 60)
    print("CRED Conversation Debug Tool")
    print("=" * 60)
    
    # Analyze conversation lengths
    sorted_df = analyze_conversation_lengths()
    
    # Test specific conversations
    test_specific_conversations()
    
    # Find failing conversations
    failing_ids = find_failing_conversations()
    
    print("\n" + "="*60)
    print("RECOMMENDATIONS:")
    print("="*60)
    
    if failing_ids:
        print("1. Your API is having issues with certain conversations")
        print("2. Consider increasing API timeout or reducing conversation length")
        print("3. Check if your OpenChat API can handle the conversation volume")
        print("4. Consider processing in smaller batches")
    else:
        print("1. All conversations are working with the API")
        print("2. The issue might be with the assessment prompts")
        print("3. Try running the main analysis again")

if __name__ == "__main__":
    main() 