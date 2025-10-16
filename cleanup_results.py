#!/usr/bin/env python3
"""
Clean up Server 5 results - keep only latest results in a clean structure
"""

import os
import shutil
import glob
from pathlib import Path

def cleanup_and_organize():
    """
    Organize results into a clean structure:
    MISTRAL_BOOM_BOOM/
      └─ server5_base_mistral/
         ├─ type1/
         │  ├─ opening_results.csv
         │  ├─ closing_results.csv
         │  ├─ reassurance_results.csv
         │  ├─ hold_results.csv
         │  └─ further_assistance_results.csv
         ├─ type2a/
         │  └─ ...
         └─ type2b/
            └─ ...
    """
    
    print("="*70)
    print("🧹 CLEANING UP SERVER 5 RESULTS")
    print("="*70)
    
    base_dir = "MISTRAL_BOOM_BOOM"
    model_name = "server5_base_mistral"
    
    # Create clean output directory
    clean_dir = os.path.join(base_dir, model_name)
    
    data_types = ['type1', 'type2a', 'type2b']
    test_types = ['opening', 'closing', 'reassurance', 'hold', 'further_assistance']
    
    # Track what we're doing
    moved_files = []
    removed_dirs = []
    
    for data_type in data_types:
        print(f"\n📂 Processing {data_type}...")
        
        # Create clean directory for this data type
        clean_data_dir = os.path.join(clean_dir, data_type)
        os.makedirs(clean_data_dir, exist_ok=True)
        
        for test_type in test_types:
            # Find all CSV files for this combination
            pattern = f"{base_dir}/{data_type}/{model_name}/*/{test_type}_results.csv"
            files = sorted(glob.glob(pattern))
            
            if files:
                # Get the latest one (last in sorted order by timestamp)
                latest_file = files[-1]
                
                # New clean location
                clean_file = os.path.join(clean_data_dir, f"{test_type}_results.csv")
                
                # Copy the file
                shutil.copy2(latest_file, clean_file)
                
                print(f"   ✅ {test_type}: Saved latest results")
                print(f"      From: {os.path.basename(os.path.dirname(latest_file))}")
                print(f"      To: {model_name}/{data_type}/{test_type}_results.csv")
                
                moved_files.append(clean_file)
            else:
                print(f"   ⚠️  {test_type}: No results found")
        
        # Now remove all the old timestamp directories for this data type
        old_dirs_pattern = f"{base_dir}/{data_type}/{model_name}/*"
        old_dirs = sorted(glob.glob(old_dirs_pattern))
        
        for old_dir in old_dirs:
            if os.path.isdir(old_dir):
                try:
                    shutil.rmtree(old_dir)
                    removed_dirs.append(old_dir)
                except Exception as e:
                    print(f"   ⚠️  Could not remove {old_dir}: {e}")
    
    # Summary
    print("\n" + "="*70)
    print("📊 CLEANUP SUMMARY")
    print("="*70)
    print(f"✅ Organized {len(moved_files)} result files")
    print(f"🗑️  Removed {len(removed_dirs)} timestamp directories")
    print()
    print("📁 NEW CLEAN STRUCTURE:")
    print(f"   {base_dir}/{model_name}/")
    for data_type in data_types:
        print(f"      └─ {data_type}/")
        for test_type in test_types:
            file_path = os.path.join(clean_dir, data_type, f"{test_type}_results.csv")
            if os.path.exists(file_path):
                print(f"         ├─ {test_type}_results.csv ✅")
            else:
                print(f"         ├─ {test_type}_results.csv ❌")
    
    print("\n" + "="*70)
    print("✨ CLEANUP COMPLETE!")
    print("="*70)
    print(f"\n📂 All final results are now in: {clean_dir}/")
    print()

if __name__ == "__main__":
    cleanup_and_organize()

