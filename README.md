# CRED Conversation Analysis - Modular Architecture

A modular, scalable Python tool for analyzing CRED customer service conversations using multiple AI models.

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```

### 2. Run Tests
```bash
# Easy launcher (recommended)
python3 run_tests.py

# Or run individual tests
python3 test_runners/test_mistral.py
python3 test_runners/test_gemini.py
python3 test_runners/test_comparison.py
```

### 3. Check Model Status
```bash
python3 model_config.py
```

## 📁 Project Structure

```
Check_DATA/
├── model_clients/           # AI model implementations
│   ├── base_client.py      # Abstract base class
│   ├── mistral_client.py   # Mistral model client
│   └── gemini_client.py    # Gemini model client
├── test_runners/           # All test files
│   ├── test_mistral.py     # Mistral-specific tests
│   ├── test_gemini.py      # Gemini-specific tests
│   ├── test_comparison.py  # Model comparison tests
│   └── run_all_models.py   # Master test runner
├── results/                # Organized results storage
│   ├── mistral/           # Mistral results
│   ├── gemini/            # Gemini results
│   └── comparison/        # Comparison results
├── run_tests.py           # Easy test launcher
├── model_config.py        # Model configuration
└── [core files...]        # Data processing, prompts, etc.
```

## 🤖 Available Models

- **Mistral** (Local) - Via OpenChat server
- **Gemini** (Cloud) - Google Gemini 2.0 Flash API

## 📊 Test Types

1. **Opening** - Agent greeting and introduction protocols
2. **Closing** - Call closing and feedback request protocols  
3. **Reassurance** - Customer reassurance statements
4. **Hold** - Proper hold request procedures
5. **Further Assistance** - Additional help offers

## 🔧 Adding New Models

1. Create model client in `model_clients/new_model_client.py`
2. Add configuration to `model_config.py`
3. Create test runner in `test_runners/test_new_model.py`

## 📖 Documentation

For detailed usage instructions, see `MODULAR_README.md`.

## 🆘 Support

- Check console output for error messages
- Verify API keys in `.env` file
- Ensure data files are in correct location
- Run `python3 model_config.py` to check model status
