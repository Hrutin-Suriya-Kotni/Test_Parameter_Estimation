# Server 5 Base Mistral - Test Results

## API Information
- **Endpoint**: `http://27.111.72.51:8000/generate`
- **Model**: Base Mistral
- **API Type**: Simple prompt-response format

## Test Configuration
- **Date**: October 11, 2025
- **Conversations per test**: 20
- **Total conversations**: 300
- **Data types**: type1, type2a, type2b
- **Guidelines tested**: Opening, Closing, Reassurance, Hold, Further Assistance

## Folder Structure

```
server5_base_mistral/
├── type1/                          # Overall paragraph format
│   ├── opening_results.csv
│   ├── closing_results.csv
│   ├── reassurance_results.csv
│   ├── hold_results.csv
│   └── further_assistance_results.csv
│
├── type2a/                         # JSON format
│   ├── opening_results.csv
│   ├── closing_results.csv
│   ├── reassurance_results.csv
│   ├── hold_results.csv
│   └── further_assistance_results.csv
│
└── type2b/                         # Labeled paragraph format
    ├── opening_results.csv
    ├── closing_results.csv
    ├── reassurance_results.csv
    ├── hold_results.csv
    └── further_assistance_results.csv
```

## Overall Performance Summary

### API Reliability
- **Success Rate**: 86.0% (258/300)
- **Failed Calls**: 42 (14%)
- **Average Latency**: 11.91 seconds

### Results Distribution (from successful calls)
- **Met**: 135 (52.3%)
- **Not Met**: 123 (47.7%)

### Performance by Guideline

| Guideline | Success Rate | Met | Not Met | Notes |
|-----------|--------------|-----|---------|-------|
| Opening | 100.0% | 25 | 35 | Perfect API reliability |
| Closing | 81.7% | 47 | 2 | High compliance rate |
| Reassurance | 88.3% | 47 | 6 | High compliance rate |
| Hold | 80.0% | 8 | 40 | Low compliance - agents rarely follow hold guidelines |
| Further Assistance | 80.0% | 8 | 40 | Low compliance - agents rarely ask correctly |

## Key Findings

### ✅ Strengths
1. **Excellent API reliability** for Opening guideline (100%)
2. **High compliance** for Closing and Reassurance guidelines (~90% met)
3. **Consistent latency** averaging ~12 seconds

### ⚠️ Issues
1. **Parse failures** (14%) - Server occasionally generates repetitive text on long transcripts
2. **Low Hold/Further Assistance compliance** - Agents don't consistently follow these guidelines
3. **Type2b performance** slightly lower than Type1 and Type2a

## CSV File Columns

Each CSV file contains:
- `conversation_id` - Unique conversation identifier
- `data_type` - Data format (type1/type2a/type2b)
- `parameter_tested` - Guideline being evaluated
- `success` - Whether API call succeeded
- `result_value` - "Met" or "Not Met"
- `evidence` - Explanation from the model
- `total_latency` - Response time in seconds
- `api_temperature` - Temperature setting (0.1)
- `api_max_tokens` - Token limit (512)
- `transcript_length` - Length of conversation
- Additional metadata fields

## Usage

To analyze results programmatically:

```python
import pandas as pd

# Load a specific result file
df = pd.read_csv('type1/opening_results.csv')

# View success rate
success_rate = df['success'].mean() * 100
print(f"Success Rate: {success_rate:.1f}%")

# Count Met vs Not Met
met_count = (df['result_value'] == 'Met').sum()
not_met_count = (df['result_value'] == 'Not Met').sum()
print(f"Met: {met_count}, Not Met: {not_met_count}")
```

## Next Steps

Consider testing:
1. Server 3 (OpenChat Mistral) for comparison
2. Gemini API for baseline performance
3. Adjusting temperature/token limits to reduce failures
4. Shorter prompts to avoid repetitive text generation



 cd /Users/cleveres_tidiot/Documents/Vocab_AI/Parameter_Testing && python3 view_server5_summary.py
================================================================================
SERVER 5 FINE-TUNED CRED MISTRAL - RESULTS SUMMARY
================================================================================


────────────────────────────────────────────────────────────────────────────────
📂 TYPE1
────────────────────────────────────────────────────────────────────────────────
🟢 Opening              | Success: 20/20 (100.0%) | Met:  5 | Not Met: 15 | Latency: 14.68s
🟢 Closing              | Success: 18/20 ( 90.0%) | Met: 18 | Not Met:  0 | Latency:  9.30s
🟢 Reassurance          | Success: 19/20 ( 95.0%) | Met: 17 | Not Met:  2 | Latency: 10.16s
🟡 Hold                 | Success: 16/20 ( 80.0%) | Met:  3 | Not Met: 13 | Latency: 13.63s
🟢 Further Assistance   | Success: 18/20 ( 90.0%) | Met:  2 | Not Met: 16 | Latency: 11.29s

────────────────────────────────────────────────────────────────────────────────
📂 TYPE2A
────────────────────────────────────────────────────────────────────────────────
🟢 Opening              | Success: 20/20 (100.0%) | Met: 14 | Not Met:  6 | Latency: 16.92s
🟡 Closing              | Success: 16/20 ( 80.0%) | Met: 15 | Not Met:  1 | Latency: 10.23s
🟡 Reassurance          | Success: 17/20 ( 85.0%) | Met: 15 | Not Met:  2 | Latency: 12.62s
🟡 Hold                 | Success: 17/20 ( 85.0%) | Met:  2 | Not Met: 15 | Latency: 11.15s
🟡 Further Assistance   | Success: 17/20 ( 85.0%) | Met:  3 | Not Met: 14 | Latency: 11.76s

────────────────────────────────────────────────────────────────────────────────
📂 TYPE2B
────────────────────────────────────────────────────────────────────────────────
🟢 Opening              | Success: 20/20 (100.0%) | Met:  6 | Not Met: 14 | Latency: 15.02s
🟡 Closing              | Success: 15/20 ( 75.0%) | Met: 14 | Not Met:  1 | Latency:  9.78s
🟡 Reassurance          | Success: 17/20 ( 85.0%) | Met: 15 | Not Met:  2 | Latency: 14.66s
🟡 Hold                 | Success: 15/20 ( 75.0%) | Met:  3 | Not Met: 12 | Latency: 10.14s
🔴 Further Assistance   | Success: 13/20 ( 65.0%) | Met:  3 | Not Met: 10 | Latency:  3.36s

================================================================================
OVERALL SUMMARY
================================================================================
Total Conversations: 300
Success Rate: 258/300 (86.0%)
Met: 135 (52.3%)
Not Met: 123 (47.7%)
Average Latency: 11.91s
================================================================================