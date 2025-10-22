# 🧪 Model Testing Guide

**Created:** October 22, 2025

---

## ✅ OpenChat Test - COMPLETED

**Server:** 27.111.72.51:3333 (RTX 4000)  
**Status:** ✅ **100% SUCCESS**  
**Results:** `results/openchat_test_results_20251022_185711.json`

### Summary:
- **Total Tests:** 1,110
- **Successful:** 1,110 (100%)
- **Failed:** 0
- **Token Limit Exceeded:** 0

### By Guideline:
- opening: 222/222 (100%)
- closing: 222/222 (100%)
- reassurance: 222/222 (100%)
- hold: 222/222 (100%)
- further_assistance: 222/222 (100%)

### By Data Type:
- Type1: 370/370 (100%)
- Type2a: 370/370 (100%)
- Type2b: 370/370 (100%)

---

## 🔄 Mistral V100 Test - READY TO RUN

**Server:** 192.168.30.252:8000 (2x Tesla V100) **LOCAL NETWORK**  
**Script:** `test_mistral_v100.py`

### ⚠️ Important Notes:

1. **Local Network Only** - Server IP `192.168.30.252` is not globally accessible
2. **Network Requirement** - You must be connected to the same network as the V100 server
3. **From Server** - Best to run from the V100 server itself or a machine on the same LAN

---

## 🚀 How to Run Mistral Test

### Option 1: From V100 Server (Recommended)

```bash
# SSH into the V100 server
ssh user@192.168.30.252

# Navigate to project (or copy the script)
cd /path/to/Parameter_Testing

# Activate environment
source .test_report_env/bin/activate

# Install requirements if needed
pip3 install transformers requests

# Run the test
python3 Mistarl-qwen-testing/test_mistral_v100.py
```

### Option 2: From Local Machine (Same Network)

```bash
# Make sure you're on the same network as 192.168.30.252
# Test connectivity first:
curl http://192.168.30.252:8000/health

# If connection works, run the test:
cd /Users/cleveres_tidiot/Documents/Vocab_AI/Parameter_Testing
source .test_report_env/bin/activate
python3 Mistarl-qwen-testing/test_mistral_v100.py
```

### Option 3: Copy Files to Server

```bash
# From your Mac, copy necessary files to V100 server
scp -r Mistarl-qwen-testing/ user@192.168.30.252:/path/
scp -r pre-processed-data/ user@192.168.30.252:/path/
scp prompts.py user@192.168.30.252:/path/

# SSH and run
ssh user@192.168.30.252
cd /path/
python3 Mistarl-qwen-testing/test_mistral_v100.py
```

---

## 📊 Test Configuration

Both tests use:
- **Token Limit:** 8,100 (safe for 8K context)
- **Pre-validation:** Checks tokens before API call
- **Retry Logic:** 3 attempts with 2s delay
- **Rate Limiting:** 0.5s between requests
- **Data:** 74 filtered conversations (pre-processed)
- **Coverage:** 5 guidelines × 3 data types = 1,110 tests

---

## 📂 Output Files

Results are saved to: `Mistarl-qwen-testing/results/`

- `openchat_test_results_YYYYMMDD_HHMMSS.json`
- `mistral_v100_test_results_YYYYMMDD_HHMMSS.json`

Each file contains:
- Overall statistics
- Per-guideline breakdown
- Per-data-type breakdown  
- Detailed results for every test
- Token counts and latencies

---

## 🔍 Quick Connectivity Test

**For Mistral V100:**

```bash
# Test if server is reachable
curl http://192.168.30.252:8000/health

# Test with a simple request
curl -X POST http://192.168.30.252:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistralai/Mistral-7B-Instruct-v0.3",
    "messages": [{"role": "user", "content": "Say hello"}],
    "max_tokens": 20
  }'
```

---

## ⏱️ Expected Duration

- **OpenChat:** ~15-20 minutes ✅ COMPLETED
- **Mistral V100:** ~15-20 minutes (pending)

---

## 📈 Next Steps

After Mistral test completes:
1. ✅ Compare results between OpenChat and Mistral
2. ✅ Analyze success rates by guideline and data type
3. ✅ Generate comparative report
4. ✅ Document findings and recommendations

