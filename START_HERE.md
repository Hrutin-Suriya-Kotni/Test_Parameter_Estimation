# 🚀 START HERE - Generic Testing Framework

**Welcome!** This framework makes it incredibly easy to test conversation analysis with **ANY AI model**.

---

## 🎯 What Can You Do?

### ✅ Test Existing Models
```bash
python3 generic_test.py
```
Currently available:
- Mistral (Local)
- Google Gemini

### ✅ Add Your Own Model (5 Minutes!)
1. Copy template
2. Add 3 methods
3. Add config
4. Test!

**That's it!** Your model automatically works with everything.

---

## 📚 Which Document Should I Read?

### 🆕 New to This Project?
**→ Read**: `README.md`
- Project overview
- Quick start commands
- Basic concepts

### 🔧 Want to Add Your Own API?
**→ Read**: `QUICK_REFERENCE.md` (start here - 1 page!)
- 5-minute checklist
- Common patterns
- Quick commands

**→ Then**: `INTEGRATION_GUIDE.md` (detailed guide)
- Step-by-step instructions
- Real-world examples (OpenAI, Claude, Ollama)
- Troubleshooting

### 💡 Want Examples?
**→ Read**: `EXAMPLE_USAGE.md`
- Copy-paste examples
- Testing workflows
- Automated scripts

### 🏗️ Understanding Architecture?
**→ Read**: `MODULAR_README.md`
- System architecture
- How it works internally
- Advanced concepts

### 🆘 Quick Troubleshooting?
**→ Read**: `QUICK_REFERENCE.md`
- Common issues & fixes
- Command reference
- Quick tips

### 📊 What Changed?
**→ Read**: `CHANGES_SUMMARY.md`
- What's new
- Benefits
- Migration guide

---

## ⚡ Quick Commands

```bash
# Check available models
python3 model_config.py

# Run tests interactively
python3 generic_test.py

# Test specific model with code
python3 -c "
from generic_test import GenericTestRunner
runner = GenericTestRunner('gemini')
runner.test_all_types(max_conversations=10)
"

# Compare models
python3 generic_test.py
# Select option 3 (Compare models)
```

---

## 🎓 Learning Path

### Beginner
```
1. README.md (5 min) - Overview
2. python3 generic_test.py (5 min) - Try it!
3. QUICK_REFERENCE.md (10 min) - Quick guide
```

### Adding Your First Model
```
1. QUICK_REFERENCE.md (5 min) - Checklist
2. INTEGRATION_GUIDE.md (10 min) - Detailed steps
3. EXAMPLE_USAGE.md (5 min) - Find your API type
4. model_clients/generic_client.py - Copy & customize
```

### Advanced Usage
```
1. MODULAR_README.md - Architecture
2. model_clients/base_client.py - Base interface
3. test_runners/base_test_runner.py - Test framework
4. Create custom test scripts
```

---

## 🗂️ File Structure

```
📁 Parameter_Testing/
│
├── 📘 START_HERE.md                    ← You are here!
├── 📘 README.md                        ← Project overview
├── 📘 QUICK_REFERENCE.md               ← 1-page quick guide
├── 📘 INTEGRATION_GUIDE.md             ← Complete guide to add models
├── 📘 EXAMPLE_USAGE.md                 ← Real examples
├── 📘 CHANGES_SUMMARY.md               ← What's new
│
├── 🐍 generic_test.py                  ← Universal test runner (USE THIS!)
├── 🐍 model_config.py                  ← Model configurations
├── 🐍 prompts.py                       ← Assessment prompts
├── 🐍 data_loader.py                   ← Data loading
│
├── 📁 model_clients/
│   ├── 🐍 generic_client.py            ← Template (COPY THIS!)
│   ├── 🐍 base_client.py               ← Base class
│   ├── 🐍 mistral_client.py            ← Mistral example
│   └── 🐍 gemini_client.py             ← Gemini example
│
├── 📁 test_runners/                    ← Legacy (still works)
├── 📁 results/                         ← Test results saved here
└── 📁 data/                            ← Excel data files
```

---

## 🎯 Use Cases

### Use Case 1: Test Your Conversations
```bash
# Interactive testing
python3 generic_test.py

# 1. Select model
# 2. Choose test type (opening, closing, etc.)
# 3. Enter number of conversations
# 4. Results saved in results/ folder
```

### Use Case 2: Add OpenAI GPT-4
```bash
# 1. Copy template
cp model_clients/generic_client.py model_clients/openai_client.py

# 2. Implement 3 methods (see INTEGRATION_GUIDE.md)

# 3. Add to model_config.py
'openai': {
    'class_name': 'OpenAIClient',
    'module_path': 'model_clients.openai_client',
    'display_name': 'OpenAI GPT-4',
    ...
}

# 4. Add API key
echo "OPENAI_API_KEY=sk-your-key" >> .env

# 5. Test it!
python3 generic_test.py
```

### Use Case 3: Compare Multiple Models
```bash
python3 generic_test.py
# Select: Compare models
# Choose: 1,2 (compare two models)
# Results show agreement rates
```

### Use Case 4: Automated Testing
```python
# my_test.py
from generic_test import GenericTestRunner

runner = GenericTestRunner('gemini')
results = runner.test_all_types(max_conversations=20)
print(f"Tests completed: {results}")
```

---

## 💡 Key Concepts

### 1. Generic Framework
- **One test runner** works with ALL models
- **One template** to add any API
- **Zero code duplication**

### 2. Configuration-Driven
All settings in `model_config.py`:
- API endpoints
- Model names
- Parameters
- API keys

### 3. Automatic Discovery
System automatically:
- Finds available models
- Loads configurations
- Initializes clients
- Runs tests

### 4. Test Types
5 conversation analysis types:
- **Opening** - Greeting & introduction
- **Closing** - Farewell & feedback
- **Reassurance** - Customer assurance
- **Hold** - Hold procedures
- **Further Assistance** - Additional help

---

## 🚦 Getting Started (5 Minutes)

### Step 1: Check Setup (1 min)
```bash
# Verify Python packages
pip install -r requirements.txt

# Check available models
python3 model_config.py
```

### Step 2: Try It (2 min)
```bash
# Run the generic test runner
python3 generic_test.py

# Follow the interactive prompts
# Test with 5 conversations first
```

### Step 3: Review Results (1 min)
```bash
# Results are in results/ folder
ls -la results/

# View a result file
cat results/gemini/opening_test_results_*.csv
```

### Step 4: Add Your Model (1 min to start)
```bash
# Read the quick guide
cat QUICK_REFERENCE.md

# Follow 5-minute checklist
# See INTEGRATION_GUIDE.md for details
```

---

## ❓ FAQ

### Q: Do I need to create separate test files for each model?
**A:** No! Use `generic_test.py` - it works with all models automatically.

### Q: How do I add my own API?
**A:** Copy `generic_client.py`, implement 3 methods, add config. See `INTEGRATION_GUIDE.md`.

### Q: What if my API is different from the examples?
**A:** `generic_client.py` has examples for REST APIs, SDKs, and local models. One will match your needs.

### Q: Can I still use the old test runners?
**A:** Yes! All existing code works. But `generic_test.py` is easier and recommended.

### Q: Where are results saved?
**A:** In `results/model_name/` folder as CSV files with timestamps.

### Q: How do I test with my own data?
**A:** Place Excel file in `data/` folder and update `model_config.py` DATA_CONFIG.

### Q: Can I compare models?
**A:** Yes! `generic_test.py` has built-in model comparison feature.

---

## 🎉 Benefits

### For You
✅ Easy to use - one command to test  
✅ Easy to extend - 5 minutes to add models  
✅ Well documented - 5 comprehensive guides  
✅ No duplication - clean, maintainable code  

### For Your Team
✅ Anyone can add models (with template)  
✅ Consistent testing across all models  
✅ Automatic result tracking  
✅ Easy to compare model performance  

---

## 📞 Next Steps

1. **Try It Now**:
   ```bash
   python3 generic_test.py
   ```

2. **Read Quick Reference**:
   ```bash
   cat QUICK_REFERENCE.md
   ```

3. **Add Your Model**:
   - Read `INTEGRATION_GUIDE.md`
   - Copy `generic_client.py`
   - Follow 5-minute checklist

4. **Explore Examples**:
   ```bash
   cat EXAMPLE_USAGE.md
   ```

---

## 🆘 Need Help?

| Issue | Solution |
|-------|----------|
| Don't know where to start | Read this file, then `README.md` |
| Want to add a model | Read `QUICK_REFERENCE.md`, then `INTEGRATION_GUIDE.md` |
| Need examples | Read `EXAMPLE_USAGE.md` |
| Having errors | Check `QUICK_REFERENCE.md` troubleshooting section |
| Understanding architecture | Read `MODULAR_README.md` |

---

## 🎊 Summary

**You have 3 options:**

### Option 1: Use Existing Models
```bash
python3 generic_test.py
```

### Option 2: Add Your Model
```bash
# Read: QUICK_REFERENCE.md (5-min checklist)
# Copy: generic_client.py
# Test: python3 generic_test.py
```

### Option 3: Learn Everything
```bash
# Read all documentation
# Explore the code
# Create custom scripts
```

**Start with Option 1, then try Option 2!** 🚀

---

**Made with ❤️ for easy AI model testing**

