# 🚀 Mistral V100 Testing - Quick Setup Guide

**Server:** 192.168.30.252:8000 (2x Tesla V100)  
**Model:** mistralai/Mistral-7B-Instruct-v0.3

---

## 📥 Step 1: Clone Repository (on V100 server)

```bash
# Via AnyDesk, open terminal on V100 server

cd /path/to/your/workspace

git clone https://github.com/Hrutin-Suriya-Kotni/Test_Parameter_Estimation.git
cd Test_Parameter_Estimation

# Checkout the Ultimate-Magic branch
git checkout Ultimate-Magic
```

---

## ⚙️ Step 2: Setup Environment

```bash
# Create virtual environment
python3 -m venv .test_env
source .test_env/bin/activate

# Install dependencies
pip3 install transformers requests

# Verify installation
python3 -c "import transformers; print('✅ Ready')"
```

---

## 🧪 Step 3: Run Mistral Test

```bash
# Make sure Mistral vLLM server is running on port 8000
# Then run the test:

python3 Mistarl-qwen-testing/test_mistral_v100.py
```

**Expected output:**
```
Testing server connectivity...
✅ Server is reachable!
Loading tokenizer...
================================================================================
Mistral V100 Multi-GPU Comprehensive Test
Server: 192.168.30.252:8000 (2x Tesla V100)
Token Limit: 8100
================================================================================
...
```

---

## 📊 Test Details

- **Total Tests:** 1,110 (74 conversations × 3 types × 5 guidelines)
- **Duration:** ~15-20 minutes
- **Token Limit:** 8,100 (validates before sending)
- **Output:** `Mistarl-qwen-testing/results/mistral_v100_test_results_*.json`

---

## ✅ What You'll Get

### Success Metrics:
- Overall success rate
- Per-guideline breakdown (opening, closing, etc.)
- Per-data-type breakdown (Type1, Type2a, Type2b)
- Token limit violations count

### Detailed Results:
- Response value (Met/Not Met/Parse Error)
- Latency per request
- Token count per request
- Full response text

---

## 🔍 Quick Health Check

Before running the full test:

```bash
# Test if server is responding
curl http://192.168.30.252:8000/health

# Test a simple request
curl -X POST http://192.168.30.252:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistralai/Mistral-7B-Instruct-v0.3",
    "messages": [{"role": "user", "content": "Say hello"}],
    "max_tokens": 20
  }'
```

---

## 📦 Files Included in Repo

```
Mistarl-qwen-testing/
├── test_mistral_v100.py          ← Run this script
├── test_openchat.py              (already completed)
├── token_analysis.py             (for reference)
├── TOKEN_ANALYSIS_REPORT.md      (analysis results)
├── OUTLIERS_ANALYSIS.md          (outlier details)
├── TESTING_GUIDE.md              (this guide)
└── results/                      (test outputs)

pre-processed-data/
├── type1_overall_paragraph.csv   (74 conversations)
├── type2a_json/                  (74 JSON files)
├── type2b_labeled_paragraph.csv  (74 conversations)
└── FILTERING_SUMMARY.md          (why 74 not 85)

prompts.py                         (required for tests)
```

---

## ⚡ One-Command Run

```bash
git clone https://github.com/Hrutin-Suriya-Kotni/Test_Parameter_Estimation.git && \
cd Test_Parameter_Estimation && \
git checkout Ultimate-Magic && \
python3 -m venv .test_env && \
source .test_env/bin/activate && \
pip3 install transformers requests && \
python3 Mistarl-qwen-testing/test_mistral_v100.py
```

---

**Pushed:** October 22, 2025  
**Branch:** Ultimate-Magic  
**Commit:** 8a0c353

