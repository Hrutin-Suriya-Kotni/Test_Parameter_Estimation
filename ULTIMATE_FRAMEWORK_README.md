# 🎯 Ultimate Testing Framework

**Multi-Model Call Center Analysis Testing System**

Test multiple LLM models across different data formats and evaluation categories with ease!

---

## 📋 Overview

This framework enables systematic testing of Large Language Models on call center transcript analysis. It supports:

- ✅ **Multiple Models**: vLLM servers, Gemini API, easy to extend
- ✅ **3 Data Formats**: Type1 (paragraph), Type2a (JSON), Type2b (labeled)
- ✅ **5 Test Categories**: Opening, Closing, Hold, Reassurance, Further Assistance
- ✅ **Robust Execution**: Retry logic, error handling, JSON extraction fallbacks
- ✅ **Comprehensive Logging**: Track every request, response, and error
- ✅ **Flexible Configuration**: YAML-based, easy to modify

---

## 🚀 Quick Start

### 1. **Setup**

```bash
# Install dependencies
pip install -r requirements.txt

# Configure your servers
vim config.yaml  # Edit model endpoints and enable/disable models
```

### 2. **Configure Models**

Edit `config.yaml`:

```yaml
models:
  multi_gpu_v100:
    name: "OpenChat Mistral 3.5 (2x V100)"
    endpoint: "http://192.168.30.252:8000/v1/chat/completions"
    enabled: true  # Set to true to test this model
```

### 3. **Run Tests**

```bash
# Test all enabled models on all data types
python run_ultimate_test.py

# Test specific model only
python run_ultimate_test.py --model multi_gpu_v100

# Test specific data type
python run_ultimate_test.py --data-types type1

# Test specific categories
python run_ultimate_test.py --categories opening closing
```

---

## 📁 Framework Structure

```
ultimate_framework/
├── __init__.py           # Package initialization
├── data_handler.py       # Loads all 3 data types
├── model_client.py       # Connects to vLLM/Gemini APIs
├── json_extractor.py     # Robust JSON extraction
└── test_runner.py        # Main test orchestration

config.yaml               # Configuration file
run_ultimate_test.py      # Main entry point
prompts.py                # Assessment prompts (fixed!)
data/                     # Your data files
  ├── type1_overall_paragraph.csv
  ├── type2a_json/
  └── type2b_labeled_paragraph.csv
ultimate_results/         # Results saved here
logs/                     # Log files
```

---

## 🔧 Configuration Guide

### Model Configuration

Each model needs:
- `name`: Display name
- `type`: "vllm" or "gemini"
- `endpoint`: API endpoint (for vLLM)
- `model_name`: Model identifier
- `enabled`: true/false
- `temperature`, `max_tokens`, `timeout`: Generation parameters

### Data Configuration

The framework automatically handles 3 data formats:
- **Type1**: Overall paragraph (CSV with conversation_id, transcript)
- **Type2a**: JSON structured (directory with .json files)
- **Type2b**: Labeled paragraph (CSV with conversation_id, labeled_transcript)

### Test Configuration

- `retry_on_failure`: Auto-retry failed requests
- `max_retries`: Maximum retry attempts
- `rate_limit_delay`: Seconds between requests

---

## 📊 Output & Results

### CSV Results

Results are saved as CSV files with columns:
- `conversation_id`: Unique conversation identifier
- `data_type`: type1, type2a, or type2b
- `category`: opening, closing, hold, reassurance, further_assistance
- `model`: Model name
- `success`: True/False
- `value`: "Met" or "Not Met"
- `evidence`: Extracted evidence text
- `latency`: Response time in seconds
- `timestamp`: When the test was run
- `error`: Error message (if failed)
- `raw_response`: Full LLM response (if enabled)

### File Naming

Format: `{model_id}_{data_type}_{timestamp}.csv`

Example: `multi_gpu_v100_type1_20251019_143052.csv`

### Logging

- Console output: Real-time progress
- Log file: `ultimate_test.log` with full details

---

## 🎯 Usage Examples

### Example 1: Test One Model on One Data Type

```bash
python run_ultimate_test.py \
  --model multi_gpu_v100 \
  --data-types type1 \
  --categories opening
```

**What it does:**
- Tests the multi-GPU V100 server
- Only on Type1 data (85 conversations)
- Only the "opening" category
- Total: 85 tests

### Example 2: Full Test on All Enabled Models

```bash
python run_ultimate_test.py
```

**What it does:**
- Tests ALL enabled models in `config.yaml`
- On ALL data types (type1, type2a, type2b)
- ALL categories (5 categories)
- Total: (# models) × 85 × 3 × 5 = **1,275 tests per model**

### Example 3: Quick Smoke Test

```bash
python run_ultimate_test.py \
  --data-types type1 \
  --categories opening closing \
  --verbose
```

**What it does:**
- Tests all enabled models
- Only on Type1 data
- Only opening + closing categories
- Total: 85 × 2 = 170 tests per model
- Verbose logging for debugging

---

## 🔍 Understanding The Data Types

### Type1: Overall Paragraph
```
conversation_id,transcript
abc-123,"agent: Hello customer: Hi agent: How can I help..."
```
**Use Case:** Simplest format, good for basic testing

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
**Use Case:** Most detailed, preserves turn structure and timing

### Type2b: Labeled Paragraph
```
conversation_id,labeled_transcript
abc-123,"agent: Hello customer: Hi agent: How can I help..."
```
**Use Case:** Balance between structure (speaker labels) and simplicity

---

## 📈 Metrics & Analysis

### Success Rate

```python
success_rate = (successful_tests / total_tests) * 100
```

**Target:** ≥95% success rate before production use

### Latency Analysis

- **Avg Latency:** Mean response time
- **P95 Latency:** 95th percentile (outliers)
- **Max Latency:** Longest response

### Value Distribution

Count of "Met" vs "Not Met" classifications per category

---

## 🛠️ Advanced Usage

### Adding a New Model

1. Edit `config.yaml`:
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

2. Run tests:
```bash
python run_ultimate_test.py --model my_new_model
```

### Testing from Python

```python
from ultimate_framework.test_runner import TestRunner

runner = TestRunner()
runner.run_full_test(
    model_id='multi_gpu_v100',
    data_types=['type1'],
    categories=['opening', 'closing']
)
```

### Custom Data Loading

```python
from ultimate_framework.data_handler import DataHandler

handler = DataHandler('./data')
conversations = handler.load_type1()

# Get stats
stats = handler.get_dataset_stats()
print(stats)
```

---

## 🐛 Troubleshooting

### Issue: "Connection timeout"

**Solution:** 
- Check server is running: `curl http://SERVER_IP:PORT/health`
- Increase timeout in `config.yaml`
- Check firewall settings

### Issue: "JSON extraction failed"

**Possible causes:**
- Model not following output format
- Response truncated (increase `max_tokens`)
- Model hallucinating

**Solution:**
- Check `raw_response` in results CSV
- Review prompt formatting in `prompts.py`
- Try increasing temperature for more varied responses

### Issue: "95% success rate not met"

**Action items:**
1. Check error messages in results CSV
2. Review failed cases in logs
3. Verify model configuration
4. Consider prompt adjustments

---

## 📝 Requirements

```
pandas>=2.0.0
pyyaml>=6.0
requests>=2.28.0
google-generativeai>=0.3.0  # For Gemini only
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 🎓 Best Practices

### 1. **Test Incrementally**
Start with one model + one data type + one category before running full tests.

### 2. **Monitor Logs**
Watch for patterns in errors - they reveal prompt or model issues.

### 3. **Rate Limiting**
Adjust `rate_limit_delay` based on your server capacity.

### 4. **Save Raw Responses**
Keep `include_raw_responses: true` for debugging.

### 5. **Version Control**
Commit `config.yaml` changes and results for tracking.

---

## 🔄 Testing Workflow

```
1. Configure Model
   ↓
2. Run Smoke Test (small subset)
   ↓
3. Check Success Rate
   ├─ <95%? → Debug & Fix
   └─ ≥95%? → Continue
   ↓
4. Run Full Test
   ↓
5. Analyze Results
   ↓
6. Compare Models
   ↓
7. Generate Report
```

---

## 📊 Results Analysis

After running tests, analyze with pandas:

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

# Category performance
print(df.groupby('category')['success'].mean())
```

---

## 🎯 Next Steps

1. **Test Your First Server**
   ```bash
   python run_ultimate_test.py --model multi_gpu_v100 --data-types type1 --categories opening
   ```

2. **Review Results**
   ```bash
   ls -lh ultimate_results/
   ```

3. **Add More Servers**
   Edit `config.yaml` and repeat

4. **Compare Models**
   Use results CSVs for analysis

---

## 💡 Tips

- Start with **Type1 data** - it's the simplest
- Test **one category** first (opening is easiest)
- Use `--verbose` flag when debugging
- Check `ultimate_test.log` for detailed info
- Results are timestamped - you can rerun safely

---

## 📞 Support

Check these files for more info:
- `FEASIBILITY_ANALYSIS.md` - Project feasibility study
- `PROMPT_FIXES_APPLIED.md` - Prompt corrections made
- `prompts.py` - All assessment prompts

---

**Built with ❤️ for comprehensive LLM testing**

Branch: `Ultimate-Magic` 🎩✨

