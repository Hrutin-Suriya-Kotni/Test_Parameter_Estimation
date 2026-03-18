#!/usr/bin/env python3
import json
import requests

# Test with the actual prompt format
prompt = '''You are an AI assistant that analyzes customer service conversations to determine if they meet specific guidelines. 

Guideline: OPENING
Description: The conversation should have a proper opening/greeting from the agent.

Please analyze the following conversation and respond with a JSON object containing:
- status: "Met" if the guideline is met, "Not Met" if not met
- value: The specific guideline being evaluated  
- evidence: Specific text from the conversation that supports your decision

Conversation: Good morning, this is सुमित. I am here to assist you today.'''

payload = {
    'model': 'Qwen/Qwen2.5-7B-Instruct',
    'messages': [
        {'role': 'system', 'content': prompt},
        {'role': 'user', 'content': 'Good morning, this is सुमित. I am here to assist you today.'}
    ],
    'max_tokens': 500,
    'temperature': 0.1
}

response = requests.post('http://27.111.72.51:8000/v1/chat/completions', json=payload)
result = response.json()
content = result['choices'][0]['message']['content']
print('Raw response:')
print(repr(content))
print()

# Test our parsing logic
cleaned_content = content.strip()
if cleaned_content.startswith('```json'):
    cleaned_content = cleaned_content[7:]
if cleaned_content.startswith('```'):
    cleaned_content = cleaned_content[3:]
if cleaned_content.endswith('```'):
    cleaned_content = cleaned_content[:-3]
cleaned_content = cleaned_content.strip()

print('Cleaned content:')
print(repr(cleaned_content))
print()

try:
    parsed_response = json.loads(cleaned_content)
    print('Parsed JSON:')
    print(json.dumps(parsed_response, indent=2))
    print()
    print('Status:', parsed_response.get('status', 'unknown'))
    print('Value:', parsed_response.get('value', 'unknown'))
    print('Evidence:', parsed_response.get('evidence', ''))
except Exception as e:
    print(f'Parse error: {e}')
