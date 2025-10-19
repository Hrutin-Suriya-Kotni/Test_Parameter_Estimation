# 🎯 Ultimate Testing Framework

**Multi-Model Call Center Analysis Testing System**

[![Branch](https://img.shields.io/badge/branch-Ultimate--Magic-purple)](https://github.com)
[![Status](https://img.shields.io/badge/status-Ready-green)]()
[![Python](https://img.shields.io/badge/python-3.8+-blue)]()

---

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Verify server is running
curl http://192.168.30.252:8000/health

# 2. Install dependencies
pip install -r requirements_ultimate.txt

# 3. Configure your server (edit config.yaml, set enabled: true)
vim config.yaml

# 4. Run your first test
python run_ultimate_test.py --model multi_gpu_v100 --data-types type1 --categories opening
```

**Expected output:** 85 tests in ~2-3 minutes with ≥95% success rate

---

## 📊 What Is This?

A comprehensive testing framework to evaluate Large Language Models on **call center transcript analysis**.

### Test Matrix
- ✅ **5 Models**: Mistral base/finetuned on different hardware + Gemini API
- ✅ **3 Data Formats**: Type1 (paragraph), Type2a (JSON), Type2b (labeled)
- ✅ **5 Categories**: Opening, Closing, Hold, Reassurance, Further Assistance
- ✅ **85 Conversations** per data type
- ✅ **Total**: 1,275 test cases per model

### Goal
Find the optimal combination of **model + hardware + data format** that delivers best **accuracy + latency + evidence quality**.

---

## 📁 Project Structure

```
Parameter_Testing/
├── ultimate_framework/          # Core framework
│   ├── data_handler.py          # Loads all 3 data formats
│   ├── model_client.py          # vLLM + Gemini API clients
│   ├── json_extractor.py        # Robust JSON parsing (4 strategies)
│   └── test_runner.py           # Test orchestration
│
├── data/                        # Test data (85 conversations)
│   ├── type1_overall_paragraph.csv
│   ├── type2a_json/             # 85 JSON files
│   └── type2b_labeled_paragraph.csv
│
├── config.yaml                  # Model configuration (EDIT THIS)
├── run_ultimate_test.py         # CLI entry point
├── prompts.py                   # Assessment prompts (fixed & validated)
├── requirements_ultimate.txt    # Dependencies
│
├── ultimate_results/            # Test results (auto-created)
├── logs/                        # Log files (auto-created)
│
├── README.md                    # This file
└── FEASIBILITY_ANALYSIS.md      # Project analysis & token calculations
```

---

## 🛠️ Configuration

### Configure Models in `config.yaml`

```yaml
models:
  multi_gpu_v100:
    name: "OpenChat Mistral 3.5 (2x V100)"
    endpoint: "http://192.168.30.252:8000/v1/chat/completions"
    model_name: "openchat/openchat-3.5-1210"
    enabled: true  # ← Set this to true to test
    temperature: 0.3
    max_tokens: 500
    timeout: 30
```

### Available Models

| Model ID | Hardware | Status | Description |
|----------|----------|--------|-------------|
| `multi_gpu_v100` | 2x Tesla V100 | ✅ Ready | OpenChat Mistral 3.5 |
| `server3_rtx4000` | RTX 4000 | ⏳ Pending | Mistral Base |
| `server3_rtx4000_finetuned` | RTX 4000 | ⏳ Pending | Mistral Finetuned |
| `multi_gpu_v100_finetuned` | 2x V100 | ⏳ Pending | Mistral Finetuned |
| `gemini_flash` | Cloud API | 🔑 Need Key | Gemini 1.5 Flash |

---

## 💻 Usage

### Basic Commands

```bash
# Test all enabled models on all data types
python run_ultimate_test.py

# Test specific model
python run_ultimate_test.py --model multi_gpu_v100

# Test specific data type(s)
python run_ultimate_test.py --data-types type1

# Test specific categories
python run_ultimate_test.py --categories opening closing

# Combine options
python run_ultimate_test.py --model multi_gpu_v100 --data-types type1 --categories opening

# Verbose output for debugging
python run_ultimate_test.py --verbose
```

### Testing Strategy

**1. Smoke Test** (2-3 minutes)
```bash
python run_ultimate_test.py --model multi_gpu_v100 --data-types type1 --categories opening
```
- 85 tests
- Verifies server works
- Checks success rate

**2. Single Data Type** (10-15 minutes)
```bash
python run_ultimate_test.py --model multi_gpu_v100 --data-types type1
```
- 85 conversations × 5 categories = 425 tests

**3. Full Test** (30-45 minutes)
```bash
python run_ultimate_test.py --model multi_gpu_v100
```
- 85 × 3 types × 5 categories = 1,275 tests

---

## 📊 Understanding Results

### CSV Output

Results are saved to `ultimate_results/` with format: `{model_id}_{data_type}_{timestamp}.csv`

**Columns:**
- `conversation_id` - Unique conversation identifier
- `data_type` - type1, type2a, or type2b
- `category` - opening, closing, hold, reassurance, further_assistance
- `model` - Model name
- `success` - True/False
- `value` - "Met" or "Not Met" (if successful)
- `evidence` - Extracted evidence text
- `latency` - Response time in seconds
- `timestamp` - When test was run
- `error` - Error message (if failed)
- `raw_response` - Full LLM response

### Console Output

```
============================================================
🚀 ULTIMATE TESTING FRAMEWORK
============================================================
Found 1 enabled model(s): ['multi_gpu_v100']
Loaded 85 Type1 conversations

Progress: 1/85 - Conv: c4a380c6... Category: opening
✅ Success - Value: Met, Latency: 2.34s

...

============================================================
📊 TEST SUMMARY
============================================================
Total Tests: 85
Successful: 81 (95.3%)  ✅ TARGET MET
Failed: 4
Avg Latency: 2.12s

Value Distribution:
  Met: 67
  Not Met: 14
============================================================
```

### Success Criteria

- ✅ **Success Rate:** ≥95%
- ✅ **Avg Latency:** <5 seconds
- ✅ **JSON Parse Rate:** ≥95%

---

## 🔍 Data Formats Explained

### Type1: Overall Paragraph
```csv
conversation_id,transcript
abc-123,"agent: Hello customer: Hi agent: How can I help..."
```
**Simplest format** - Full conversation as continuous text

### Type2a: JSON Structured
```json
{
  "conversation_id": "abc-123",
  "turns": [
    {"speaker": "agent", "text": "Hello", "starttime": 1.2},
    {"speaker": "customer", "text": "Hi", "starttime": 2.5}
  ]
}
```
**Most detailed** - Turn-by-turn with timestamps

### Type2b: Labeled Paragraph
```csv
conversation_id,labeled_transcript
abc-123,"agent: Hello customer: Hi agent: How can I help..."
```
**Balanced** - Speaker labels + paragraph format

---

## 🌟 Key Features

### Robust Testing
- ✅ Automatic retry logic (up to 3 attempts)
- ✅ Rate limiting (configurable delay)
- ✅ Comprehensive error handling
- ✅ Detailed logging to file + console

### Smart JSON Extraction
- ✅ **4-strategy fallback system**
  1. Direct JSON parse
  2. Markdown code block extraction
  3. Pattern matching
  4. Auto-fix common errors
- ✅ Handles single quotes, missing commas, etc.
- ✅ Validates required fields (Value, Evidence)
- ✅ Auto-normalizes "Yes"/"No" to "Met"/"Not Met"

### Flexible Architecture
- ✅ Easy to add new models
- ✅ Supports vLLM servers + Gemini API
- ✅ YAML configuration (no code changes)
- ✅ Modular design for extensions

---

## 🔧 Troubleshooting

### "Connection timeout"
```bash
# Test server connectivity
curl http://192.168.30.252:8000/health

# Check firewall
sudo ufw status

# Increase timeout in config.yaml
timeout: 60
```

### "JSON extraction failed"
- Check `raw_response` column in results CSV
- Review `ultimate_test.log` for details
- Increase `max_tokens` in config.yaml
- Verify prompts in `prompts.py`

### "Success rate <95%"
1. Check error messages in results CSV
2. Review detailed logs: `ultimate_test.log`
3. Verify server is stable
4. Test with `--verbose` flag
5. Consider prompt adjustments

### "ModuleNotFoundError"
```bash
# Make sure you're in the right directory
cd /path/to/Parameter_Testing

# Install dependencies
pip install -r requirements_ultimate.txt
```

---

## 🔧 Advanced Usage

### Adding a New Model

1. **Edit `config.yaml`:**
```yaml
my_new_model:
  name: "My Custom Model"
  type: "vllm"
  endpoint: "http://my-server:8000/v1/chat/completions"
  model_name: "my-model"
  enabled: true
  temperature: 0.3
  max_tokens: 500
```

2. **Test it:**
```bash
python run_ultimate_test.py --model my_new_model --data-types type1 --categories opening
```

### Python API

```python
from ultimate_framework.test_runner import TestRunner

# Initialize
runner = TestRunner()

# Run tests
runner.run_full_test(
    model_id='multi_gpu_v100',
    data_types=['type1'],
    categories=['opening', 'closing']
)
```

### Analyzing Results

```python
import pandas as pd

# Load results
df = pd.read_csv('ultimate_results/multi_gpu_v100_type1_20251019_143052.csv')

# Success rate
print(f"Success Rate: {(df['success'].sum() / len(df)) * 100:.1f}%")

# Average latency
print(f"Avg Latency: {df[df['success']]['latency'].mean():.2f}s")

# Value distribution
print(df[df['success']]['value'].value_counts())

# Per-category performance
print(df.groupby('category')['success'].mean())
```

---

## 📦 Requirements

```bash
pip install -r requirements_ultimate.txt
```

**Dependencies:**
- pandas >= 2.0.0
- pyyaml >= 6.0
- requests >= 2.28.0
- google-generativeai >= 0.3.0 (for Gemini only)

---

## 🐛 Known Issues & Fixes

### Issue 1: Prompt Inconsistencies ✅ FIXED
- **Problem:** Examples showed "Yes"/"No" instead of "Met"/"Not Met"
- **Fix:** All prompts validated and corrected
- **Details:** See `prompts.py` lines 116, 148, 176

### Issue 2: Copy-Paste Error ✅ FIXED
- **Problem:** Further assistance prompt said "putting on hold"
- **Fix:** Corrected to "asking for further assistance"
- **Details:** See `prompts.py` line 201

### Issue 3: JSON Quote Styles ✅ FIXED
- **Problem:** Mixed single/double quotes in examples
- **Fix:** All examples use proper JSON double quotes
- **Details:** JSON extractor handles both anyway

---

## 🎯 Project Context

### Background
This framework tests LLMs on call center quality assessment. We have:
- 85 real call center conversations (Hindi + English code-mixed)
- 5 quality parameters to evaluate
- Multiple model deployments to compare

### Research Questions
1. Which **data format** works best? (Type1 vs Type2a vs Type2b)
2. Does **hardware** matter? (Single GPU vs Multi-GPU)
3. How close to **Gemini** can Mistral get?
4. Does **finetuning** help?

### Success Metrics
- **Accuracy:** Classification correctness (Met/Not Met)
- **Latency:** Response time per request
- **Evidence Quality:** How good are extracted evidences?
- **Stability:** Success rate ≥95%

See `FEASIBILITY_ANALYSIS.md` for detailed project analysis.

---

## 🚦 Current Status

### ✅ Completed
- [x] Framework architecture
- [x] Data handlers (all 3 types)
- [x] Model clients (vLLM + Gemini)
- [x] Robust JSON extraction
- [x] Test runner with retry logic
- [x] Prompt fixes & validation
- [x] Comprehensive documentation
- [x] Git branch: Ultimate-Magic
- [x] Pushed to GitHub

### 🔄 Ready to Test
- [ ] Multi-GPU server (192.168.30.252:8000) - **READY!**

### ⏳ Pending
- [ ] Server3 RTX 4000 endpoint configuration
- [ ] Finetuned model deployments
- [ ] Gemini API key integration
- [ ] Results comparison tool
- [ ] Performance visualization

---

## 🎓 Testing Workflow

```
1. Configure Model (config.yaml)
   ↓
2. Run Smoke Test (1 category, type1)
   ↓
3. Check Success Rate
   ├─ <95%? → Debug (check logs)
   └─ ≥95%? → Continue
   ↓
4. Run Full Test (all categories, all types)
   ↓
5. Analyze Results (CSV + Python)
   ↓
6. Compare Models
   ↓
7. Generate Report
```

---

## 📝 Git Information

**Branch:** `Ultimate-Magic`  
**GitHub:** https://github.com/Hrutin-Suriya-Kotni/Test_Parameter_Estimation/tree/Ultimate-Magic

**Backup:** All old code preserved in `updated_version` branch

```bash
# View current branch
git branch --show-current

# Switch to backup
git checkout updated_version

# Back to Ultimate-Magic
git checkout Ultimate-Magic
```

---

## 💡 Tips & Best Practices

1. **Start Small** - Test one category first
2. **Monitor Logs** - Review `ultimate_test.log` regularly
3. **Use Config** - Edit `config.yaml` instead of code
4. **Save Everything** - Results auto-saved with timestamps
5. **Rate Limit** - Adjust delay if server gets overwhelmed
6. **Verbose Mode** - Use `--verbose` for debugging
7. **Test Locally** - Verify with `curl` before running tests

---

## 🤝 Contributing

To test a new model:
1. Add configuration to `config.yaml`
2. Set `enabled: true`
3. Run: `python run_ultimate_test.py --model YOUR_MODEL_ID`

To extend the framework:
- See `ultimate_framework/` for modular components
- Each module is self-contained and documented
- Add new model types in `model_client.py`
- Add new data formats in `data_handler.py`

---

## 📞 Getting Help

1. **Quick Issues:** Check this README
2. **Technical Details:** See `FEASIBILITY_ANALYSIS.md`
3. **Logs:** Review `ultimate_test.log`
4. **Prompt Issues:** Check `prompts.py`
5. **Code:** Explore `ultimate_framework/` modules

---

## 🎯 Next Steps

**Ready to start testing?**

```bash
# Test your first server (2-3 minutes)
python run_ultimate_test.py \
  --model multi_gpu_v100 \
  --data-types type1 \
  --categories opening

# Check results
ls -lh ultimate_results/
```

---

**Branch:** `Ultimate-Magic` 🎩✨  
**Status:** Production Ready 🚀  
**Last Updated:** October 2025

---

**Built with ❤️ for comprehensive LLM testing**
