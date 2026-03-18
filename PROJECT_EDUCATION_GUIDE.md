# 📚 Parameter Testing Project - Complete Learning Guide
## Learning Like You're 5 Years Old (LKG Style)

---

## 🎯 **PART 1: WHAT IS THIS PROJECT?**

### The Big Picture (Story Time!)

Imagine you're a **teacher** checking if your students (call center agents) followed the rules:
1. ✅ Did they say "Hello" properly? (Opening)
2. ✅ Did they ask for feedback? (Closing)
3. ✅ Did they put customers on hold politely? (Hold)
4. ✅ Did they reassure worried customers? (Reassurance)
5. ✅ Did they offer more help? (Further Assistance)

**Instead of checking 85 conversations manually**, this project uses **AI robots** (LLMs) to check automatically!

---

## 🏗️ **PART 2: PROJECT STRUCTURE (Like Building Blocks)**

```
Parameter_Testing/
├── 🎯 ENTRY POINT
│   └── run_ultimate_test.py          # You run this! (Main door)
│
├── ⚙️ CONFIGURATION
│   └── config.yaml                   # All settings in one place
│
├── 📝 PROMPTS (Questions for AI)
│   └── prompts.py                    # What to ask the AI
│
├── 🧱 FRAMEWORK (The Engine Room)
│   └── ultimate_framework/
│       ├── data_handler.py           # 📖 Reads conversation files
│       ├── model_client.py           # 📡 Talks to AI servers
│       ├── json_extractor.py         # 🔍 Finds answers in text
│       ├── conversation_truncator.py # ✂️ Shortens long chats
│       └── test_runner.py            # 🎮 Controls everything
│
├── 📊 DATA (Test Conversations)
│   └── data/
│       ├── type1_overall_paragraph.csv
│       ├── type2a_json/ (85 JSON files)
│       └── type2b_labeled_paragraph.csv
│
└── 📈 RESULTS
    └── ultimate_results/             # Where answers are saved
```

---

## 🔄 **PART 3: HOW THE CODE FLOWS (Step-by-Step Journey)**

### **FLOWCHART: What Happens When You Run `python run_ultimate_test.py`**

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: START                                                │
│ You type: python run_ultimate_test.py                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: READ CONFIG                                          │
│ run_ultimate_test.py → TestRunner → reads config.yaml       │
│ Finds: Which models? What data? Which categories?            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: LOAD DATA                                            │
│ TestRunner → DataHandler → Reads CSV/JSON files              │
│ Gets: 85 conversations ready to test                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: LOOP THROUGH EACH TEST                               │
│ For each conversation (85x) × each category (5 Examine questions) │
│ = 425 tests!                                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 5: BUILD PROMPT                                         │
│ TestRunner → Takes:                                           │
│   - Transcript (conversation text)                           │
│   - Prompt from prompts.py (the question)                    │
│   - Combines: "TRANSCRIPT + PROMPT"                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 6: CALL AI MODEL                                        │
│ TestRunner → ModelClient → Sends HTTP POST request           │
│ Waits for AI response...                                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 7: EXTRACT ANSWER                                       │
│ TestRunner → JSONExtractor → Finds JSON in response          │
│ Checks: {"Value": "Met", "Evidence": "..."}                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 8: SAVE RESULT                                          │
│ TestRunner → Saves to CSV file                               │
│ File: ultimate_results/{model}_{type}_{timestamp}.csv       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 9: REPEAT                                               │
│ Go back to STEP 4 until all tests done                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 10: PRINT SUMMARY                                       │
│ Shows: Success rate, Average latency, Results saved          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📡 **PART 4: POST REQUEST EXPLAINED (Like Sending a Letter)**

### **What is a POST Request?**

Think of it like **sending a letter** through the mail:
- **You** = Your Python code
- **Letter** = Your request (JSON data)
- **Mailbox** = Server URL (e.g., `http://192.168.30.252:8000/v1/chat/completions`)
- **Reply** = Server's response (JSON with AI answer)

### **POST Request Anatomy**

```python
import requests

# 1️⃣ THE ADDRESS (Where to send)
url = "http://192.168.30.252:8000/v1/chat/completions"

# 2️⃣ THE HEADERS (Like envelope labels)
headers = {
    "Content-Type": "application/json",  # Says "I'm sending JSON!"
    # "Authorization": "Bearer YOUR_KEY"  # If needed for security
}

# 3️⃣ THE MESSAGE (What you're asking)
body = {
    "model": "openchat/openchat-3.5-1210",  # Which AI to use
    "messages": [                             # The conversation
        {
            "role": "user",
            "content": "Hello! Can you check this conversation?..."
        }
    ],
    "temperature": 0.3,      # How creative? (0 = robot, 1 = creative)
    "max_tokens": 500        # Max response length
}

# 4️⃣ SEND IT!
response = requests.post(url, headers=headers, json=body, timeout=30)

# 5️⃣ CHECK IF SUCCESSFUL
if response.status_code == 200:
    data = response.json()
    ai_answer = data['choices'][0]['message']['content']
    print(f"AI said: {ai_answer}")
else:
    print(f"Error: {response.status_code}")
```

### **Breaking Down Each Part**

#### **1. URL (Uniform Resource Locator)**
```
http://192.168.30.252:8000/v1/chat/complet闻ions
│    │              │    │    │
│    │              │    │    └─── Path (what service you want)
│    │              │    └──────── Port number (like door number)
│    │              └────────────── Server address (like house address)
│    └───────────────────────────── Protocol (http = regular, https = secure)
```

#### **2. Headers (Metadata)**
- **Content-Type**: Tells server "I'm sending JSON, not text!"
- **Authorization**: Like a password (if server needs it)

#### **3. Body (Your Actual Request)**
- **model**: Which AI model to use
- **messages**: Array of conversation turns
  - `role: "user"` = What you say
  - `role: "system"` = Instructions to AI
- **temperature**: Randomness (0 = deterministic, 1 = creative)
- **max_tokens**: Maximum response length

#### **4. Response (What You Get Back)**
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "{\"Value\": \"Met\", \"Evidence\": \"Agent said hello...\"}"
      }
    }
  ]
}
```

### **How It Works in This Project**

Look at `ultimate_framework/model_client.py`:

```python
class vLLMClient(BaseModelClient):
    def generate(self, prompt: str, system_prompt: Optional[str] = None):
        # 1. Build messages array
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # 2. Build request body
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        # 3. Send POST request
        response = requests.post(
            self.endpoint,           # URL
            json=payload,            # Body (auto-converts to JSON)
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )
        
        # 4. Extract answer
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'response': data['choices'][0]['message']['content']
            }
        else:
            return {'success': False, 'error': response.text}
```

---

## 🏛️ **PART 5: FRAMEWORK ARCHITECTURE (Modularity)**

### **Why Modular Design? (Like LEGO Blocks)**

**Bad Code** (Monolithic - everything in one file):
```python
# terrible_code.py
# 1000 lines of mixed logic!
# Hard to debug, impossible to reuse
```

**Good Code** (Modular - separated concerns):
```python
# Each file does ONE job
data_handler.py      # Only reads data
model_client.py      # Only talks to AI
json_extractor.py    # Only extracts JSON
test_runner.py       # Only orchestrates
```

### **Design Pattern: Separation of Concerns**

Each module has a **single responsibility**:

| Module | What It Does | What It Doesn't Do |
|--------|-------------|-------------------|
| `data_handler.py` | Loads CSV/JSON files | Doesn't talk to AI |
| `model_client.py` | Sends HTTP requests | Doesn't parse responses |
| `json_extractor.py` | Extracts JSON from text | Doesn't send requests |
| `test_runner.py` | Orchestrates everything | Doesn't do the actual work |

### **Design Pattern: Factory Pattern**

See `model_client.py` - `ModelClientFactory`:

```python
class ModelClientFactory:
    @staticmethod
    def create_client(config):
        if config['type'] == 'vllm':
            return vLLMClient(config)  # Creates vLLM client
        elif config['type'] == 'gemini':
            return GeminiClient(config)  # Creates Gemini client
        # Easy to add new types!
```

**Why?** You can swap models without changing test code!

### **Design Pattern: Strategy Pattern**

See `json_extractor.py` - Multiple extraction strategies:

```python
class JSONExtractor:
    @staticmethod
    def extract(response_text):
        # Try Strategy 1: Direct parse
        result = _try_direct_parse(response_text)
        if result: return result
        
        # Try Strategy  Sweet 2: Markdown blocks
        result = _try_markdown_extraction(response_text)
        if result: return result
        
        # Try Strategy 3: Pattern matching
        result = _try_pattern_extraction(response_text)
        if result: return result
        
        # Try Strategy 4: Fix common errors
        result = _try_fix_and_parse(response_text)
        if result: return result
```

**Why?** If one method fails, try another automatically!

---

## 🌐 **PART 6: PROJECT SECTOR & INDUSTRY CONTEXT**

### **What Industry Is This?**

**Primary Sector**: **LLMOps / ML Evaluation**
- **Sub-sector**: Model Benchmarking & Quality Assurance
- **Application**: Call Center Quality Monitoring

### **Similar Projects In Industry**

1. **Hugging Face Evaluation Suite**: Tests models on benchmarks
2. **OpenAI Evals**: Evaluates GPT models
3. **LangChain Evaluators**: Tests RAG systems
4. **MLflow**: Tracks model performance

### **Real-World Use Cases**

- **Call Center QA**: Automated conversation analysis (YOUR PROJECT!)
- **Medical Diagnosis**: Testing AI diagnostic systems
- **Legal Tech**: Testing contract review AI
- **Customer Service**: Automated chat quality checks

---

## 🔧 **PART 7: HOW TO ADD A NEW API (Step-by-Step Guide)**

### **Scenario: You want to test "Claude API" (Anthropic)**

### **STEP 1: Understand the API** 📚

**What format does it use?**
- OpenAI-compatible? ✅ Use `vLLMClient`
- Custom format? 🔨 Create new client class
- Has SDK? 📦 Use SDK (like Gemini)

**Let's say Claude uses a different format:**

```python
# Claude API format (hypothetical)
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-3-sonnet",
  "max_tokens": 500,
  "messages": [...]
}
```

### **STEP 2: Create the Client Class** 🔨

**File**: `ultimate_framework/model_client.py`

**Add this new class:**

```python
class ClaudeClient(BaseModelClient):
    """Client for Anthropic Claude API"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.endpoint = config['endpoint']  # "https://api.anthropic.com/v1/messages"
        self.api_key = config['api_key']
        self.model_name = config['model_name']
        self.temperature = config.get('temperature', 0.3)
        self.max_tokens = config.get('max_tokens', 500)
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Generate response from Claude API"""
        start_time = time.time()
        
        # Build messages (Claude format)
        messages = []
        if system_prompt:
            # Claude might need system prompt differently
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Build request (Claude's format)
        payload = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        
        # Headers (Claude needs special header)
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,  # Claude uses x-api-key!
            "anthropic-version": "2023-06-01"
        }
        
        try:
            # Send POST request
            response = requests.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            latency = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                # Claude might return: data['content'][0]['text']
                response_text = data['content'][0]['text']
                
                return {
                    'success': True,
                    'response': response_text,
                    'latency': latency,
                    'model': self.name
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text}",
                    'latency': latency
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'latency': time.time() - start_time
            }
```

### **STEP 3: Update the Factory** 🏭

**In the same file, update `ModelClientFactory`:**

```python
class ModelClientFactory:
    @staticmethod
    def create_client(config: Dict[str, Any]) -> BaseModelClient:
        model_type = config.get('type', 'vllm').lower()
        
        if model_type == 'vllm':
            return vLLMClient(config)
        elif model_type == 'gemini':
            return GeminiClient(config)
        elif model_type == 'claude':  # ✨ NEW!
            return ClaudeClient(config)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
```

### **STEP 4: Add to Config** ⚙️

**File**: `config.yaml`

**Add new model section:**

```yaml
models:
  # ... existing models ...
  
  claude_sonnet:
    name: "Claude 3 Sonnet"
    type: "claude"  # ✨ This triggers ClaudeClient!
    endpoint: "https://api.anthropic.com/v1/messages"
    api_key: "YOUR_API_KEY_HERE"  # Or use env var
    model_name: "claude-3-sonnet-20240229"
    enabled: true  # ✨ Set to true to test
    temperature: 0.3
    max_tokens: 500
    timeout: 30
```

### **STEP 5: Test It!** 🧪

```bash
# Test your new model
python run_ultimate_test.py --model claude_sonnet --data-types type1 --categories opening
```

### **STEP 6: Handle Special Cases** 🔍

**What if Claude has different error handling?**

Add retry logic in `ClaudeClient.generate()`:

```python
def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
    # Try 3 times if rate limited
    for attempt in range(3):
        try:
            response = requests.post(...)
            
            # Claude-specific: Rate limit errors
            if response.status_code == 429:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            
            # ... rest of code ...
        except Exception as e:
            if attempt == 2:  # Last attempt
                return {'success': False, 'error': str(e)}
            time.sleep(1)
```

---

## 📋 **PART 8: UNDERSTANDING THE CODE - FILE BY FILE**

### **File 1: `run_ultimate_test.py`** (Entry Point)

**What it does:**
- Parses command-line arguments
- Sets up logging
- Creates TestRunner
- Starts testing

**Key code:**
```python
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='Which model to test')
    parser.add_argument('--data-types', nargs='+', help='Type1/2a/2b')
    parser.add_argument('--categories', nargs='+', help='opening/closing/etc')
    
    args = parser.parse_args()
    
    runner = TestRunner(config_path='config.yaml')
    runner.run_full_test(
        model_id=args.model,
        data_types=args.data_types,
        categories=args.categories
    )
```

### **File 2: `test_runner.py`** (The Orchestra Conductor)

**What it does:**
- Loads config
- Loads data
- Loops through tests
- Calls model clients
- Extracts JSON
- Saves results

**Key code flow:**
```python
class TestRunner:
    def run_full_test(self, model_id, data_types, categories):
        # 1. Get models to test
        models = self.get_enabled_models() if not model_id else {model_id: config[model_id]}
        
        # 2. Loop through each model
        for model_id, model_config in models.items():
            # 3. Loop through each data type
            for data_type in data_types:
                # 4. Load conversations
                conversations = self.data_handler.load_specific_type(data_type)
                
                # 5. Create model client
                client = ModelClientFactory.create_client(model_config)
                
                # 6. Loop through conversations × categories
                for conversation in conversations:
                    for category in categories:
                        # 7. Run single test
                        result = self.run_single_test(client, conversation, category)
                        
                        # 8. Save result
                        all_results.append(result)
                
                # 9. Save to CSV
                self._save_results(model_id, data_type, all_results)
```

### **File 3: `model_client.py`** (The Communicator)

**What it does:**
- Sends HTTP requests to AI servers
- Handles errors
- Returns standardized format

**Key pattern:**
```python
class BaseModelClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> Dict[str, Any]:
        """Must return: {success: bool, response: str, error: str}"""
        pass

class vLLMClient(BaseModelClient):
    def generate(self, prompt: str):
        # 1. Build request
        payload = {...}
        
        # 2. Send POST
        response = requests.post(self.endpoint, json=payload)
        
        # 3. Return standardized format
        return {
            'success': response.status_code == 200,
            'response': response.json()['choices'][0]['message']['content'],
            'latency': time.time() - start_time
        }
```

### **File 4: `data_handler.py`** (The Librarian)

**What it does:**
- Reads CSV files
- Reads JSON files
- Converts to standard format

**Key code:**
```python
class DataHandler:
    def load_type1(self):
        df = pd.read_csv('data/type1_overall_paragraph.csv')
        return [
            {
                'conversation_id': row['conversation_id'],
                'transcript': row['transcript'],
                'data_type': 'type1'
            }
            for _, row in df.iterrows()
        ]
```

### **File 5: `json_extractor.py`** (The Detective)

**What it does:**
- Finds JSON in messy AI responses
- Validates JSON format
- Fixes common errors

**Key strategies:**
```python
def extract(response_text):
    # Strategy 1: Direct parse
    try:
        return json.loads(response_text), ""
    except:
        pass
    
    # Strategy 2: Find in markdown
    match = re.search(r'```json\s*(\{.*?\})\s*```', response_text)
    if match:
        return json.loads(match.group(1)), ""
    
    # Strategy 3: Pattern match
    match = re.search(r'\{[^{}]*\}', response_text)
    if match:
        return json.loads(match.group(0)), ""
    
    # Strategy 4: Fix and retry
    fixed = fix_common_errors(response_text)
    return json.loads(fixed), ""
```

---

## 🎓 **PART 9: KEY CONCEPTS EXPLAINED**

### **1. HTTP Methods**

| Method | What It Does | When to Use |
|--------|-------------|-------------|
| **GET** | Read data | Revealing web pages, downloading files |
| **POST** | Send data | Sending forms, API requests (YOUR USE CASE!) |
| **PUT** | Replace data | Updating entire records |
| **DELETE** | Remove data | Deleting files |

**Your project uses POST because:**
- You're **sending** conversation transcripts
- You're **creating** a new analysis request
- You're not just reading (GET), you're asking for work

### **2. JSON (JavaScript Object Notation)**

**What is it?**
A way to represent data as text:

```json
{
  "name": "John",
  "age": 30,
  "skills": ["Python", "HTTP"]
}
```

**Why use it?**
- Easy for humans to read
- Easy for computers to parse
- Universal standard for APIs

**In your project:**
- **Request JSON**: What you send to AI
- **Response JSON**: What AI sends back

### **3. API Endpoint**

**What is it?**
A specific URL that does a specific job:

```
http://server.com/v1/chat/completions
                          └───────────┘
                          This is the endpoint
```

**Your project uses:**
- `/v1/chat/completions` - OpenAI-compatible endpoint
- Different APIs have different endpoints!

### **4. Status Codes**

**What are they?**
HTTP responses include a number telling you what happened:

| Code | Meaning | Example |
|------|---------|---------|
| 200 | ✅ Success | Everything worked! |
| 400 | ❌ Bad Request | You sent wrong data |
| 401 | 🔒 Unauthorized | Missing/invalid API key |
| 404 | 🔍 Not Found | Wrong URL |
| 429 | ⏱️ Too Many Requests | Rate limit exceeded |
| 500 | 💥 Server Error | Server has a problem |

**Your code checks:**
```python
if response.status_code == 200:
    # Success! Use the response
else:
    # Error! Log it and retry
```

### **5. Token Limits**

**What are tokens?**
- Words are broken into tokens
- Example: "Hello world" = 2 tokens
- Models have maximum context lengths (e.g., 8192 tokens)

**Why it matters:**
- If transcript + prompt > limit → Error!
- Solution: Truncate long conversations (`conversation_truncator.py`)

---

## 🚀 **PART 10: PRACTICAL EXERCISES**

### **Exercise 1: Test a Simple POST Request**

Create `test_post.py`:

```python
import requests

url = "http://192.168.30.252:8000/v1/chat/completions"
headers = {"Content-Type": "application/json"}
body = {
    "model": "openchat/openchat-3.5-1210",
    "messages": [{"role": "user", "content": "Say 'Hello' in arabic"}],
    "max_tokens": 50
}

response = requests.post(url, json=body, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

**Run it:**
```bash
python test_post.py
```

### **Exercise 2: Add Your Own Model Client**

Try adding support for a simple API:

1. Create `test_custom_client.py`
2. Implement a basic POST request
3. Mata it into the framework

### **Exercise 3: Debug a Failed Request**

When a request fails:
1. Check `response.status_code`
2. Print `response.text` (error message)
3. Check `config.yaml` (wrong endpoint?)
4. Test with `curl` first:
   ```bash
   curl -X POST http://192.168.30.252:8000/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"model": "test", "messages": [{"role": "user", "content": "hi"}]}'
   ```

---

## 📚 **PART 11: LEARNING RESOURCES**

### **HTTP/REST APIs**
- [MDN Web Docs - HTTP Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
- [REST API Tutorial](https://restfulapi.net/)

### **Python Requests Library**
- [Requests Documentation](https://requests.readthedocs.io/)
- [Real Python - HTTP Requests](https://realpython.com/python-requests/)

### **JSON**
- [JSON.org](https://www.json.org/json-en.html)
- [Python JSON Tutorial](https://docs.python.org/3/library/json.html)

### **Design Patterns**
- [Refactoring Guru - Design Patterns](https://refactoring.guru/design-patterns)
- [Factory Pattern](https://refactoring.guru/design-patterns/factory-method)

---

## ✅ **CHECKLIST: Do You Understand?**

- [ ] Can you explain what POST requests do?
- [ ] Can you identify where POST requests are made in the code?
- [ ] Can you explain why the project uses modular design?
- [ ] Can you trace the flow from `run_ultimate_test.py` to results?
- [ ] Can you add a new model client following the pattern?
- [ ] Do you understand what each framework module does?

---

## 🎯 **FINAL SUMMARY**

**This project is:**
1. **A Testing Framework** - Tests AI models systematically
2. **Modular Architecture** - Clean separation of concerns
3. **HTTP-Based** - Uses POST requests to communicate
4. **Configurable** - Settings in YAML, no code changes needed
5. **Extensible** - Easy to add new models/APIs

**Key Takeaways:**
- ✅ POST requests send data and get responses
- ✅ Modular code is easier to maintain and extend
- ✅ Factory pattern allows easy model swapping
- ✅ Separation of concerns makes code readable
- ✅ Error handling and retries make code robust

---

**You're now ready to understand and extend this project! 🎉**

