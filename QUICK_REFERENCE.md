 explaining
# 🚀 Quick Reference Guide - Parameter Testing Project

---

## 📋 **TWO-MINUTE OVERVIEW**

**What this project does:**
1. Reads 85 call center conversations from files
2. Tip: Send each conversation to AI models (Gemini, OpenChat, Qwen, etc.)
3. Asks: "Did the agent follow guidelines?" (5 questions per conversation)
4. Collects all answers
5. Saves results to CSV files
6. Compares which model performs best

---

## 🔑 **KEY CONCEPTS (One-Liners)**

| Concept | Simple Explanation |
|---------|-------------------|
| **POST Request** | Sending data to a server and getting a response back |
| **HTTP** | Language computers use to talk to each other |
| **JSON** | Text format for structured data (like a dictionary in text form) |
| **API Endpoint** | Specific URL that does a specific job |
| **Modular Code** | Code split into separate files, each doing one job |
| **Factory Pattern** | A function that creates the right object based on settings |
| **Token Limit** | Maximum length of text a model can process |

---

## 📁 **FILE PURPOSES (At a Glance)**

```
run_ultimate_test.py          → You run this! (Main entry point)
config.yaml                    → All settings (models, paths, etc.)
prompts.py                     → Questions to ask the AI

ultimate_framework/
├── data_handler.py           → Reads CSV/JSON conversation files
├── model_client.py           → Sends POST requests to AI servers
├── json_extractor.py         → Finds JSON in messy AI responses
├── conversation_truncator.py → Shortens conversations if too long
└── test_runner.py            → Controls the entire testing process
```

---

## 🔄 **HOW DATA FLOWS**

```
CSV/JSON Files
    ↓
data_handler.py (reads files)
    ↓
test_runner.py (loops through conversations)
    ↓
prompts.py (builds questions)
    ↓
model_client.py (sends POST request)
    ↓
AI Server (processes and responds)
    ↓
לient.py (receives response)
    ↓
json_extractor.py (finds JSON answer)
    ↓
test_runner.py (saves to CSV)
    ↓
Results CSV File
```

---

## 🌐 **POST REQUEST TEMPLATE**

```python
import requests

# 1. Where to send
url = "http://SERVER:PORT/v1/chat/completions"

# 2. What to send
body = {
    "model": "model-name",
    "messages": [
        {"role": "user", "content": "Your question here"}
    ],
    "temperature": 0.3,
    "max_tokens": 500
}

# 3. Headers
headers = {"Content-Type": "application/json"}

# 4. Send it!
response = requests.post(url, json=body, headers=headers, timeout=30)

# 5. Check result
if response.status_code == 200:
    data = response.json()
    answer = data['choices'][0]['message']['content']
    print(answer)
else:
    print(f"Error: {response.status_code}")
```

---

## ➕ **HOW TO ADD A NEW API (3 STEPS)**

### **Step 1: Create Client Class**

In `ultimate_framework/model_client.py`, add:

```python
class NewAPIClient(BaseModelClient):
    def __init__(self, config):
        super().__init__(config)
        self.endpoint = config['endpoint']
        self.api_key = config.get('api_key')
    
    def generate(self, prompt: str, system_prompt=None):
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        body = {
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": self.max_tokens
        }
        
        response = requests.post(self.endpoint, json=body, headers=headers)
        
        if response.status_code == 200:
            return {
                'success': True,
                'response': response.json()['content']  # Adjust based on API
            }
        else:
            return {'success': False, 'error': response.text}
```

### **Step 2: Update Factory**

In same file, update `ModelClientFactory.create_client()`:

```python
if model_type == 'newapi':  # ✨ Add this
    return NewAPIClient(config)
```

### **Step 3: Add to Config**

In `config.yaml`:

```yaml
models:
  new_api_model:
    name: "My New API"
    type: "newapi"  # ✨ Matches factory
    endpoint: "http://server.com/api"
    api_key: "YOUR_KEY"
    enabled: true
```

---

## 🎯 **COMMON COMMANDS**

```bash
# Run all enabled models
python run_ultimate_test.py

# Run specific model
python run_ultimate_test.py --model multi_gpu_v100_qwen

# Run specific data type
python run_ultimate_test.py --data-types type1

# Run specific category
python run_ultimate_test.py --categories opening

# Combine options
python run_ultimate_test.py --model multi_gpu_v100_qwen --data-types type1 --categories opening

# Verbose mode (see more details)
python run_ultimate_test.py --verbose
```

---

## 🐛 **DEBUGGING CHECKLIST**

When something doesn't work:

- [ ] Is the server running? `curl http://SERVER:PORT/health`
- [ ] Is `config.yaml` correct? (Check endpoint, model name)
- [ ] Is model `enabled: true` in config?
- [ ] Check logs: `ultimate_test.log`
- [ ] Check results CSV for error messages
- [ ] Try verbose mode: `--verbose`
- [ ] Test with simple POST request first (see `LEARN_BY_EXAMPLE.py`)

---

## 📊 **UNDERSTANDING RESULTS**

**CSV Columns:**
- `conversation_id` - Which conversation
- `category` - Which guideline (opening/closing/etc)
- `success` - Did it work? (True/False)
- `value` - "Met" or "Not Met"
- `evidence` - Quote/she said
- `latency` - How long it took (seconds)
- `error` - Error message (if failed)

**Success Criteria:**
- ✅ Success rate ≥ 95%
- ✅ Average latency < 5 seconds
- ✅ JSON parse rate ≥ 95%

---

## 🔍 **CODE PATTERNS TO REMEMBER**

### **Pattern 1: Error Handling**
```python
try:
    response = requests.post(...)
    if response.status_code == 200:
        return {'success': True, 'data': response.json()}
    else:
        return {'success': False, 'error': response.text}
except Exception as e:
    return {'success': False, 'error': str(e)}
```

### **Pattern 2: Retry Logic**
```python
for attempt in range(3):
    result = do_something()
    if result favored success:
        return result
    time.sleep(2)  # Wait before retry
return result  # Give up after 3 tries
```

### **Pattern 3: Factory Pattern**
```python
if config['type'] == 'vllm':
    return vLLMClient(config)
elif config['type'] == 'gemini':
    return GeminiClient(config)
# Easy to add new types!
```

---

## 📚 **WHAT TO LEARN NEXT**

1. ✅ Understand this project (you're here!)
2. 📖 Read HTTP basics (MDN Web Docs)
3. 🐍 Master Python `requests` library
4. 📦 Learn JSON format deeply
5. 🏗️ Study design patterns (Factory, Strategy)
6. 🔧 Practice by adding a new API

---

## 🎓 **TEST YOUR UNDERSTANDING**

Answer these questions:

1. **What does a POST request do?**
   - [ ] Sends data to server and gets response
   - [ ] Downloads files from internet
   - [ ] Deletes data from server

2. **Why is modular code better?**
   - [ ] It's shorter
   - [ ] Each file does one job, easier to test/debug
   - [ ] It runs faster

3. **Where does the AI response come from?**
   - [ ] config.yaml
   - [ ] HTTP POST request to server
   - [ ] prompts.py

4. **What is the purpose of json_extractor.py?**
   - [ ] To send requests
   - [ ] To find JSON in messy AI responses
   - [ ] To save results

5. **To add a new API, you need to:**
   - [ ] Modify run_ultimate_test.py
   - [ ] Create client class + update factory + add config
   - [ ] Change prompts.py

**Answers:** 1-A, 2-B, 3-B, 4-B, 5-B

---

## 💡 **PRO TIPS**

1. **Start Small**: Test one conversation, one category first
2. **Read Logs**: `ultimate_test.log` has detailed information
3. **Use Verbose**: `--verbose` shows everything happening
4. **Test Server First**: Use `curl` or simple Python script before running full test
5. **Save Config Backups**: Before changing `config.yaml`, save a copy
6. **Check Rate Limits**: Some APIs limit requests per minute

---

## 🆘 **WHEN STUCK**

1. Check `PROJECT_EDUCATION_GUIDE.md` for deep explanations
2. Run `LEARN_BY_EXAMPLE.py` to see code in action
3. Check error messages in:
   - Console output
   - `ultimate_test.log`
   - Results CSV `error` column
4. Test POST request manually first
5. Verify config.yaml syntax (must be valid YAML)

---

**Remember: Coding is like learning a language. Start simple, practice a lot, and you'll get fluent! 🚀**

