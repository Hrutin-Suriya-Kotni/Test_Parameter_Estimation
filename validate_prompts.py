#!/usr/bin/env python3
"""
Validate prompts.py to ensure all fixes are correctly applied
"""

import re
from prompts import (
    PROMPT_OPENING,
    PROMPT_CLOSING,
    PROMPT_REASSURANCE,
    PROMPT_HOLD,
    PROMPT_FURTHER_ASSISTANCE
)

def check_for_issues(prompt_name, prompt_text):
    """Check a prompt for common issues"""
    issues = []
    
    # Check 1: Look for "Yes" or "No" in Value field (should be "Met" or "Not Met")
    if re.search(r'"Value":\s*"(Yes|No)"', prompt_text):
        issues.append("❌ Found 'Yes' or 'No' instead of 'Met'/'Not Met'")
    
    # Check 2: Look for single quotes in JSON examples
    json_blocks = re.findall(r'```json.*?```', prompt_text, re.DOTALL)
    for block in json_blocks:
        if "'" in block and '"Value"' not in block:
            issues.append("❌ Found single quotes in JSON example")
    
    # Check 3: Specific check for further assistance
    if prompt_name == "FURTHER_ASSISTANCE":
        if "putting a customer on hold" in prompt_text.lower():
            issues.append("❌ CRITICAL: Further assistance prompt still mentions 'hold'!")
        if "further assistance" not in prompt_text.lower():
            issues.append("❌ Further assistance prompt doesn't mention 'further assistance'")
    
    # Check 4: Look for missing commas in JSON
    if re.search(r'"Met"\s*\n\s*"Evidence"', prompt_text):
        issues.append("❌ Missing comma after 'Met' in JSON example")
    
    return issues

def main():
    print("🔍 Validating Prompts...")
    print("=" * 60)
    
    prompts = {
        "OPENING": PROMPT_OPENING,
        "CLOSING": PROMPT_CLOSING,
        "REASSURANCE": PROMPT_REASSURANCE,
        "HOLD": PROMPT_HOLD,
        "FURTHER_ASSISTANCE": PROMPT_FURTHER_ASSISTANCE
    }
    
    all_good = True
    
    for name, prompt in prompts.items():
        print(f"\n📋 Checking {name} prompt...")
        issues = check_for_issues(name, prompt)
        
        if issues:
            all_good = False
            for issue in issues:
                print(f"  {issue}")
        else:
            print(f"  ✅ No issues found!")
    
    print("\n" + "=" * 60)
    if all_good:
        print("✅ ALL PROMPTS VALIDATED SUCCESSFULLY!")
        print("\n🚀 Ready to proceed with stability testing!")
    else:
        print("❌ ISSUES FOUND - Please fix before testing!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

