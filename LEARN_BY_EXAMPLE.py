#!/usr/bin/env python3
"""
🎓 LEARN BY EXAMPLE - Hands-on tutorial for understanding the project
Run this script step-by-step to see how everything works!
"""

# ============================================================================
# LESSON 1: UNDERSTANDING POST REQUESTS (Like sending a letter)
# ============================================================================

print("=" * 70)
print("📮 LESSON 1: What is a POST Request?")
print("=" * 70)

# Imagine you want to ask an AI a question
# You need to "POST" (send) your question to the server

import requests  # This library helps us send HTTP requests

# Step 1: The address where the AI lives
url = "http://192.168.30.252:8000/v1/chat/completions"

# Step 2: What you're sending (like the letter content)
letter_content = {
    "model": "openchat/openchat-3.5-1210",  # Which AI to use
    "messages": [
        {
            "role": "user",
            "content": "Say 'Hello' in Spanish, then stop."
        }
    ],
    "temperature": 0.3,
    "max_tokens": 50
}

# Step 3: Label on the envelope (headers)
envelope_label = {
    "Content-Type": "application/json"  # "This letter contains JSON!"
}

print("\n📍 Step 1: Preparing your request...")
print(f"   URL: {url}")
print(f"   Model: {letter_content['model']}")
print(f"   Question: {letter_content['messages'][0]['content']}")

print("\n⏳ Step 2: Sending POST request...")
print("   (This is like dropping your letter in a mailbox)")

try:
    # This is THE POST REQUEST! 🎯
    response = requests.post(
        url,                    # Where to send
        json=letter_content,    # What to send (auto-converts to JSON)
        headers=envelope_label, # Metadata
        timeout=10              # Wait max 10 seconds
    )
    
    # Step 4: Did it work?
    if response.status_code == 200:
        print("\n✅ Step 3: Success! Got a response!")
        answer = response.json()
        ai_response = answer['choices'][0]['message']['content']
        print(f"   AI Said: {ai_response}")
    else:
        print(f"\n❌ Step 3: Error! Status code: {response.status_code}")
        print(f"   Error message: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ Connection failed! Is the server running?")
    print("   (This is okay for learning - the code is correct!)")
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + uploading + "*" * 70 + "\n")

# ============================================================================
# LESSON 2: UNDERSTANDING MODULAR CODE (Like LEGO blocks)
# ============================================================================

print("🧱 LESSON 2: Why Modular Code? (Lego Blocks)")
print("=" * 70)

# BAD CODE (everything in one function):
print("\n❌ BAD CODE - Everything mixed together:")
bad_code_example = """
def do_everything():
    # Read file
    with open('data.csv', 'r') as f:
        data = f.read()
    
    # Process data
    processed = data.split(',')
    
    # Send to server
    requests.post('http://server.com', json=processed)
    
    # Parse response
    response = requests.post(...)
    result = json.loads(response.text)
    
    # Save to file
    with open('result.txt', 'w') as f:
        f.write(result)
    
    # Hard to test! Hard to debug! Hard to reuse!
"""
print(bad_code_example)

# GOOD CODE (modular - each function does one thing):
print("\n✅ GOOD CODE - Each function does ONE job:")
good_code_example = """
# Module 1: Read data
def read_data(filename):
    with open(filename, 'r') as f:
        return f.read()

# Module 2: Process data
def process_data(raw_data):
    return raw_data.split(',')

# Module 3: Send to server
def send_request(processed_data):
    return requests.post('http://server.com', json=processed_data)

# Module 4: Parse response
def parse_response(response):
    return json.loads(response.text)

# Module 5: Save result
def save_result(result, filename):
    with open(filename, 'w') as f:
        f.write(result)

# Now you can:
# - Test each function separately!
# - Reuse functions in other projects!
# - Debug easily (know exactly where problem is!)
"""
print(good_code_example)

print("\n" + "=" * 70 + "\n")

# ============================================================================
# LESSON 3: UNDERSTANDING THE FLOW (Step by step)
# ============================================================================

print("🔄 LESSON 3: How Your Project Works (Step by Step)")
print("=" * 70)

# Simulate what happens when you run: python run_ultimate_test.py

print("\n📝 Step 1: Load Configuration")
config = {
    'models': {
        'test_model': {
            'name': 'Test Model',
            'endpoint': 'http://192.168.30.252:8000/v1/chat/completions',
            'enabled': True
        }
    },
    'data': {
        'base_path': './data'
    }
}
print(f"   ✅ Loaded config with {len(config['models'])} model(s)")

print("\n📊 Step 2: Load Test Data")
# Simulate loading a conversation
test_conversation = {
    'conversation_id': 'test-123',
    'transcript': 'agent: Hello, how can I help? customer: Hi there!',
    'data_type': 'type1'
}
print(f"   ✅ Loaded conversation: {test_conversation['conversation_id']}")

print("\n📝 Step 3: Build Prompt")
from prompts import ASSESSMENT_PROMPTS
category = 'opening'
prompt = ASSESSMENT_PROMPTS.get(category, '')
full_prompt = f"{test_conversation['transcript']}\n\n{prompt}"
print(f"   ✅ Built prompt for category: {category}")
print(f"   📏 Prompt length: {len(full_prompt)} characters")

print("\n📡 Step 4: Send to AI (POST Request)")
print("   (This is where Lesson 1 POST request happens!)")
print("   ⏳ Sending request...")
print("   ⏳ Waiting for response...")
print("   ✅ Got response!")

print("\n🔍 Step 5: Extract JSON from Response")
# Simulate JSON extraction
simulated_response = """Here is my assessment:
```json
{
    "Value": "Met",
    "Evidence": "The agent said 'Hello'"
}
```"""
import re
json_match = re.search(r'\{[^{}]*\}', simulated_response)
if json_match:
    print(f"   ✅ Found JSON: {reference_match.group(0)}")
else:
    print("   ❌ No JSON found")

print("\n💾 Step 6: Save Result")
result = {
    'conversation_id': test_conversation['conversation_id'],
    'category': category,
    'success': True,
    'value': 'Met'
}
print(f"   ✅ Saved result: {result}")

print("\n🎉 Step 7: Repeat for all conversations!")
print("   (85 conversations × 5 categories = 425 tests)")

print("\n" + "=" * 70 + "\n")

# ============================================================================
# LESSON 4: UNDERSTANDING ERROR HANDLING
# ============================================================================

print("🛡️  LESSON 4: Error Handling (What if something goes wrong?)")
print("=" * 70)

def safe_post_request(url, data, max_retries=3):
    """
    This shows how to handle errors gracefully
    (This is how your project handles errors!)
    """
    for attempt in range(max_retries):
        try:
            print(f"\n   Attempt {attempt + 1}/{max_retries}...")
            response = requests.post(url, json=data, timeout=5)
            
            if response.status_code == 200:
                print("   ✅ Success!")
                return {'success': True, 'data': response.json()}
            elif response.status_code == 429:
                print("   ⏱️  Rate limited! Waiting...")
                import time
                time.sleep(2 ** attempt)  # Wait longer each retry
            else:
                print(f"   ❌ Error {response.status_code}: {response.text}")
                return {'success': False, 'error': response.text}
                
        except requests.exceptions.Timeout:
            print("   ⏱️  Timeout! Server took too long.")
            if attempt < max_retries - 1:
                print("   🔄 Retrying...")
        except requests.exceptions.ConnectionError:
            print("   🔌 Connection error! Is server running?")
            return {'success': False, 'error': 'Connection failed'}
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
            return {'success': False, 'error': str(e)}
    
    return {'success': False, 'error': 'All retries failed'}

print("\n🔍 Example: Making a safe request (with error handling)")
print("   (This won't actually run if server isn't available, but you see the pattern)")

result = safe_post_request(
    url="http://example.com/api",
    data={"test": "data"}
)
print(f"\n   Final result: {result}")

print("\n" + "=" * 70 + "\n")

# ============================================================================
# LESSON 5: UNDERSTANDING JSON
# ============================================================================

print("📦 LESSON 5: Understanding JSON Format")
print("=" * 70)

import json

# JSON is just a way to represent data as text
print("\n📝 What is JSON?")
print("   JSON = JavaScript Object Notation")
print("   It's a way to structure data so both humans and computers can read it")

# Example JSON objects
example_json = {
    "name": "John Doe",
    "age": 30,
    "skills": ["Python", "HTTP", "JSON"],
    "active": True
}

print("\n📦 Example JSON object:")
print(json.dumps(example_json, indent=2))

print("\n🔄 Converting JSON to string (for sending):")
json_string = json.dumps(example_json)
print(f"   String: {json_string}")
print(f"   Type: {type(json_string)}")

print("\n🔄 Converting string back to JSON (after receiving):")
parsed_back = json.loads(json_string)
print(f"   Parsed: {parsed_back}")
print(f"   Type: {type(parsed_back)}")

print("\n📋 In your project:")
print("   Request body (what you send) = JSON → string")
print("   Response (what you get) = string → JSON")

print("\n" + "=" * 70 + "\n")

# ============================================================================
# LESSON 6: PRACTICAL EXERCISE
# ============================================================================

print("🎯 LESSON 6: Practice Exercise - Build a Simple Test")
print("=" * 70)

print("""
Try this yourself:

1. Create a file called: my_first_test.py

2. Copy this code:

```python
import requests
import json

# Configuration
url = "http://192.168.30.252:8000/v1/chat/completions"
headers = {"Content-Type": "application/json"}

# Test data
conversation = "agent: Hello, how can I help? customer: Hi there!"

# Build request
request_data = {
    "model": "openchat/openchat-3.5-1210",
    "messages": [
        {
            "role": "user",
            "content": f"{conversation}\\n\\nDid the agent greet the customer properly? Answer with JSON: {{\"answer\": \"yes\" or \"no\"}}"
        }
    ],
    "temperature": 0.3,
    "max_tokens": 100
}

# Send POST request
print("Sending request...")
response = requests.post(url, json=request_data, headers=headers, timeout=30)

# Check result
if response.status_code == 200:
    result = response.json()
    ai_answer = result['choices'][0]['message']['content']
    print(f"✅ Success!")
    print(f"AI Response: {ai_answer}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
```

3. Run it: python my_first_test.py

4. Modify it:
   - Change the conversation text
   - Change the question
   - Try different models

This is exactly what your project does, but on a larger scale!
""")

print("\n" + "=" * 70)
print("🎓 LESSONS COMPLETE!")
print("=" * 70)
print("\nYou now understand:")
print("  ✅ What POST requests are")
print("  ✅ Why modular code is better")
print("  ✅ How your project flows")
print("  ✅ How to handle errors")
print("  ✅ What JSON is")
print("\nNext: Read PROJECT_EDUCATION_GUIDE.md for deeper understanding!")
print("=" * 70 + "\n")

