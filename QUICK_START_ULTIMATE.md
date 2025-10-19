# ⚡ Ultimate Framework - Quick Start Guide

**Get testing in 5 minutes!**

---

## Step 1: Verify Your Server is Running ✅

```bash
# Test the multi-GPU server you deployed
curl http://192.168.30.252:8000/health
```

**Expected:** Should return immediately

---

## Step 2: Install Dependencies 📦

```bash
pip install pandas pyyaml requests
```

Or:
```bash
pip install -r requirements_ultimate.txt
```

---

## Step 3: Configure Your Server 🔧

Edit `config.yaml` - Find this section:

```yaml
models:
  multi_gpu_v100:
    name: "OpenChat Mistral 3.5 (2x V100)"
    endpoint: "http://192.168.30.252:8000/v1/chat/completions"
    model_name: "openchat/openchat-3.5-1210"
    enabled: true  # ← Make sure this is true!
```

---

## Step 4: Run Your First Test 🚀

```bash
python run_ultimate_test.py \
  --model multi_gpu_v100 \
  --data-types type1 \
  --categories opening
```

**What this does:**
- Tests your multi-GPU server
- On Type1 data (85 conversations)
- Just the "opening" category
- **Total: 85 tests (~2-3 minutes)**

---

## Step 5: Check Results 📊

```bash
# List results
ls -lh ultimate_results/

# View the CSV
cat ultimate_results/multi_gpu_v100_type1_*.csv | head -20
```

Or open in Excel/pandas!

---

## Expected Output

You should see:
```
============================================================
🚀 ULTIMATE TESTING FRAMEWORK
============================================================
Found 1 enabled model(s): ['multi_gpu_v100']
Loading Type1 data from: ./data/type1_overall_paragraph.csv
Loaded 85 Type1 conversations

Progress: 1/85 - Conv: c4a380c6... Category: opening
✅ Success - Value: Met, Latency: 2.34s

Progress: 2/85 - Conv: c5255fb4... Category: opening
✅ Success - Value: Not Met, Latency: 1.89s

...

============================================================
📊 TEST SUMMARY
============================================================
Total Tests: 85
Successful: 81 (95.3%)
Failed: 4
Avg Latency: 2.12s

Value Distribution:
  Met: 67
  Not Met: 14
============================================================

📊 Results saved to: ultimate_results/multi_gpu_v100_type1_20251019_143052.csv
```

---

## Success Criteria ✅

- ✅ **Success Rate ≥ 95%** - Your server is stable!
- ✅ **Avg Latency < 5s** - Good performance
- ✅ **No errors** - Everything working

---

## What's Next? 🎯

### Test All Categories
```bash
python run_ultimate_test.py --model multi_gpu_v100 --data-types type1
```
**Time:** ~10-15 minutes (85 conversations × 5 categories = 425 tests)

### Test All Data Types
```bash
python run_ultimate_test.py --model multi_gpu_v100
```
**Time:** ~30-45 minutes (85 × 3 types × 5 categories = 1,275 tests)

### Add Another Server

1. Edit `config.yaml`:
```yaml
server3_rtx4000:
  name: "Mistral Base (RTX 4000)"
  endpoint: "http://SERVER3_IP:PORT/v1/chat/completions"
  enabled: true
```

2. Run:
```bash
python run_ultimate_test.py --model server3_rtx4000 --data-types type1 --categories opening
```

---

## Troubleshooting 🔧

### ❌ "Connection timeout"
**Fix:** Check server is running
```bash
curl http://192.168.30.252:8000/health
```

### ❌ "ModuleNotFoundError: ultimate_framework"
**Fix:** You're in wrong directory
```bash
cd /path/to/Parameter_Testing
python run_ultimate_test.py
```

### ❌ "No enabled models found"
**Fix:** Enable a model in `config.yaml`
```yaml
enabled: true  # Change from false to true
```

---

## Pro Tips 💡

1. **Start Small** - Test one category first
2. **Use Verbose** - Add `--verbose` flag to see more details
3. **Check Logs** - Review `ultimate_test.log` for full details
4. **Save Results** - Results are auto-saved with timestamps

---

## Full Command Reference

```bash
# Test everything (long!)
python run_ultimate_test.py

# Test specific model
python run_ultimate_test.py --model MODEL_ID

# Test specific data types
python run_ultimate_test.py --data-types type1 type2a

# Test specific categories
python run_ultimate_test.py --categories opening closing

# Combine options
python run_ultimate_test.py \
  --model multi_gpu_v100 \
  --data-types type1 \
  --categories opening closing hold

# Verbose mode (for debugging)
python run_ultimate_test.py --verbose
```

---

## Getting Help

1. Read: `ULTIMATE_FRAMEWORK_README.md` (comprehensive guide)
2. Check: `FEASIBILITY_ANALYSIS.md` (project details)
3. Review: `prompts.py` (assessment prompts)
4. Inspect: `ultimate_test.log` (detailed logs)

---

**Ready to test? Run this now:**

```bash
python run_ultimate_test.py --model multi_gpu_v100 --data-types type1 --categories opening
```

**Good luck! 🚀**

