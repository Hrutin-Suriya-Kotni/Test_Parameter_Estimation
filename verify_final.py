import pandas as pd

df = pd.read_csv('/Users/cleveres_tidiot/Documents/Vocab_AI/Parameter_Testing/20_testing_type2b/QA_Validated_Results.csv')
print(f"Final Shape: {df.shape}")
print("-" * 20)
for col in df.columns:
    if '_status' in col:
        print(f"{col} unique: {df[col].unique()}")

print("-" * 20)
print(f"NaN count:\n{df.isna().sum()}")
