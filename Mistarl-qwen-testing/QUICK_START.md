# ⚡ Quick Start - Mistral V100 Testing

## On V100 Server (via AnyDesk):

```bash
# 1. Clone
git clone https://github.com/Hrutin-Suriya-Kotni/Test_Parameter_Estimation.git
cd Test_Parameter_Estimation
git checkout Ultimate-Magic

# 2. Setup
python3 -m venv .venv
source .venv/bin/activate

# 3. Install (auto-installs sentencepiece if missing)
pip install -r Mistarl-qwen-testing/requirements.txt

# 4. Run
python3 Mistarl-qwen-testing/test_mistral_v100.py
```

---

## If sentencepiece error occurs:

```bash
pip install sentencepiece protobuf
python3 Mistarl-qwen-testing/test_mistral_v100.py
```

---

**Server:** 192.168.30.252:8000  
**Expected Time:** 15-20 minutes  
**Output:** `Mistarl-qwen-testing/results/mistral_v100_test_results_*.json`

