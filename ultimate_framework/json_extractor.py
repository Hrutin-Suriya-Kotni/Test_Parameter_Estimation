"""
Robust JSON Extraction - Extract structured data from LLM responses
Handles various formats and edge cases
"""

import json
import re
from typing import Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class JSONExtractor:
    """Robust JSON extraction from LLM responses"""
    
    @staticmethod
    def extract(response_text: str) -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Extract JSON from LLM response using multiple strategies
        
        Args:
            response_text: Raw text response from LLM
        
        Returns:
            Tuple of (extracted_dict, error_message)
            If successful: (dict, "")
            If failed: (None, error_message)
        """
        # Strategy 1: Try direct JSON parse
        result, error = JSONExtractor._try_direct_parse(response_text)
        if result:
            return result, ""
        
        # Strategy 2: Extract from markdown code blocks
        result, error = JSONExtractor._try_markdown_extraction(response_text)
        if result:
            return result, ""
        
        # Strategy 3: Find JSON-like patterns
        result, error = JSONExtractor._try_pattern_extraction(response_text)
        if result:
            return result, ""
        
        # Strategy 4: Fix common issues and retry
        result, error = JSONExtractor._try_fix_and_parse(response_text)
        if result:
            return result, ""
        
        # All strategies failed
        logger.error(f"Failed to extract JSON. Tried all strategies. Last error: {error}")
        return None, f"JSON extraction failed: {error}"
    
    @staticmethod
    def _try_direct_parse(text: str) -> Tuple[Optional[Dict], str]:
        """Try parsing the entire text as JSON"""
        try:
            data = json.loads(text.strip())
            if isinstance(data, dict):
                return data, ""
        except json.JSONDecodeError as e:
            return None, f"Direct parse failed: {str(e)}"
        except Exception as e:
            return None, f"Direct parse error: {str(e)}"
        
        return None, "Parsed but not a dict"
    
    @staticmethod
    def _try_markdown_extraction(text: str) -> Tuple[Optional[Dict], str]:
        """Extract JSON from markdown code blocks"""
        # Pattern: ```json ... ```  or ```...```
        patterns = [
            r'```json\s*(\{.*?\})\s*```',
            r'```\s*(\{.*?\})\s*```',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            if matches:
                for match in matches:
                    try:
                        data = json.loads(match)
                        if isinstance(data, dict):
                            return data, ""
                    except:
                        continue
        
        return None, "No markdown JSON blocks found"
    
    @staticmethod
    def _try_pattern_extraction(text: str) -> Tuple[Optional[Dict], str]:
        """Find and extract JSON-like patterns"""
        # Find anything that looks like { ... }
        pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(pattern, text, re.DOTALL)
        
        for match in matches:
            try:
                data = json.loads(match)
                if isinstance(data, dict) and 'Value' in data:
                    return data, ""
            except:
                continue
        
        return None, "No JSON patterns found"
    
    @staticmethod
    def _try_fix_and_parse(text: str) -> Tuple[Optional[Dict], str]:
        """Try to fix common JSON issues"""
        # Clean up the text
        text = text.strip()
        
        # Find potential JSON content
        start = text.find('{')
        end = text.rfind('}')
        
        if start == -1 or end == -1 or end <= start:
            return None, "No JSON structure found"
        
        json_text = text[start:end+1]
        
        # Common fixes
        fixes = [
            # Fix 1: Replace single quotes with double quotes
            lambda t: t.replace("'", '"'),
            
            # Fix 2: Add missing quotes around keys
            lambda t: re.sub(r'(\{|,)\s*([A-Za-z_][A-Za-z0-9_]*)\s*:', r'\1"\2":', t),
            
            # Fix 3: Fix missing commas
            lambda t: re.sub(r'"\s*\n\s*"', '",\n"', t),
            
            # Fix 4: Remove trailing commas
            lambda t: re.sub(r',\s*}', '}', t),
            lambda t: re.sub(r',\s*\]', ']', t),
        ]
        
        # Try each fix
        for fix_func in fixes:
            try:
                fixed_text = fix_func(json_text)
                data = json.loads(fixed_text)
                if isinstance(data, dict):
                    return data, ""
            except:
                continue
        
        # Try applying all fixes together
        try:
            fixed_text = json_text
            for fix_func in fixes:
                fixed_text = fix_func(fixed_text)
            
            data = json.loads(fixed_text)
            if isinstance(data, dict):
                return data, ""
        except Exception as e:
            return None, f"All fixes failed: {str(e)}"
        
        return None, "Could not fix JSON"
    
    @staticmethod
    def validate_assessment(data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate that extracted JSON has required fields for assessment
        
        Args:
            data: Extracted dictionary
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = ['Value', 'Evidence']
        
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Validate Value field
        value = data['Value']
        valid_values = ['Met', 'Not Met', 'met', 'not met', 'MET', 'NOT MET']
        
        if value not in valid_values:
            # Try to normalize
            if value.lower() in ['yes', 'true', '1']:
                data['Value'] = 'Met'
            elif value.lower() in ['no', 'false', '0']:
                data['Value'] = 'Not Met'
            else:
                return False, f"Invalid Value: '{value}'. Must be 'Met' or 'Not Met'"
        
        # Normalize to standard case
        if value.lower() == 'met':
            data['Value'] = 'Met'
        elif value.lower() in ['not met', 'notmet']:
            data['Value'] = 'Not Met'
        
        # Validate Evidence field
        if not isinstance(data['Evidence'], str):
            return False, f"Evidence must be a string, got: {type(data['Evidence'])}"
        
        if len(data['Evidence'].strip()) == 0:
            return False, "Evidence cannot be empty"
        
        return True, ""


def extract_and_validate(response_text: str) -> Dict[str, Any]:
    """
    Extract and validate JSON from LLM response
    
    Args:
        response_text: Raw LLM response
    
    Returns:
        Dict with keys:
            - success: bool
            - data: Dict or None
            - error: str (if failed)
    """
    # Extract JSON
    extracted, error = JSONExtractor.extract(response_text)
    
    if not extracted:
        return {
            'success': False,
            'data': None,
            'error': error,
            'raw_response': response_text
        }
    
    # Validate
    is_valid, validation_error = JSONExtractor.validate_assessment(extracted)
    
    if not is_valid:
        return {
            'success': False,
            'data': extracted,
            'error': f"Validation failed: {validation_error}",
            'raw_response': response_text
        }
    
    return {
        'success': True,
        'data': extracted,
        'error': None,
        'raw_response': response_text
    }


if __name__ == "__main__":
    # Test the JSON extractor
    logging.basicConfig(level=logging.INFO)
    
    test_cases = [
        # Case 1: Clean JSON
        '{"Value": "Met", "Evidence": "The agent said hello"}',
        
        # Case 2: JSON in markdown
        '''```json
        {
            "Value": "Not Met",
            "Evidence": "No greeting found"
        }
        ```''',
        
        # Case 3: Single quotes
        "{'Value': 'Met', 'Evidence': 'Agent greeted customer'}",
        
        # Case 4: With extra text
        '''The assessment is as follows:
        {
            "Value": "Met",
            "Evidence": "Agent provided excellent service"
        }
        That's my analysis.''',
        
        # Case 5: Wrong value (should auto-fix)
        '{"Value": "Yes", "Evidence": "Found it"}',
    ]
    
    print("\n=== Testing JSON Extraction ===\n")
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}:")
        print(f"Input: {test[:60]}...")
        result = extract_and_validate(test)
        if result['success']:
            print(f"✅ Success: {result['data']}")
        else:
            print(f"❌ Failed: {result['error']}")
        print()

