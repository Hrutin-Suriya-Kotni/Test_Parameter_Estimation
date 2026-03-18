import pandas as pd

df = pd.read_csv('/Users/cleveres_tidiot/Documents/Vocab_AI/Parameter_Testing/20_testing_type2b/FULL_results_not_Validated.csv')

# Check for duplicates
duplicates = df[df.duplicated(subset=['conversation_id', 'guideline'], keep=False)]
if not duplicates.empty:
    print(f"Found {len(duplicates)} duplicate rows (based on conversation_id + guideline).")
    print(duplicates[['conversation_id', 'guideline']].head(10))
    # Show counts
    print("\nDuplicate Counts:")
    print(duplicates.groupby(['conversation_id', 'guideline']).size())
else:
    print("No duplicates found based on conversation_id + guideline.")

# Check counts per guideline
print("\nCounts per guideline:")
print(df['guideline'].value_counts())

# Check counts per conversation
print("\nCounts per conversation (first 5):")
print(df['conversation_id'].value_counts().head(5))
