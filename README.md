# CRED Conversation Analysis - Generic Framework

A **reusable, zero-duplication** Python framework for analyzing CRED customer service conversations using **ANY AI model**.

## ⚡ What's New - Generic Components

✅ **`generic_client.py`** - Template to add ANY AI API in minutes  
✅ **`generic_test.py`** - One test runner for ALL models (no duplication!)  
✅ **`INTEGRATION_GUIDE.md`** - Step-by-step guide for new models  

**No more creating separate test files for each model!**

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```

### 2. Run Tests (Generic Way - Works with ALL Models!)
```bash
# Universal test runner - works with ANY model
python3 generic_test.py

# Or use the old way
python3 run_tests.py
```

### 3. Add Your Own Model (Takes 5 Minutes!)
```bash
# 1. Copy template
cp model_clients/generic_client.py model_clients/my_model_client.py

# 2. Edit 3 methods in my_model_client.py

# 3. Add config to model_config.py

# 4. Test it!
python3 generic_test.py

# See INTEGRATION_GUIDE.md for details
```

### 4. Check Model Status
```bash
python3 model_config.py
```

## 📁 Project Structure

```
Parameter_Testing/
├── 🆕 generic_test.py           # Universal test runner (works with ALL models!)
├── 🆕 INTEGRATION_GUIDE.md      # How to add your own model
├── model_clients/                # AI model implementations
│   ├── 🆕 generic_client.py     # Template for ANY API (copy & customize)
│   ├── base_client.py           # Abstract base class
│   ├── mistral_client.py        # Mistral model client
│   └── gemini_client.py         # Gemini model client
├── test_runners/                 # Individual test runners (legacy)
│   ├── base_test_runner.py     # Shared test functionality
│   ├── test_mistral.py          # Mistral tests (use generic_test.py instead!)
│   ├── test_gemini.py           # Gemini tests (use generic_test.py instead!)
│   ├── test_comparison.py       # Model comparison
│   └── run_all_models.py        # Master test runner
├── results/                      # Organized results storage
│   ├── mistral/                 # Mistral results
│   ├── gemini/                  # Gemini results
│   └── comparison/              # Comparison results
├── run_tests.py                 # Menu launcher (legacy)
├── model_config.py              # Centralized model configuration
├── prompts.py                   # Assessment prompts & guidelines
├── data_loader.py               # Data loading utilities
└── requirements.txt             # Python dependencies
```

**🔥 Use `generic_test.py` instead of individual test runners!**

## 🎯 Why Use Generic Components?

### Before (Code Duplication 😞)
```python
# Had to create separate files for each model:
test_mistral.py      # 147 lines
test_gemini.py       # 147 lines  
test_claude.py       # 147 lines
test_gpt4.py         # 147 lines
# = 588 lines of duplicated code!
```

### After (Zero Duplication 🎉)
```python
# One file works for ALL models:
generic_test.py      # 300 lines, works with ANY model!
generic_client.py    # Template with examples

# To add a new model:
# 1. Copy template (30 seconds)
# 2. Implement 3 methods (5 minutes)
# 3. Add config (1 minute)
# Done! Automatic integration with all test runners
```

## 🤖 Available Models

- **Mistral** (Local) - Via OpenChat server
- **Gemini** (Cloud) - Google Gemini 2.0 Flash API
- **🆕 Your Model** - Add any API in 5 minutes! See `INTEGRATION_GUIDE.md`

## 📊 Test Types

1. **Opening** - Agent greeting and introduction protocols
2. **Closing** - Call closing and feedback request protocols  
3. **Reassurance** - Customer reassurance statements
4. **Hold** - Proper hold request procedures
5. **Further Assistance** - Additional help offers

## 🔧 Adding New Models (Easy!)

### Option 1: Use Generic Template (Recommended)
```bash
# 1. Copy template
cp model_clients/generic_client.py model_clients/my_api_client.py

# 2. Edit just 3 methods:
#    - initialize()         # Load API key
#    - analyze_conversation()  # Make API call
#    - test_connection()    # Test API

# 3. Add to model_config.py:
'my_api': {
    'class_name': 'MyAPIClient',
    'module_path': 'model_clients.my_api_client',
    'display_name': 'My API',
    'description': 'My custom API',
    'requires_api_key': True,
    'api_key_env_var': 'MY_API_KEY',
    'config': {
        'api_url': 'https://api.myapi.com/chat',
        'model': 'my-model-v1',
        'max_tokens': 512,
        'temperature': 0.1
    }
}

# 4. Add API key to .env:
echo "MY_API_KEY=your_key_here" >> .env

# 5. Test it!
python3 generic_test.py
```

**No need to create separate test runners anymore!** `generic_test.py` works with any model automatically.

### Option 2: Legacy Way (Not Recommended)
1. Create model client in `model_clients/new_model_client.py`
2. Add configuration to `model_config.py`
3. Create test runner in `test_runners/test_new_model.py` (lots of duplicated code!)

## 📖 Documentation

- **`INTEGRATION_GUIDE.md`** - Complete guide to add your own AI model (5 minutes!)
- **`MODULAR_README.md`** - Detailed architecture and legacy usage instructions
- **`README.md`** - This file (quick start & overview)

## 🆘 Support

- Check console output for error messages
- Verify API keys in `.env` file
- Ensure data files are in correct location
- Run `python3 model_config.py` to check model status
