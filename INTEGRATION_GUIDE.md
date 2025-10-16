# 🚀 Integration Guide - Add Your Own AI Model

This guide shows you how to integrate **ANY AI model** into the testing framework with minimal effort.

## ⚡ Quick Start (5 Minutes)

### Option A: Using the Generic Template (Recommended)

```bash
# 1. Copy the generic template
cp model_clients/generic_client.py model_clients/my_model_client.py

# 2. Edit 3 methods in my_model_client.py (see below)

# 3. Add config to model_config.py (copy-paste example)

# 4. Add API key to .env file (if needed)
echo "MY_MODEL_API_KEY=your_key_here" >> .env

# 5. Test it!
python3 generic_test.py
```

**That's it! Your model will automatically work with all test runners.**

---

## 📝 Step-by-Step Integration

### Step 1: Create Your Model Client

**Option 1: Use Generic Template (Easiest)**

```python
# model_clients/my_model_client.py
from model_clients.generic_client import GenericClient

class MyModelClient(GenericClient):
    API_TYPE = "my_model"  # Change this
    
    # Only implement these 3 methods:
    def initialize(self) -> bool:
        # Load API key, initialize client
        pass
    
    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        # Make API call, return response
        pass
    
    def test_connection(self) -> bool:
        # Test if API is working
        pass
```

**Option 2: Full Example (REST API)**

```python
# model_clients/my_model_client.py
import requests
import os
from model_clients.base_client import BaseModelClient
from model_config import ModelConfig

class MyModelClient(BaseModelClient):
    def __init__(self):
        super().__init__("MyModel")
        
        # Load config from model_config.py
        config = ModelConfig.get_model_config('my_model') or {}
        cfg = config.get('config', {})
        
        self.api_url = cfg.get('api_url', 'https://api.mymodel.com/chat')
        self.model = cfg.get('model', 'my-model-v1')
        self.max_tokens = cfg.get('max_tokens', 512)
        self.temperature = cfg.get('temperature', 0.1)
        self.api_key = None
    
    def initialize(self) -> bool:
        try:
            self.api_key = os.getenv("MY_MODEL_API_KEY")
            if not self.api_key:
                return False
            
            if self.test_connection():
                self.initialized = True
                return True
            return False
        except Exception as e:
            print(f"Initialization failed: {e}")
            return False
    
    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        try:
            enhanced_prompt = f"""{prompt}

CRITICAL: Respond with ONLY valid JSON.
{{"Value": "Met" or "Not Met", "Evidence": "explanation"}}

Transcript:
{transcript}"""
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You respond with ONLY valid JSON."},
                    {"role": "user", "content": enhanced_prompt}
                ],
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            # Adjust based on your API response format
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {str(e)}"
    
    def test_connection(self) -> bool:
        try:
            response = self.analyze_conversation("Test", "Test")
            return not response.startswith("Error:")
        except:
            return False
```

---

### Step 2: Add Configuration

Edit `model_config.py` and add your model:

```python
# In model_config.py, inside AVAILABLE_MODELS dict:

'my_model': {
    'class_name': 'MyModelClient',
    'module_path': 'model_clients.my_model_client',
    'display_name': 'My Model Name',
    'description': 'Description of your model',
    'requires_api_key': True,  # or False for local models
    'api_key_env_var': 'MY_MODEL_API_KEY',  # or None
    'config': {
        'api_url': 'https://api.mymodel.com/v1/chat',
        'model': 'my-model-v1',
        'max_tokens': 512,
        'temperature': 0.1
    }
}
```

---

### Step 3: Add API Key (if needed)

Create/edit `.env` file:

```bash
# .env
MY_MODEL_API_KEY=your_actual_api_key_here
GEMINI_API_KEY=existing_keys_here
```

---

### Step 4: Test Your Integration

```bash
# Check model status
python3 model_config.py

# Test your model
python3 generic_test.py
# Select your model from menu
# Test with a small number of conversations first (e.g., 5)
```

---

## 🎯 Real-World Examples

### Example 1: OpenAI GPT-4

```python
# model_clients/openai_client.py
from model_clients.generic_client import OpenAIClient
# Already implemented in generic_client.py!
```

```python
# Add to model_config.py:
'openai': {
    'class_name': 'OpenAIClient',
    'module_path': 'model_clients.generic_client',
    'display_name': 'OpenAI GPT-4',
    'description': 'OpenAI GPT-4 via API',
    'requires_api_key': True,
    'api_key_env_var': 'OPENAI_API_KEY',
    'config': {
        'api_url': 'https://api.openai.com/v1/chat/completions',
        'model': 'gpt-4',
        'max_tokens': 512,
        'temperature': 0.1
    }
}
```

```bash
# .env
OPENAI_API_KEY=sk-your-key-here
```

---

### Example 2: Anthropic Claude

```python
# model_clients/claude_client.py
from model_clients.generic_client import AnthropicClient
# Already implemented in generic_client.py!
```

```python
# Add to model_config.py:
'anthropic': {
    'class_name': 'AnthropicClient',
    'module_path': 'model_clients.generic_client',
    'display_name': 'Claude 3.5 Sonnet',
    'description': 'Anthropic Claude via API',
    'requires_api_key': True,
    'api_key_env_var': 'ANTHROPIC_API_KEY',
    'config': {
        'api_url': 'https://api.anthropic.com/v1/messages',
        'model': 'claude-3-5-sonnet-20241022',
        'max_tokens': 512,
        'temperature': 0.1
    }
}
```

---

### Example 3: Local Model (Ollama)

```python
# model_clients/ollama_client.py
import requests
from model_clients.base_client import BaseModelClient
from model_config import ModelConfig

class OllamaClient(BaseModelClient):
    def __init__(self):
        super().__init__("Ollama")
        config = ModelConfig.get_model_config('ollama') or {}
        cfg = config.get('config', {})
        self.api_url = cfg.get('api_url', 'http://localhost:11434/api/chat')
        self.model = cfg.get('model', 'llama2')
        self.temperature = cfg.get('temperature', 0.1)
    
    def initialize(self) -> bool:
        # No API key needed for local model
        return self.test_connection()
    
    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        try:
            enhanced_prompt = f"{prompt}\n\nTranscript:\n{transcript}"
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": enhanced_prompt}
                ],
                "stream": False,
                "options": {
                    "temperature": self.temperature
                }
            }
            
            response = requests.post(self.api_url, json=data, timeout=120)
            response.raise_for_status()
            result = response.json()
            return result["message"]["content"]
        except Exception as e:
            return f"Error: {str(e)}"
    
    def test_connection(self) -> bool:
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
```

```python
# Add to model_config.py:
'ollama': {
    'class_name': 'OllamaClient',
    'module_path': 'model_clients.ollama_client',
    'display_name': 'Ollama (Local)',
    'description': 'Local Ollama server',
    'requires_api_key': False,
    'api_key_env_var': None,
    'config': {
        'api_url': 'http://localhost:11434/api/chat',
        'model': 'llama2',
        'temperature': 0.1
    }
}
```

---

## 🧪 Testing Workflow

### 1. Test with Sample Data First

```bash
# Test with just 5 conversations
python3 generic_test.py
# Select your model
# Choose "Run all tests"
# Enter: 5 (for max conversations)
```

### 2. Check Results

```bash
# Results are saved in: results/your_model/
ls -la results/your_model/

# Review the CSV files
cat results/your_model/opening_test_results_*.csv
```

### 3. Scale Up

```bash
# If sample tests work, run on full dataset
python3 generic_test.py
# Select your model
# Choose "Run all tests"
# Press Enter (for all conversations)
```

---

## 📊 Using Your New Model

### Single Model Testing

```bash
python3 generic_test.py
# Select "Test single model"
# Choose your model
# Select test type or run all
```

### Compare Models

```bash
python3 generic_test.py
# Select "Compare models"
# Choose multiple models (e.g., 1,2,3)
# Results show side-by-side comparison
```

### Automated Testing

```python
# Create a custom script: my_automated_test.py
from generic_test import GenericTestRunner

# Test your model
runner = GenericTestRunner('my_model')
if runner.model_client:
    results = runner.test_all_types(max_conversations=10)
    print(f"Tests completed! Results: {results}")
```

---

## 🔧 Common API Patterns

### Pattern 1: OpenAI-Compatible APIs

Many APIs use OpenAI format (Mistral, Together AI, Groq, etc.):

```python
# Works for: OpenAI, Mistral, Groq, Together AI, etc.
def analyze_conversation(self, prompt: str, transcript: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {self.api_key}"
    }
    
    data = {
        "model": self.model,
        "messages": [
            {"role": "system", "content": "You respond with ONLY JSON."},
            {"role": "user", "content": f"{prompt}\n\nTranscript:\n{transcript}"}
        ],
        "max_tokens": self.max_tokens,
        "temperature": self.temperature
    }
    
    response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
    return response.json()["choices"][0]["message"]["content"]
```

### Pattern 2: SDK-Based APIs

For APIs with Python SDKs (Google, Anthropic, etc.):

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

### Pattern 3: Local Models

For local servers (Ollama, LocalAI, vLLM, etc.):

```python
def initialize(self) -> bool:
    # No API key needed
    return self.test_connection()

def analyze_conversation(self, prompt: str, transcript: str) -> str:
    # Usually simpler - just POST to local endpoint
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

## ⚠️ Troubleshooting

### Issue: Model not showing in menu

**Solution:**
```bash
# Check model status
python3 model_config.py

# Common fixes:
# 1. Check model name spelling in config
# 2. Verify API key in .env
# 3. Check class_name matches your Python class
# 4. Check module_path is correct
```

### Issue: JSON parsing errors

**Solution:**
```python
# In your analyze_conversation(), ensure you:
# 1. Tell the model to respond ONLY with JSON
# 2. Show the exact format required
# 3. Handle non-JSON responses gracefully

enhanced_prompt = f"""{prompt}

CRITICAL: Respond with ONLY valid JSON. No explanation before or after.
Required format: {{"Value": "Met" or "Not Met", "Evidence": "explanation"}}

Transcript:
{transcript}"""
```

### Issue: Timeout errors

**Solution:**
```python
# Increase timeout in your requests
response = requests.post(url, json=data, timeout=120)  # 2 minutes

# Or in config:
'config': {
    'timeout': 120,
    'max_tokens': 256  # Reduce tokens for faster response
}
```

### Issue: Rate limiting

**Solution:**
```python
# In base_test_runner.py, adjust sleep time:
# Line ~134: time.sleep(2)  # Change to 5 or more

# Or in your test script:
runner = GenericTestRunner('my_model')
# Add delay between API calls in your client
```

---

## 📚 Best Practices

### 1. Start Small
```bash
# Always test with 5-10 conversations first
python3 generic_test.py
# Enter: 5
```

### 2. One Test Type at a Time
```bash
# Don't run all 5 test types immediately
# Start with "opening" test only
# Verify results before scaling
```

### 3. Monitor Costs
```python
# Add cost tracking to your client
def analyze_conversation(self, prompt: str, transcript: str) -> str:
    response = self.api_call(prompt, transcript)
    
    # Log token usage
    tokens_used = response.get('usage', {}).get('total_tokens', 0)
    print(f"Tokens used: {tokens_used}")
    
    return response.text
```

### 4. Save Raw Responses
```python
# Useful for debugging
def analyze_conversation(self, prompt: str, transcript: str) -> str:
    response = self.api_call(prompt, transcript)
    
    # Save raw response
    with open(f'logs/{self.model_name}_response.json', 'a') as f:
        json.dump(response, f)
    
    return response.text
```

---

## 🎓 Learning Resources

### Understanding the Framework

1. **Base Classes**: Read `model_clients/base_client.py` - Shows what you need to implement
2. **Existing Examples**: Check `mistral_client.py` and `gemini_client.py` - Real working examples
3. **Generic Template**: Study `generic_client.py` - Documented template with examples

### Testing Your Model

1. **Unit Test**: `python3 -m pytest test_your_model.py` (create simple tests)
2. **Connection Test**: `python3 model_config.py` (check status)
3. **Sample Run**: `python3 generic_test.py` (5 conversations)
4. **Full Run**: `python3 generic_test.py` (all conversations)

---

## 🚀 Next Steps

1. ✅ Copy `generic_client.py` → `your_model_client.py`
2. ✅ Implement 3 methods (initialize, analyze_conversation, test_connection)
3. ✅ Add config to `model_config.py`
4. ✅ Add API key to `.env`
5. ✅ Test with `python3 model_config.py`
6. ✅ Run tests with `python3 generic_test.py`
7. ✅ Compare with other models
8. ✅ Scale to full dataset

**Need help?** Check the examples in `generic_client.py` or existing clients!

---

## 📞 Support

- **Check Status**: `python3 model_config.py`
- **View Logs**: Check `results/your_model/*.csv` for detailed results
- **Debug**: Add print statements in your client's methods
- **Examples**: Look at `mistral_client.py`, `gemini_client.py`, or `generic_client.py`

Happy testing! 🎉


