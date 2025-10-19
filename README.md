# 🎯 Ultimate Testing Framework

**Multi-Model Call Center Analysis Testing System**

[![Branch](https://img.shields.io/badge/branch-Ultimate--Magic-purple)](https://github.com)
[![Status](https://img.shields.io/badge/status-Ready-green)]()
[![Python](https://img.shields.io/badge/python-3.8+-blue)]()

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements_ultimate.txt

# 2. Configure your server
vim config.yaml  # Enable your model

# 3. Run your first test
python run_ultimate_test.py --model multi_gpu_v100 --data-types type1 --categories opening
```

**See full guide:** [QUICK_START_ULTIMATE.md](QUICK_START_ULTIMATE.md)

---

## 📊 What Is This?

A comprehensive testing framework to evaluate Large Language Models on **call center transcript analysis** across:

- ✅ **5 Models**: Mistral base/finetuned on different hardware + Gemini API
- ✅ **3 Data Formats**: Type1 (paragraph), Type2a (JSON), Type2b (labeled)
- ✅ **5 Categories**: Opening, Closing, Hold, Reassurance, Further Assistance
- ✅ **Total**: 1,275 test cases per model

---

## 🎯 Project Goals

**Find the optimal combination of:**
1. **Model** (base vs finetuned)
2. **Hardware** (single GPU vs multi-GPU)
3. **Data format** (Type1 vs Type2a vs Type2b)

That delivers the best **accuracy**, **latency**, and **evidence quality** - as close to Gemini as possible!

---

## 📁 Project Structure

```
Parameter_Testing/
├── ultimate_framework/          # 🆕 Core framework
│   ├── data_handler.py          # Multi-format data loading
│   ├── model_client.py          # vLLM + Gemini API clients
│   ├── json_extractor.py        # Robust JSON parsing
│   └── test_runner.py           # Test orchestration
│
├── data/                        # Test data (85 conversations)
│   ├── type1_overall_paragraph.csv
│   ├── type2a_json/             # 85 JSON files
│   └── type2b_labeled_paragraph.csv
│
├── config.yaml                  # 🆕 Model configuration
├── run_ultimate_test.py         # 🆕 CLI entry point
├── prompts.py                   # ✅ Fixed assessment prompts
│
├── ultimate_results/            # Test results (auto-created)
├── logs/                        # Log files (auto-created)
│
├── ULTIMATE_FRAMEWORK_README.md # 📖 Comprehensive guide
├── QUICK_START_ULTIMATE.md      # ⚡ Quick start
├── FEASIBILITY_ANALYSIS.md      # 📊 Project analysis
└── PROMPT_FIXES_APPLIED.md      # 🔧 Prompt corrections
```

---

## 🛠️ Models Under Test

| # | Model | Hardware | Status | Config ID |
|---|-------|----------|--------|-----------|
| 1 | Mistral Base | RTX 4000 | ⏳ Pending | `server3_rtx4000` |
| 2 | OpenChat Mistral 3.5 | 2x Tesla V100 | ✅ **Ready** | `multi_gpu_v100` |
| 3 | Mistral Finetuned | RTX 4000 | ⏳ Pending | `server3_rtx4000_finetuned` |
| 4 | Mistral Finetuned | 2x V100 | ⏳ Pending | `multi_gpu_v100_finetuned` |
| 5 | Gemini 1.5 Flash | Cloud API | 🔑 Need Key | `gemini_flash` |

---

## 📖 Documentation

- **[QUICK_START_ULTIMATE.md](QUICK_START_ULTIMATE.md)** - Get started in 5 minutes
- **[ULTIMATE_FRAMEWORK_README.md](ULTIMATE_FRAMEWORK_README.md)** - Complete documentation
- **[FEASIBILITY_ANALYSIS.md](FEASIBILITY_ANALYSIS.md)** - Project feasibility study
- **[PROMPT_FIXES_APPLIED.md](PROMPT_FIXES_APPLIED.md)** - Prompt corrections made

---

## 💻 Usage Examples

### Test One Server

```bash
python run_ultimate_test.py \
  --model multi_gpu_v100 \
  --data-types type1 \
  --categories opening
```

### Full Test Suite

```bash
# All enabled models × all data types × all categories
python run_ultimate_test.py
```

### Specific Combination

```bash
python run_ultimate_test.py \
  --model multi_gpu_v100 \
  --data-types type1 type2a \
  --categories opening closing hold
```

---

## 📊 Expected Results

After running tests, you'll get CSV files with:

- ✅ **Success rate** (target: ≥95%)
- ⚡ **Latency metrics** (avg, P95, max)
- 📝 **Classification** (Met/Not Met)
- 🔍 **Evidence extraction**
- ⚠️ **Error tracking**

Example output:
```
Total Tests: 85
Successful: 81 (95.3%) ✅
Failed: 4
Avg Latency: 2.12s
```

---

## 🔧 Configuration

Edit `config.yaml` to:
- Enable/disable models
- Configure endpoints
- Adjust test parameters
- Set rate limits

Example:
```yaml
models:
  multi_gpu_v100:
    enabled: true  # ← Change this
    endpoint: "http://192.168.30.252:8000/v1/chat/completions"
```

---

## 🌟 Key Features

### Robust Testing
- ✅ Automatic retry logic
- ✅ Error handling & recovery
- ✅ Rate limiting
- ✅ Comprehensive logging

### Flexible JSON Extraction
- ✅ 4-strategy fallback system
- ✅ Handles markdown code blocks
- ✅ Fixes common JSON errors
- ✅ Validates output format

### Multi-Model Support
- ✅ vLLM servers (any model)
- ✅ Gemini API
- ✅ Easy to extend

---

## 📈 Testing Workflow

```
1. Configure Model → 2. Run Smoke Test → 3. Verify ≥95% Success
                                              ↓
              6. Generate Report ← 5. Analyze Results ← 4. Run Full Test
```

---

## 🐛 Troubleshooting

### Connection Issues
```bash
# Test server connectivity
curl http://192.168.30.252:8000/health
```

### JSON Extraction Fails
- Check `raw_response` in results CSV
- Review prompts in `prompts.py`
- Increase `max_tokens` in config

### Low Success Rate (<95%)
1. Check error messages in CSV
2. Review logs: `ultimate_test.log`
3. Verify server stability
4. Consider prompt adjustments

---

## 📦 Requirements

```bash
pip install -r requirements_ultimate.txt
```

**Dependencies:**
- pandas >= 2.0.0
- pyyaml >= 6.0
- requests >= 2.28.0
- google-generativeai >= 0.3.0 (for Gemini)

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

### 🔄 In Progress
- [ ] Testing multi-GPU server (ready to test!)
- [ ] Finetuned model deployment
- [ ] Gemini API integration

### 📋 Planned
- [ ] Results comparison tool
- [ ] Performance visualization
- [ ] Automated reporting

---

## 🤝 Contributing

This is a research project. To test a new model:

1. Add configuration to `config.yaml`
2. Set `enabled: true`
3. Run: `python run_ultimate_test.py --model YOUR_MODEL_ID`

---

## 📝 Change Log

### v1.0.0 - Ultimate-Magic Branch (Oct 2025)
- ✨ Complete framework rewrite
- ✨ Modular architecture
- ✨ YAML-based configuration
- ✨ Robust JSON extraction
- ✨ CLI interface
- ✅ Prompt fixes applied
- 📚 Comprehensive documentation

---

## 📞 Support

Need help?
1. Check [QUICK_START_ULTIMATE.md](QUICK_START_ULTIMATE.md)
2. Read [ULTIMATE_FRAMEWORK_README.md](ULTIMATE_FRAMEWORK_README.md)
3. Review [FEASIBILITY_ANALYSIS.md](FEASIBILITY_ANALYSIS.md)
4. Check `ultimate_test.log` for details

---

## 🎯 Next Steps

**Ready to start?**

```bash
# Quick test (2-3 minutes)
python run_ultimate_test.py --model multi_gpu_v100 --data-types type1 --categories opening

# Full test (30-45 minutes)
python run_ultimate_test.py --model multi_gpu_v100
```

---

**Branch:** `Ultimate-Magic` 🎩✨  
**Status:** Ready for Testing 🚀  
**Last Updated:** October 2025
