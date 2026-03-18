import pandas as pd

try:
    df = pd.read_csv('/Users/cleveres_tidiot/Documents/Vocab_AI/Parameter_Testing/20_testing_type2b/FULL_results_not_Validated.csv')
    print('Shape:', df.shape)
    print('Unique IDs:', df['conversation_id'].nunique())
    print('Unique Guidelines:', df['guideline'].unique())
    print('Unique Guidelines Count:', df['guideline'].nunique())
    
    # Check for specific error strings
    print('Parse Errors per col:')
    print((df == 'Parse Error').sum())
    
    print('NaNs per col:')
    print(df.isna().sum())
    
    # Check if 0 is agent or customer in transcript
    # Just looking at the first row's transcript
    first_transcript = df['transcript'].iloc[0]
    print('First Transcript snippet:', first_transcript[:100])

except Exception as e:
    print(f"Error: {e}")
