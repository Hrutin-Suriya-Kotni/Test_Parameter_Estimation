import pandas as pd
import sys
sys.path.append('/Users/cleveres_tidiot/Documents/Vocab_AI/Parameter_Testing')
from ultimate_framework.json_extractor import JSONExtractor

INPUT_FILE = '/Users/cleveres_tidiot/Documents/Vocab_AI/Parameter_Testing/20_testing_type2b/FULL_results_not_Validated.csv'

df = pd.read_csv(INPUT_FILE)
row_idx = 178
if len(df) > row_idx:
    row = df.iloc[row_idx]
    print(f"Row {row_idx} Status/Evidence cols:")
    for col in df.columns:
        if '_status' in col:
            s_val = row[col]
            e_col = col.replace('_status', '_evidence')
            e_val = row[e_col]
            print(f"{col}: {s_val}")
            print(f"{e_col}: {repr(e_val)}")
            
            if isinstance(s_val, str) and 'Parse Error' in s_val:
                print(f"Testing extraction for {e_col}...")
                data, error = JSONExtractor.extract(str(e_val))
                print(f"Extraction result: {data}")
                print(f"Extraction error: {error}")
else:
    print(f"Row {row_idx} out of bounds (max {len(df)-1})")
