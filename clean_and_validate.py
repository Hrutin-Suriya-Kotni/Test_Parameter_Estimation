import pandas as pd
import sys
import os

# Add project root to sys.path
sys.path.append('/Users/cleveres_tidiot/Documents/Vocab_AI/Parameter_Testing')

from ultimate_framework.json_extractor import JSONExtractor

INPUT_FILE = '/Users/cleveres_tidiot/Documents/Vocab_AI/Parameter_Testing/20_testing_type2b/FULL_results_not_Validated.csv'
OUTPUT_FILE = '/Users/cleveres_tidiot/Documents/Vocab_AI/Parameter_Testing/20_testing_type2b/QA_Validated_Results.csv'

def clean_dataframe(df):
    status_cols = [c for c in df.columns if '_status' in c]
    
    print(f"Processing {len(df)} rows...")
    fixed_counts = 0
    
    for idx, row in df.iterrows():
        row_changed = False
        for col in status_cols:
            status_val = row[col]
            # Check for Parse Error (exact or substring)
            if isinstance(status_val, str) and 'Parse Error' in status_val:
                # Find corresponding evidence column
                evidence_col = col.replace('_status', '_evidence')
                evidence_val = row[evidence_col]
                if pd.isna(evidence_val):
                    print(f"Skipping row {idx} {col}: Evidence is NaN")
                    continue
                    
                # Use project's robust extractor
                # extract returns (json_dict, error_msg)
                try:
                    data, error = JSONExtractor.extract(str(evidence_val))
                    if data and "Value" in data:
                        val = data["Value"]
                        ev = data.get("Evidence", "")
                        
                        df.at[idx, col] = val
                        df.at[idx, evidence_col] = ev
                        row_changed = True
                        print(f"Fixed {col} at row {idx}: {val}")
                    else:
                        print(f"Extraction returned no data for row {idx} {col}. Error: {error}")
                        # print(f"Evidence snippet: {str(evidence_val)[:50]}...")
                        
                except Exception as e:
                    print(f"Extraction failed for row {idx} {col}: {e}")
        
        if row_changed:
            fixed_counts += 1
            
    print(f"Fixed Parse Errors in {fixed_counts} rows.")
    
    # Standardize Status
    for col in status_cols:
        # Convert to Title Case, strip whitespace
        df[col] = df[col].astype(str).str.strip().str.title()
        
        # Replace remaining errors
        df[col] = df[col].replace({'Nan': 'Error', 'Parse Error': 'Error'})
        
    return df

def main():
    df = pd.read_csv(INPUT_FILE)
    print(f"Original Shape: {df.shape}")
    
    cleaned_df = clean_dataframe(df)
    
    # Verify unique statuses
    status_cols = [c for c in cleaned_df.columns if '_status' in c]
    for col in status_cols:
        print(f"Unique values in {col}: {cleaned_df[col].unique()}")
        
    cleaned_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
