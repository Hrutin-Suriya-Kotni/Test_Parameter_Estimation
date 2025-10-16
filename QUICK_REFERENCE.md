# 📚 Quick Reference Guide

One-page reference for the Generic Testing Framework.

---

## 🚀 Quick Commands

```bash
# Check available models and their status
python3 model_config.py

# Run tests (interactive)
python3 generic_test.py

# Test specific model programmatically
python3 -c "
from generic_test import GenericTestRunner
runner = GenericTestRunner('gemini')
runner.test_all_types(max_conversations=10)
"
```

---

## 📝 Add New Model (5-Minute Checklist)

### ✅ Step 1: Create Client (2 minutes)
```bash
cp model_clients/generic_client.py model_clients/YOUR_MODEL_client.py
```

Edit 3 methods in `YOUR_MODEL_client.py`:
- `initialize()` - Load API key
- `analyze_conversation()` - Make API call  
- `test_connection()` - Test API

### ✅ Step 2: Add Config (1 minute)
```python
# In model_config.py, add to AVAILABLE_MODELS:
'your_model': {
    'class_name': 'YourModelClient',
    'module_path': 'model_clients.YOUR_MODEL_client',
    'display_name': 'Your Model Name',
    'description': 'Description',
    'requires_api_key': True,
    'api_key_env_var': 'YOUR_MODEL_API_KEY',
    'config': {
        'api_url': 'https://api.yourmodel.com/v1/chat',
        'model': 'your-model-v1',
        'max_tokens': 512,
        'temperature': 0.1
    }
}
```

### ✅ Step 3: Add API Key (30 seconds)
```bash
echo "YOUR_MODEL_API_KEY=your_key_here" >> .env
```

### ✅ Step 4: Test (1 minute)
```bash
python3 generic_test.py
```

**Done!** Your model works with all test runners automatically.

---

## 🎯 Common API Patterns

### OpenAI-Compatible APIs
Works for: OpenAI, Mistral, Groq, Together AI, etc.

```python
def analyze_conversation(self, prompt: str, transcript: str) -> str:
    response = requests.post(
        self.api_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        },
        json={
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Respond with ONLY JSON"},
                {"role": "user", "content": f"{prompt}\n\nTranscript:\n{transcript}"}
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        },
        timeout=60
    )
    return response.json()["choices"][0]["message"]["content"]
```

### SDK-Based APIs
Works for: Google Gemini, Anthropic Claude, etc.

```python
def initialize(self) -> bool:
    import your_model_sdk
    your_model_sdk.configure(api_key=self.api_key)
    self.client = your_model_sdk.Client(model=self.model)
    return self.test_connection()

def analyze_conversation(self, prompt: str, transcript: str) -> str:
    response = self.client.generate(
        prompt=f"{prompt}\n\nTranscript:\n{transcript}",
        max_tokens=self.max_tokens,
        temperature=self.temperature
    )
    return response.text
```

### Local Models
Works for: Ollama, LocalAI, vLLM, etc.

```python
def initialize(self) -> bool:
    return self.test_connection()  # No API key needed

def analyze_conversation(self, prompt: str, transcript: str) -> str:
    response = requests.post(
        self.api_url,
        json={
            "model": self.model,
            "prompt": f"{prompt}\n\nTranscript:\n{transcript}"
        }
    )
    return response.json()["response"]
```

---

## 📊 File Structure

```
Parameter_Testing/
├── generic_test.py           # ⭐ Use this! Works with ALL models
├── generic_client.py          # ⭐ Copy this to add new models
├── INTEGRATION_GUIDE.md       # 📖 Complete integration guide
├── QUICK_REFERENCE.md         # 📖 This file
├── EXAMPLE_USAGE.md           # 📖 Real-world examples
├── model_config.py            # ⚙️  All model configurations
├── prompts.py                 # 📝 Assessment prompts
├── data_loader.py             # 📊 Data loading
└── model_clients/             # 🤖 Model implementations
    ├── generic_client.py      # Template with examples
    ├── base_client.py         # Base class
    ├── mistral_client.py      # Mistral example
    └── gemini_client.py       # Gemini example
```

---

## 🔧 Testing Workflow

### For New Models
1. Test with 1 conversation
2. Test with 5 conversations  
3. Test with 10 conversations
4. Test all types with 20 conversations
5. Scale to full dataset

### Commands
```bash
# Step 1-3: Quick validation
python3 generic_test.py
# Select model → Run specific test → Enter: 1, 5, 10

# Step 4: Comprehensive test
python3 generic_test.py
# Select model → Run all tests → Enter: 20

# Step 5: Full dataset
python3 generic_test.py
# Select model → Run all tests → Press Enter (no limit)
```

---

## 📈 Results

Results are automatically saved to:
```
results/
├── mistral/
│   ├── opening_test_results_TIMESTAMP.csv
│   ├── closing_test_results_TIMESTAMP.csv
│   └── ...
├── gemini/
│   └── ...
└── your_model/
    └── ...
```

Each CSV contains:
- conversation_id
- result (Met/Not Met)
- evidence
- response_time
- success status

---

## 🐛 Troubleshooting

### Model not showing
```bash
python3 model_config.py  # Check status
# Fix: Check API key in .env, verify config syntax
```

### Import errors
```bash
python3 -c "from model_clients.YOUR_MODEL_client import YourModelClient; print('OK')"
# Fix: Check class name, file name, imports
```

### Connection errors
```python
# In your client, test connection manually:
def test_connection(self) -> bool:
    try:
        # Add debug output
        print(f"Testing connection to: {self.api_url}")
        response = self.analyze_conversation("Test", "Test")
        print(f"Response: {response}")
        return not response.startswith("Error:")
    except Exception as e:
        print(f"Connection failed: {e}")
        return False
```

### JSON parsing errors
```python
# Ensure your prompt includes clear JSON instructions:
enhanced_prompt = f"""{prompt}

CRITICAL: Respond with ONLY valid JSON. No text before or after.
Required format: {{"Value": "Met" or "Not Met", "Evidence": "explanation"}}

Transcript:
{transcript}"""
```

---

## 🎓 Documentation Files

| File | Purpose |
|------|---------|
| `INTEGRATION_GUIDE.md` | Complete step-by-step guide to add models |
| `EXAMPLE_USAGE.md` | Real-world usage examples |
| `QUICK_REFERENCE.md` | This file - quick reference |
| `README.md` | Project overview |
| `MODULAR_README.md` | Detailed architecture docs |

---

## 💡 Pro Tips

1. **Always test small first**: Start with 1-5 conversations
2. **Use generic_test.py**: Don't create separate test files
3. **Copy generic_client.py**: It has working examples for OpenAI and Claude
4. **Check model_config.py**: Ensure your config is correct
5. **Monitor costs**: Track API usage for paid models
6. **Review results**: Check CSV files after each test

---

## 🆘 Getting Help

1. Read `INTEGRATION_GUIDE.md` for detailed explanations
2. Check `EXAMPLE_USAGE.md` for real examples
3. Look at existing clients: `mistral_client.py`, `gemini_client.py`
4. Test imports: `python3 -c "from model_clients.YOUR_MODEL_client import YourModelClient"`
5. Check status: `python3 model_config.py`

---

## 📞 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Model not found" | Add to `model_config.py` AVAILABLE_MODELS |
| "API key not found" | Add to `.env` file |
| "Module not found" | Check `module_path` in config |
| "Class not found" | Check `class_name` matches Python class |
| "Connection failed" | Test API endpoint manually |
| "JSON parsing error" | Add JSON format instructions to prompt |
| "Timeout error" | Increase timeout in requests or reduce max_tokens |

---

**Remember**: The generic framework eliminates code duplication. One test runner, many models! 🚀


