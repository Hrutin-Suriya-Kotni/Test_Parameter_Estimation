# 🎯 BOOM BOOM Test Instructions

## ✅ Everything is Ready!

### Your Setup:
- ✅ **Server3** (vLLM Direct): `http://27.111.72.53:3333` - Working!
- ✅ **Server5**: `http://27.111.72.51:8000` - Working!
- ⚠️  **Karvalo**: TBD (add later)
- ✅ **Gemini API**: Ready (needs API key)

### Your Data:
- ✅ **type1**: 86 conversations
- ✅ **type2a**: 85 conversations  
- ✅ **type2b**: 86 conversations

### Your Parameters:
1. Opening
2. Closing
3. Reassurance
4. Hold
5. Further Assistance

---

## 🚀 Run Comprehensive Test

### Option 1: Automated (Recommended)

Run Server3 + Server5 on ALL data types and ALL parameters with 20 conversations:

```bash
python3 run_server3_server5_full_test.py
# Type: yes
# Wait 30-45 minutes
# Results saved automatically
```

### Option 2: Interactive (Manual Control)

```bash
python3 boom_boom_test.py

# For Server3 on Type1, all parameters:
# Choice: 1 (single model, single data type)
# Parameter: 6 (ALL PARAMETERS)
# Max conversations: 20
# Model: 1 (Server3)
# Data type: 1 (type1)
```

---

## 📊 Results Location

```
MISTRAL_BOOM_BOOM/
├── type1/
│   ├── server3_base_openchat_mistral/
│   │   └── 20251010_183045/
│   │       ├── opening_results.csv
│   │       ├── closing_results.csv
│   │       ├── reassurance_results.csv
│   │       ├── hold_results.csv
│   │       └── further_assistance_results.csv
│   └── server5_base_mistral/
│       └── 20251010_183122/
│           └── [same 5 files]
├── type2a/
│   └── [same structure]
└── type2b/
    └── [same structure]
```

---

## 🔍 Monitor Progress

```bash
# Count completed tests
ls -R MISTRAL_BOOM_BOOM/ | grep "\.csv" | wc -l

# Expected: 30 CSV files (2 models × 3 data types × 5 parameters)

# View latest results
ls -lt MISTRAL_BOOM_BOOM/*/server3*/*/

# Check what's running
ps aux | grep python3 | grep boom
```

---

## 📈 Analyze Results

```python
import pandas as pd
import glob

# Load all Server3 results
server3_files = glob.glob('MISTRAL_BOOM_BOOM/*/server3*/*/*.csv')
df_list = [pd.read_csv(f) for f in server3_files]
all_server3 = pd.concat(df_list, ignore_index=True)

# Summary by parameter
print(all_server3.groupby('parameter_tested')['result_value'].value_counts())

# Average latency by parameter
print(all_server3.groupby('parameter_tested')['total_latency'].mean())

# Token usage by parameter
print(all_server3.groupby('parameter_tested')['total_tokens'].sum())
```

---

## ✅ What You'll Get

30 CSV files with complete metadata:
- Parameter being tested
- API settings (temperature, max_tokens, endpoint)
- Results (Met/Not Met)
- Evidence
- Latency per conversation
- Token usage
- Timestamps

All organized by data type and model!

---

**Status**: Test running automatically! Check results in MISTRAL_BOOM_BOOM/ folder.

