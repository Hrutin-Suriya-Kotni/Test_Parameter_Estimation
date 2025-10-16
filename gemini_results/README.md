# Gemini API Test Results

This directory contains test results from running Gemini API on conversation analysis tasks.

## 📁 Directory Structure

```
gemini_results/
├── type1/              # Overall paragraph data results
├── type2a/             # JSON format data results
└── type2b/             # Labeled paragraph data results
```

## 🎯 Test Configuration

- **Model**: `gemini-2.0-flash-exp`
- **Temperature**: `0.1` (for consistent, deterministic output)
- **Max Output Tokens**: `512`
- **Retry Strategy**: 5 attempts with exponential backoff (2s → 4s → 8s → 16s → 32s)

## 📊 Guidelines Tested

Each data type is tested on 5 conversation guidelines:

1. **Opening** - Greeting and introduction
2. **Closing** - Proper call termination with feedback request
3. **Hold** - Putting customer on hold properly
4. **Reassurance** - Providing customer assurance
5. **Further Assistance** - Asking if customer needs more help

## 📝 Result Files

Result files are named: `{guideline}_results_{timestamp}.csv`

Example: `opening_results_20251016_143022.csv`

### CSV Columns Include:

- `conversation_id` - Unique conversation identifier
- `data_type` - Type of data (type1/type2a/type2b)
- `parameter_tested` - Guideline being tested
- `result_value` - Met/Not Met/Error
- `evidence` - Explanation from the model
- `attempts_used` - Number of retry attempts needed
- `total_latency` - Total time including retries
- `temperature` - API temperature setting
- `max_output_tokens` - Token limit
- `transcript_length` - Length of input conversation
- `response_length` - Length of model response

## 🚀 How to Run Tests

```bash
python run_gemini_full_test.py
```

Make sure you have:
1. Created `.env` file with `GEMINI_API_KEY`
2. Installed: `pip install google-generativeai pandas python-dotenv`

## 📈 Analysis

To analyze results:
```python
import pandas as pd

# Load results
df = pd.read_csv('gemini_results/type1/opening_results_20251016_143022.csv')

# Quick stats
print(df['result_value'].value_counts())
print(f"Success rate: {(df['success'].sum() / len(df)) * 100:.1f}%")
print(f"Average latency: {df['total_latency'].mean():.2f}s")
print(f"Average retries: {df['attempts_used'].mean():.2f}")
```

## 🔄 Retry Logic

The test runner implements exponential backoff for rate limiting:

- **Attempt 1**: Immediate
- **Attempt 2**: Wait 2 seconds
- **Attempt 3**: Wait 4 seconds
- **Attempt 4**: Wait 8 seconds
- **Attempt 5**: Wait 16 seconds
- **Final wait**: 32 seconds (if needed)

This is designed to work with Gemini's free tier rate limits.

## ⚙️ Data Type Context

Each request includes context about the data format:

### Type 1 (Overall Paragraph)
- Continuous narrative without speaker labels
- Natural conversation flow as single text block

### Type 2a (JSON Format)
- Structured data with speaker identification
- Timestamps and turn-by-turn dialogue

### Type 2b (Labeled Paragraph)
- Line-by-line with speaker prefixes
- Format: "Agent: [text]" or "Customer: [text]"

## 📞 Support

For issues or questions, refer to:
- `GEMINI_ENV_SETUP.txt` - Environment setup guide
- `run_gemini_full_test.py` - Main test script
- `prompts.py` - Assessment prompts and guidelines

