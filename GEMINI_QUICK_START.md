# 🚀 Gemini API Testing - Quick Start Guide

## 📋 What Has Been Created

### 1. Folder Structure
```
gemini_results/
├── README.md           # Documentation for results
├── type1/              # Overall paragraph results
├── type2a/             # JSON format results
└── type2b/             # Labeled paragraph results
```

### 2. Test Script
- **File**: `run_gemini_full_test.py`
- **Purpose**: Comprehensive testing of Gemini API on all data types and guidelines

### 3. Environment Setup Guide
- **File**: `GEMINI_ENV_SETUP.txt`
- **Purpose**: Instructions for setting up your `.env` file with Gemini API key

---

## ⚙️ Configuration Summary

### API Settings
- **Model**: `gemini-2.0-flash-exp`
- **Temperature**: `0.1` (for consistent, deterministic output)
- **Max Output Tokens**: `512` (optimized for your response size)
- **Retry Strategy**: 5 attempts with exponential backoff

### Retry Delays (Exponential Backoff)
1. Attempt 1: Immediate
2. Attempt 2: Wait 2 seconds
3. Attempt 3: Wait 4 seconds
4. Attempt 4: Wait 8 seconds
5. Attempt 5: Wait 16 seconds
6. Final wait: 32 seconds (if needed)

This strategy is designed to work reliably with **Gemini's free tier** rate limits.

### Data Types Tested
1. **Type 1**: Overall paragraph (continuous conversation narrative)
2. **Type 2a**: JSON format (structured with speaker labels)
3. **Type 2b**: Labeled paragraph (line-by-line with Agent:/Customer: prefixes)

### Guidelines Tested (5 Parameters)
1. **Opening** - Greeting and agent introduction
2. **Closing** - Proper call termination with feedback request
3. **Hold** - Putting customer on hold appropriately
4. **Reassurance** - Providing customer assurance
5. **Further Assistance** - Asking if customer needs more help

---

## 🔧 Setup Instructions

### Step 1: Install Required Packages
```bash
pip install google-generativeai pandas python-dotenv
```

### Step 2: Create `.env` File
Create a file named `.env` in the project root:
```bash
touch .env
```

### Step 3: Add Your Gemini API Key
Edit the `.env` file and add:
```
GEMINI_API_KEY=your_actual_api_key_here
```

**Get your API key:**
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy and paste into `.env` file

### Step 4: Verify Setup
```bash
python run_gemini_full_test.py
```

---

## 🎯 What the Script Does

### Full Test Matrix
- **3 Data Types** × **5 Guidelines** = **15 Test Batches**
- **20 Conversations** per batch (default)
- **Total**: ~300 conversations tested

### Test Flow
```
For each data type (type1, type2a, type2b):
    For each guideline (opening, closing, hold, reassurance, further_assistance):
        Load 20 conversations
        For each conversation:
            1. Add data type context to prompt
            2. Send request to Gemini API
            3. If fails, retry up to 5 times with exponential backoff
            4. Parse JSON response
            5. Save results
        Save results to CSV with timestamp
```

### Results Output
Each test creates a CSV file with:
- Conversation details
- Test results (Met/Not Met)
- Evidence/reasoning from Gemini
- Performance metrics (latency, retries)
- Configuration used (temperature, tokens)

---

## 🎨 Key Features

### 1. Data Type Context in Prompts ✅
Each request includes explanation of the data format being analyzed:
- Type 1: "continuous narrative without speaker labels"
- Type 2a: "structured JSON with speaker identification"
- Type 2b: "line-by-line with speaker prefixes"

### 2. Robust Retry Logic ✅
- 5 retry attempts automatically
- Exponential backoff (2s → 4s → 8s → 16s → 32s)
- Handles rate limiting gracefully
- Perfect for free tier usage

### 3. Optimized for Free Tier ✅
- Temperature: 0.1 (deterministic)
- Max tokens: 512 (efficient)
- 1 second delay between conversations
- 2 second delay between test batches

### 4. Comprehensive Logging ✅
- Real-time progress updates
- Success/failure tracking
- Retry attempt counts
- Latency measurements
- Final summary statistics

---

## 📊 Expected Runtime

With 20 conversations per test:
- **Per Conversation**: ~3-5 seconds (including retries if needed)
- **Per Test Batch**: ~1-2 minutes
- **Full Test Suite**: ~30-45 minutes

*Note: Times may vary based on API response times and rate limiting*

---

## 📁 Results Location

After running, find your results in:
```
gemini_results/
├── type1/
│   ├── opening_results_20251016_143022.csv
│   ├── closing_results_20251016_144520.csv
│   ├── hold_results_20251016_145822.csv
│   ├── reassurance_results_20251016_151205.csv
│   └── further_assistance_results_20251016_152610.csv
├── type2a/
│   └── [same 5 files]
└── type2b/
    └── [same 5 files]
```

---

## 🔍 Analyzing Results

### Quick Analysis with pandas
```python
import pandas as pd
import glob

# Load all results
all_files = glob.glob('gemini_results/*/*.csv')
dfs = [pd.read_csv(f) for f in all_files]
combined = pd.concat(dfs, ignore_index=True)

# Summary statistics
print("=== OVERALL SUMMARY ===")
print(f"Total conversations: {len(combined)}")
print(f"Success rate: {(combined['success'].sum() / len(combined)) * 100:.1f}%")
print(f"\nResults breakdown:")
print(combined['result_value'].value_counts())
print(f"\nAverage latency: {combined['total_latency'].mean():.2f}s")
print(f"Average retries: {combined['attempts_used'].mean():.2f}")

# By data type
print("\n=== BY DATA TYPE ===")
print(combined.groupby('data_type')['result_value'].value_counts())

# By guideline
print("\n=== BY GUIDELINE ===")
print(combined.groupby('parameter_tested')['result_value'].value_counts())
```

---

## ⚠️ Troubleshooting

### Error: "GEMINI_API_KEY not found"
- Make sure `.env` file exists in project root
- Check that `GEMINI_API_KEY=...` is in the file
- Verify no extra spaces around the `=` sign

### Error: "google-generativeai not found"
```bash
pip install google-generativeai
```

### Rate Limit Errors
- The script automatically retries with backoff
- If still failing, increase delays in `retry_delays` list
- Consider reducing `max_conversations` in script

### Parse Errors
- Check `response_length` in CSV - if very small, API may be blocked
- Review `evidence` column for error messages
- Verify your API key is valid and active

---

## 🎉 Quick Commands

### Run Full Test Suite
```bash
python run_gemini_full_test.py
```

### View Results Summary
```bash
cd gemini_results
ls -R
```

### Check Test Progress (in another terminal)
```bash
watch -n 5 'ls -lR gemini_results/'
```

---

## 📞 Files Reference

| File | Purpose |
|------|---------|
| `run_gemini_full_test.py` | Main test script |
| `GEMINI_ENV_SETUP.txt` | Environment setup guide |
| `gemini_results/README.md` | Results documentation |
| `model_config.py` | Model configuration (updated) |
| `prompts.py` | Assessment prompts |
| `boom_boom_data_loader.py` | Data loading utilities |

---

## ✅ You're All Set!

Everything is configured and ready to run. Just:
1. ✅ Install packages: `pip install google-generativeai pandas python-dotenv`
2. ✅ Create `.env` with your `GEMINI_API_KEY`
3. ✅ Run: `python run_gemini_full_test.py`
4. ✅ Wait ~30-45 minutes for full completion
5. ✅ Analyze results in `gemini_results/` folder

**Good luck with your testing! 🚀**

