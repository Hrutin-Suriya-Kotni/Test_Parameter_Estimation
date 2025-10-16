# 🎉 MISTRAL_BOOM_BOOM - API Comparison Project

Complete comparison of 4 Mistral API variants across 3 data types with full metadata tracking.

---

## 🎯 Project Overview

**Goal**: Compare performance, accuracy, and characteristics of 4 different API implementations:

1. **Server3 OpenChat Mistral** (`server3_base_openchat_mistral`)
   - Endpoint: `http://27.111.72.53:8000/chat`
   - Format: OpenAI-compatible
   - ✅ **Available**

2. **Server5 Base Mistral** (`server5_base_mistral`)
   - Endpoint: `http://27.111.72.51:8000/generate`
   - Format: Simple prompt-response
   - ✅ **Available**

3. **Karvalo OpenChat Mistral** (`karvalo_base_openchat_mistal`)
   - Endpoint: TBD
   - Format: TBD
   - ⚠️  **Coming Soon**

4. **Gemini API** (`gemini_api`)
   - Google Gemini 2.0 Flash
   - ✅ **Available** (requires API key)

---

## 📊 Data Types

### Type1: `type1_overall_paragraph.csv`
- Overall conversation paragraphs
- CSV format
- ~86 conversations

### Type2a: `type2a_json/`
- JSON format with turn-by-turn conversation
- Agent/Customer dialogue structure
- ~85 JSON files

### Type2b: `type2b_labeled_paragraph.csv`
- Labeled paragraph format
- CSV format
- ~86 conversations

---

## 📁 Folder Structure

```
MISTRAL_BOOM_BOOM/
├── README.md                          # This file
├── type1/                             # Type1 results
│   ├── server3_base_openchat_mistral/ # Results for Server3
│   ├── server5_base_mistral/          # Results for Server5
│   ├── karvalo_base_openchat_mistal/  # Results for Karvalo
│   └── gemini_api/                    # Results for Gemini
├── type2a/                            # Type2a results
│   ├── server3_base_openchat_mistral/
│   ├── server5_base_mistral/
│   ├── karvalo_base_openchat_mistal/
│   └── gemini_api/
└── type2b/                            # Type2b results
    ├── server3_base_openchat_mistral/
    ├── server5_base_mistral/
    ├── karvalo_base_openchat_mistal/
    └── gemini_api/
```

Each result folder contains CSV files with timestamp:
- `opening_results_20250110_120000.csv`
- `closing_results_20250110_120500.csv`
- etc.

---

## 🚀 Quick Start

### 1. Test Single API on Single Data Type

```bash
cd /path/to/Parameter_Testing
python3 boom_boom_test.py

# Select: 1 (Single model on single data type)
# Choose: Model (1-4)
# Choose: Data Type (1-3)
# Enter: Test type (opening, closing, etc.)
# Enter: Max conversations (or press Enter for all)
```

### 2. Run Full Comparison

```bash
python3 boom_boom_test.py

# Select: 4 (Test all models on all data types)
# Enter: Test type (opening, closing, etc.)
# Enter: Max conversations (or press Enter for all)
# Confirm: yes
```

### 3. Programmatic Usage

```python
from boom_boom_test import BoomBoomTestRunner

runner = BoomBoomTestRunner()

# Test Server3 on Type1 data
runner.test_model_on_data_type(
    model_name='server3_base_openchat_mistral',
    data_type='type1',
    test_type='opening',
    max_conversations=10
)

# Full run
runner.test_all_models_all_data_types(
    test_type='opening',
    max_conversations=20
)
```

---

## 📈 Metadata Tracked

Each result file contains comprehensive metadata:

### Common Fields
- `conversation_id`: Unique conversation identifier
- `data_type`: type1, type2a, or type2b
- `test_type`: opening, closing, reassurance, etc.
- `model_name`: API being tested
- `timestamp`: When test was run
- `success`: Whether API call succeeded
- `result_value`: Met/Not Met/Error
- `evidence`: Detailed evidence from analysis
- `total_latency`: End-to-end latency in seconds
- `transcript_length`: Input transcript length
- `response_length`: Response length

### Server3 Specific (OpenAI-compatible)
- `prompt_tokens`: Exact prompt tokens used
- `completion_tokens`: Exact completion tokens generated
- `total_tokens`: Total tokens consumed
- `finish_reason`: stop/length/etc.
- `latency_seconds`: API latency

### Server5 Specific
- `prompt_tokens_estimate`: Estimated prompt tokens
- `completion_tokens_estimate`: Estimated completion tokens
- `total_tokens_estimate`: Estimated total
- `response_length_chars`: Response character count
- `note`: "Token counts are estimates"

### Gemini Specific
- Similar to Server3 (exact token counts provided by API)

---

## 📊 Analyzing Results

### Load Results

```python
import pandas as pd

# Load Server3 Type1 opening results
df = pd.read_csv('MISTRAL_BOOM_BOOM/type1/server3_base_openchat_mistral/opening_results_20250110_120000.csv')

# View summary statistics
print(df['total_latency'].describe())
print(df['total_tokens'].describe())
print(df['result_value'].value_counts())
```

### Compare Models

```python
import pandas as pd

# Load results from multiple models
server3_df = pd.read_csv('MISTRAL_BOOM_BOOM/type1/server3_base_openchat_mistral/opening_results_20250110_120000.csv')
server5_df = pd.read_csv('MISTRAL_BOOM_BOOM/type1/server5_base_mistral/opening_results_20250110_120000.csv')

# Compare average latency
print(f"Server3 avg latency: {server3_df['total_latency'].mean():.3f}s")
print(f"Server5 avg latency: {server5_df['total_latency'].mean():.3f}s")

# Compare accuracy
print(f"Server3 'Met' rate: {(server3_df['result_value']=='Met').sum()/len(server3_df)*100:.1f}%")
print(f"Server5 'Met' rate: {(server5_df['result_value']=='Met').sum()/len(server5_df)*100:.1f}%")

# Compare token usage
if 'total_tokens' in server3_df.columns:
    print(f"Server3 avg tokens: {server3_df['total_tokens'].mean():.0f}")
if 'total_tokens_estimate' in server5_df.columns:
    print(f"Server5 avg tokens (est): {server5_df['total_tokens_estimate'].mean():.0f}")
```

---

## 🔧 Configuration

### Update API Settings

Edit `model_config.py`:

```python
'server3_base_openchat_mistral': {
    'config': {
        'api_url': 'http://27.111.72.53:8000/chat',
        'model': 'openchat/openchat-3.5-1210',
        'max_tokens': 512,        # Adjust this
        'temperature': 0.1        # Adjust this
    }
}
```

### Add Karvalo API (When Available)

1. Get API endpoint details
2. Create `model_clients/karvalo_openchat_mistral_client.py`
3. Update `api_url` in `model_config.py`
4. Test: `python3 boom_boom_test.py`

---

## 📝 Test Types Available

From `prompts.py`:

1. **opening** - Agent greeting and introduction
2. **closing** - Call closing and feedback request
3. **reassurance** - Customer reassurance statements
4. **hold** - Hold procedures
5. **further_assistance** - Additional help offers

---

## 🎯 Typical Workflow

### Initial Testing (Small Sample)
```bash
# Test with 5 conversations to verify setup
python3 boom_boom_test.py
# Select: 1 (Single model on single data type)
# Choose: Server3 (1)
# Choose: Type1 (1)
# Test type: opening
# Max conversations: 5
```

### Full Data Type Test
```bash
# Test Server3 on all Type1 data
python3 boom_boom_test.py
# Select: 1
# Choose: Server3 (1)
# Choose: Type1 (1)
# Test type: opening
# Max conversations: [Press Enter for all]
```

### Complete Comparison
```bash
# Test all models on all data types
python3 boom_boom_test.py
# Select: 4 (Full run)
# Test type: opening
# Max conversations: [Press Enter for all]
# Confirm: yes
```

---

## 📊 Expected Results

Each test generates a CSV file with columns like:

| Column | Example | Description |
|--------|---------|-------------|
| conversation_id | conv_1 | Unique ID |
| data_type | type1 | Data source |
| model_name | Server3_OpenChat_Mistral | API tested |
| success | True | API call succeeded |
| result_value | Met | Analysis result |
| evidence | "Agent said..." | Supporting evidence |
| total_latency | 2.345 | Total time (seconds) |
| total_tokens | 156 | Tokens consumed |
| prompt_tokens | 120 | Input tokens |
| completion_tokens | 36 | Output tokens |

---

## 🐛 Troubleshooting

### API Connection Errors

```bash
# Test individual API
python3 -c "
from model_clients.server3_openchat_mistral_client import Server3OpenChatMistralClient
client = Server3OpenChatMistralClient()
print('Initialization:', client.initialize())
"
```

### Check Model Status

```bash
python3 model_config.py | grep -A 3 "Server3\|Server5\|Karvalo\|Gemini"
```

### View Sample Data

```bash
python3 boom_boom_data_loader.py
```

---

## 📈 Performance Benchmarks

### Expected Performance (Example)

| Model | Avg Latency | Avg Tokens | Accuracy |
|-------|-------------|------------|----------|
| Server3 | 2-5s | 150-250 | TBD |
| Server5 | 7-10s | 150 (est) | TBD |
| Karvalo | TBD | TBD | TBD |
| Gemini | 1-3s | 100-200 | TBD |

*Note: These are estimates. Actual results will vary.*

---

## 🎉 Status

### Completed ✅
- [x] Server3 API client
- [x] Server5 API client
- [x] Data loader (all 3 types)
- [x] Test runner with metadata
- [x] Folder structure
- [x] Documentation

### In Progress 🚧
- [ ] Karvalo API client (waiting for endpoint)
- [ ] Gemini API testing (requires API key)
- [ ] Full comparison analysis

### Planned 📋
- [ ] Automated comparison reports
- [ ] Visualization dashboards
- [ ] Cost analysis
- [ ] Performance optimization

---

## 📞 Quick Commands

```bash
# Test data loader
python3 boom_boom_data_loader.py

# Check model status
python3 model_config.py

# Run interactive test
python3 boom_boom_test.py

# Test Server3
python3 model_clients/server3_openchat_mistral_client.py

# Test Server5
python3 model_clients/server5_base_mistral_client.py

# View results
ls -R MISTRAL_BOOM_BOOM/
cat MISTRAL_BOOM_BOOM/type1/server3_base_openchat_mistral/*.csv
```

---

## 🎯 Next Steps

1. ✅ Test Server3 and Server5 on small sample (5-10 conversations)
2. ⬜ Add Karvalo API when endpoint is provided
3. ⬜ Add Gemini API key and test
4. ⬜ Run full comparison on all data types
5. ⬜ Analyze results and generate comparison report
6. ⬜ Create visualization dashboard

---

**Project**: MISTRAL_BOOM_BOOM 🎉  
**Status**: Ready for Testing  
**Created**: Current Session  
**Last Updated**: Current Session


