#!/usr/bin/env python3
import json

# Test the parsing fix
content = '''```json
{
  "status": "Met",
  "value": "OPENING",
  "evidence": "Good morning, this is सुमित. I am here to assist you today."
}
```'''

# Clean the content - remove markdown code blocks if present
cleaned_content = content.strip()
if cleaned_content.startswith('```json'):
    cleaned_content = cleaned_content[7:]  # Remove ```json
if cleaned_content.startswith('```'):
    cleaned_content = cleaned_content[3:]   # Remove ```
if cleaned_content.endswith('```'):
    cleaned_content = cleaned_content[:-3]  # Remove trailing ```
cleaned_content = cleaned_content.strip()

print('Cleaned content:')
print(repr(cleaned_content))
print()

try:
    parsed_response = json.loads(cleaned_content)
    print('✅ Parse successful!')
    print(json.dumps(parsed_response, indent=2))
except json.JSONDecodeError as e:
    print(f'❌ Parse error: {e}')
