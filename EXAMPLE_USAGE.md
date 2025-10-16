# 🎓 Usage Examples - Generic Test Framework

Real-world examples showing how to use the generic testing framework.

---

## Example 1: Test Single Model (Most Common)

```bash
# Start the generic test runner
python3 generic_test.py

# You'll see:
# ===================================================================
# 🎯 GENERIC TEST RUNNER - Works with ANY Model!
# ===================================================================
#
# 📋 Available Models
# ===================================================================
# 
# ✅ READY TO USE:
#    • Mistral (Local) (mistral)
#      Local Mistral model via OpenChat server
#    • Google Gemini (gemini)
#      Google Gemini 2.0 Flash model via API
#
# ===================================================================
#
# 📋 Main Menu
# ----------------------------------------
#   1. Test single model
#   2. Test all available models
#   3. Compare models
#   4. Show model status
#   5. Exit
#
# Enter your choice (1-5): 1

# Select model:
# Available models:
#   1. Mistral (Local) (mistral)
#   2. Google Gemini (gemini)
#
# Select model (1-2): 2

# Choose test type:
# Options:
#   1. Run all tests
#   2. Run specific test type
#   3. Exit
#
# Enter your choice (1-3): 1

# Enter max conversations (or press Enter for all): 10
# 
# Will test 10 conversations on all 5 test types
# Results saved to: results/gemini/
```

---

## Example 2: Compare Two Models

```bash
python3 generic_test.py

# Main Menu: Enter 3 (Compare models)
# Select models to compare: 1,2
# Enter max conversations: 20

# Will test both models on same 20 conversations
# Side-by-side comparison shows agreement rates
# Results saved to: results/comparison/
```

---

## Example 3: Add Your Own API (OpenAI Example)

### Step 1: Copy Template
```bash
cp model_clients/generic_client.py model_clients/openai_client.py
```

### Step 2: Edit Client (3 methods only!)

```python
# model_clients/openai_client.py
import requests
import os
from model_clients.base_client import BaseModelClient
from model_config import ModelConfig

class OpenAIClient(BaseModelClient):
    def __init__(self):
        super().__init__("OpenAI")
        config = ModelConfig.get_model_config('openai') or {}
        cfg = config.get('config', {})
        
        self.api_url = cfg.get('api_url', 'https://api.openai.com/v1/chat/completions')
        self.model = cfg.get('model', 'gpt-4')
        self.max_tokens = cfg.get('max_tokens', 512)
        self.temperature = cfg.get('temperature', 0.1)
        self.api_key = None
    
    def initialize(self) -> bool:
        """Load API key and test connection"""
        try:
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                print("❌ OPENAI_API_KEY not found in .env")
                return False
            
            if self.test_connection():
                self.initialized = True
                return True
            return False
        except Exception as e:
            print(f"OpenAI initialization failed: {e}")
            return False
    
    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        """Send conversation to OpenAI API"""
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
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {str(e)}"
    
    def test_connection(self) -> bool:
        """Test if OpenAI API is accessible"""
        try:
            response = self.analyze_conversation("Test", "Test transcript")
            return not response.startswith("Error:")
        except:
            return False
```

### Step 3: Add Configuration

```python
# In model_config.py, add to AVAILABLE_MODELS dict:

'openai': {
    'class_name': 'OpenAIClient',
    'module_path': 'model_clients.openai_client',
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

### Step 4: Add API Key

```bash
# Add to .env file
echo "OPENAI_API_KEY=sk-your-key-here" >> .env
```

### Step 5: Test It!

```bash
# Check status
python3 model_config.py

# Should show:
# ✅ OpenAI GPT-4 (openai)
#    Description: OpenAI GPT-4 via API

# Run tests
python3 generic_test.py
# Select OpenAI from menu
# Test with 5 conversations first
```

---

## Example 4: Automated Testing Script

```python
#!/usr/bin/env python3
"""
my_automated_test.py - Custom automated testing
"""

from generic_test import GenericTestRunner, compare_models

# Test single model
print("🧪 Testing Gemini model...")
gemini_runner = GenericTestRunner('gemini')

if gemini_runner.model_client:
    # Test just "opening" conversations with 10 samples
    gemini_runner.test_single_type('opening', max_conversations=10)
    
    # Or test all types with 20 samples
    results = gemini_runner.test_all_types(max_conversations=20)
    
    print(f"✅ Tests completed!")
    print(f"Results: {results}")
else:
    print("❌ Gemini not available")

# Compare multiple models
print("\n🔍 Comparing Gemini vs Mistral...")
compare_models(
    model_names=['gemini', 'mistral'],
    test_type='opening',  # Just compare on opening
    max_conversations=15
)
```

Run it:
```bash
python3 my_automated_test.py
```

---

## Example 5: Test All Models in Batch

```python
#!/usr/bin/env python3
"""
batch_test_all.py - Test all available models
"""

from model_config import ModelConfig
from generic_test import GenericTestRunner

# Get all available models
models_status = ModelConfig.get_available_models_with_status()
available_models = [
    name for name, info in models_status.items() 
    if info['status']['available']
]

print(f"📊 Testing {len(available_models)} models...")

for model_name in available_models:
    print(f"\n{'='*60}")
    print(f"🧪 Testing {model_name}")
    print(f"{'='*60}")
    
    runner = GenericTestRunner(model_name)
    if runner.model_client:
        # Test all types with 10 conversations each
        results = runner.test_all_types(max_conversations=10)
        
        print(f"✅ {model_name} completed")
    else:
        print(f"❌ {model_name} failed to initialize")

print("\n🎉 All models tested!")
```

---

## Example 6: Local Model (Ollama)

### Add Ollama Support

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
        return self.test_connection()
    
    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        try:
            enhanced_prompt = f"{prompt}\n\nTranscript:\n{transcript}"
            
            data = {
                "model": self.model,
                "messages": [{"role": "user", "content": enhanced_prompt}],
                "stream": False
            }
            
            response = requests.post(self.api_url, json=data, timeout=120)
            response.raise_for_status()
            return response.json()["message"]["content"]
        except Exception as e:
            return f"Error: {str(e)}"
    
    def test_connection(self) -> bool:
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
```

### Add Config

```python
# In model_config.py:
'ollama': {
    'class_name': 'OllamaClient',
    'module_path': 'model_clients.ollama_client',
    'display_name': 'Ollama (Local)',
    'description': 'Local Ollama server running Llama2',
    'requires_api_key': False,
    'api_key_env_var': None,
    'config': {
        'api_url': 'http://localhost:11434/api/chat',
        'model': 'llama2',
        'temperature': 0.1
    }
}
```

### Test It

```bash
# Start Ollama server first
ollama serve

# In another terminal
python3 generic_test.py
# Select Ollama from menu
```

---

## Example 7: Testing Best Practices

```python
#!/usr/bin/env python3
"""
best_practices_test.py - Recommended testing workflow
"""

from generic_test import GenericTestRunner

def test_new_model(model_name: str):
    """
    Best practice testing workflow for a new model
    """
    print(f"🧪 Testing {model_name} model...")
    
    runner = GenericTestRunner(model_name)
    
    if not runner.model_client:
        print(f"❌ {model_name} failed to initialize")
        return False
    
    # Step 1: Test with 1 conversation first
    print("\n📝 Step 1: Testing with 1 conversation...")
    result = runner.test_single_type('opening', max_conversations=1)
    if not result:
        print("❌ Failed on single conversation test")
        return False
    
    # Step 2: Test with 5 conversations
    print("\n📝 Step 2: Testing with 5 conversations...")
    result = runner.test_single_type('opening', max_conversations=5)
    if not result:
        print("❌ Failed on 5 conversation test")
        return False
    
    # Step 3: Test all types with 10 conversations
    print("\n📝 Step 3: Testing all types with 10 conversations...")
    results = runner.test_all_types(max_conversations=10)
    
    if all(results.values()):
        print(f"✅ {model_name} passed all tests!")
        
        # Step 4: Scale up to full dataset
        print("\n📝 Step 4: Ready for full dataset!")
        print(f"Run: runner.test_all_types()  # No limit")
        return True
    else:
        print(f"❌ Some tests failed: {results}")
        return False

# Test a new model
test_new_model('openai')
```

---

## Common Commands Reference

```bash
# Check what models are available
python3 model_config.py

# Run generic test runner (interactive)
python3 generic_test.py

# Test specific model programmatically
python3 -c "
from generic_test import GenericTestRunner
runner = GenericTestRunner('gemini')
runner.test_all_types(max_conversations=10)
"

# Compare two models
python3 -c "
from generic_test import compare_models
compare_models(['gemini', 'mistral'], max_conversations=10)
"

# View results
ls -la results/gemini/
cat results/gemini/opening_test_results_*.csv
```

---

## Troubleshooting Examples

### Problem: Model not showing up

```bash
# Check status
python3 model_config.py

# Common issues:
# 1. API key missing in .env
# 2. Wrong module_path in config
# 3. Class name doesn't match

# Debug: Test import directly
python3 -c "
from model_clients.my_model_client import MyModelClient
client = MyModelClient()
print(client.initialize())
"
```

### Problem: JSON parsing errors

```python
# In your client, add debugging:
def analyze_conversation(self, prompt: str, transcript: str) -> str:
    response = self.api_call(prompt, transcript)
    
    # Debug: Print raw response
    print(f"DEBUG - Raw response: {response}")
    
    return response
```

---

## Summary

**For New Users:**
1. Start with `python3 generic_test.py`
2. Test with 5 conversations first
3. Review results in `results/` folder
4. Scale up gradually

**For Adding New Models:**
1. Copy `generic_client.py`
2. Implement 3 methods
3. Add to `model_config.py`
4. Test with `generic_test.py`

**For Production Use:**
1. Test with sample data first
2. Monitor API costs/quotas
3. Check results quality
4. Scale to full dataset

🎉 That's it! The generic framework handles everything else automatically.


