# Assessment prompts and guidelines for CRED conversation analysis

# Base instructions and guidelines
LLM_INSTRUCTIONS = """
    You are a helpful and objective AI assistant. Please read the above transcript.
    Follow the instructions below to check if the agent has followed the provided guidelines during the conversation.
    Your output should be deterministic and consistent for the same prompt.
    Mark the output as 'Met' if the agent's greeting matches the guidelines provided. Otherwise, mark it as 'Not Met'.
    Provide a reason for your decision.
    If you mark it as 'Met' give the exact statement used by the agent in the conversation.
    If you mark it as 'Not Met' explain what was missing or incorrect based on the guidelines.
"""

ASSESSMENT_GUIDELINES = """
    - The agent can switch between English and Hindi or use a mix of languages.
    - Minor variations in phrasing are acceptable as long as the intent matches the guideline.
    - Evaluate based on intent and not strict wording.
"""

OUTPUT_FORMAT_GUIDELINES = """
  Provide your assessment in a clear and concise manner. Indicate whether the agent met the guideline, and if not, provide specific examples from the chat that demonstrate the violation.
  
  **CRITICAL: You must respond with ONLY a valid JSON object. No additional text before or after.**
  
  **Output Format:**
  ```json
  {
      "Value": "Met" or "Not Met",
      "Evidence": "<detailed evidence>"
  }
  ```
  
  **Important Notes:**
  - Use "Met" when the guideline is followed
  - Use "Not Met" when the guideline is NOT followed (never use "No")
  - Keep evidence concise but specific
  - Ensure valid JSON syntax with double quotes
"""

# Specific guidelines for each assessment type
OPENING_GUIDELINES = """
 - Greet the customer by using any 'Good morning/afternoon/evening/ Hello'
    - The agent must introduce themselves with their name: <name>
    - The agent confirm or ask the customer's name: <customer name>
    Agent can introduce themselves as follwings -
    - this is <name>
    - my name is <name>
    - <name> this side
    - myself is <name>
    - <name> calling from
    the confirmation statements can be any one of the following -
    - Am I speaking with <customer name>
    - Is this <customer name>
    The agent doesn't need to say his/her full name.
    If the agent use these kind of statement anywhere in the trancript mark it as Met.
"""

CLOSING_GUIDELINES = """
  - check if the agent ask the client for further help
  - ask to share the feedback for the conversation
  - ask the customer to transferring the call for the feedback.
  - close the chat with the proper greetings similar to the statement - 'I hope you have a great day ahead'
  - if the customer did not end the call ask him to cut the call politely.
  - if the customer becomes abusive on the call, agent can say similar statment :
    - I understand that you're frustrated, but I need to let you know that I can only continue this conversation if it remains respectful.
  - if the customer continues for abuse -  I am sorry, however, I am forced to disconnect the call. Feel free to reach out again when you're ready to discuss your concerns respectfully.
"""

HOLD_GUIDELINES = """
    The agent can use the following statements or similar statements while putting a call on hold -
    - "May I place your call on hold for 2 min?"
    - "Thank you for being on hold Sir/ Mam."
    - "May I place this call on hold <> minutes to check the information for you."
    - "To check the information for you may I place this call on hold for <> minutes."
    - "Kya mein aapki call ko <> Hold pe rak saktha / Sakti hoon information check karne ke liye?"
    - "Aapki jaankari check karne ke liye kya mein aapka/aapki call <> minute hold pe rak saktha sakti hoon sir/madam?"
    - "sir/madam ek minute hold kijeye"
"""

ASSISTANCE_GUIDELINES = """
    The agent can use the following statements or similar statements to find if the customer needs further assistance -
    - Iske alawa koi aur sahayata meri taraf se/ Iske alawa koi aur jankari
    - Is there anything else apart from this I may assist you with
"""

REASSURANCE_GUIDELINES = """
    The agent can assured the customer by providing statements similar to the below statements -
    - You can rest assured that we are working on this right now.
    - I will get back to you as soon as possible
    - I assure you, we will handle this matter promptly.
    - We are committed to resolving this for you as quickly as possible.
    - I will personally ensure that this issue is taken care of.
    - We have already started looking into this and will update you shortly.
    - Our support team is here for you, and we will see this through to the end.
    - I have all the necessary information and will make sure this gets fixed.
    - We take this matter seriously and will address it immediately.
    - We are here to help and will make sure this is resolved for you.
    - We appreciate your patience and will resolve this as quickly as possible.
    - I will keep you updated on the progress and next steps.
"""

# Complete prompts for each assessment type
PROMPT_OPENING = f"""
    **Assessment Instructions**
    {LLM_INSTRUCTIONS}
    **Guidelines:**
    {OPENING_GUIDELINES}
    **Output formatting considerations**
    {OUTPUT_FORMAT_GUIDELINES}
    **Assessment Criteria:**
    {ASSESSMENT_GUIDELINES}
    **Examples:**
    - If the agent said "विजय calling from Cred" and "Am I speaking with गोविंद?", the output should be:
    json
    {{
        "Value": "Yes",
        "Evidence": "The agent introduced themselves as 'विजय calling from Cred' and confirmed the customer's name with 'Am I speaking with गोविंद?'"
    }}
    - If the agent said "Hello, this is from Cred" without a name, and "Is this गोविंद?", the output should be:
    json
    {{
        "Value": "Not Met",
        "Evidence": "The agent did not provide their name and only confirmed the customer's name with 'Is this गोविंद?'."
    }}
    **Notice 1:** The agent may combine Hindi and English guidelines in a sentence, and this is acceptable.
    **Notice 2:** The agent's and customer's names can be in Hindi or English, and either is correct.
"""

PROMPT_CLOSING = f"""
    **Assessment Instructions**
    {LLM_INSTRUCTIONS}
    **Guidelines:**
    {CLOSING_GUIDELINES}
    **Output formatting considerations**
    {OUTPUT_FORMAT_GUIDELINES}
    **Assessment Criteria:**
    {ASSESSMENT_GUIDELINES}
    - All the cases where the agent had no opportunity to close the call, that is customer cut the call before agent's statement Mark it as "MET" instead of "NOT MET"
    - If the customer is ending the call abruptly, mark is as 'MET'.
    - If the customer cut the call before the agent had a chance to ask for feedback or closing statement, mark it as 'MET'.
    - It is mandatory for the agent to ask the customer for transferring the call for feedback. If he is suggesting the customer for feedback or directly transferring for feedback then mark the closing parameter as "Not Met"
    **Examples:**
    - If the agent said "Is there anything else I can help you with?" and "Great! Before we end this call, may I request you to share your valuable feedback basis our conversation?," the output should be:
    ```json
    {{
        'Value': 'Met'
        'Evidence': 'The agent asked if there was anything else they could help with and requested feedback before ending the call.'
    }}
    ```
    - If the agent did not ask for feedback but did ask if there was anything else to help with, the output should be:
    ```json
    {{
        'Value': 'Not Met',
        'Evidence': 'The agent asked if there was anything else to help with but did not request feedback before ending the call.'
    }}
    ```
    **Notice 1:** The agent may combine Hindi and English in a sentence, which is acceptable.
    **Notice 2:** Ensure leniency in evaluating the phrasing as long as the guideline's intent is met.
"""

PROMPT_REASSURANCE = f"""
    **Assessment Instructions**
    {LLM_INSTRUCTIONS}
    **Guidelines:**
    {REASSURANCE_GUIDELINES}
    **Output formatting considerations**
    {OUTPUT_FORMAT_GUIDELINES}
    **Assessment Criteria:**
    {ASSESSMENT_GUIDELINES}
    - An agent should be able to create a sense and atmosphere where the customer feels assured.
    **Output Format:**
    ```json
    {{
        'Value': 'Met' or 'Not Met',
        'Evidence': <detailed evidence>
    }}
    ```
    **Notice 1:** The agent may combine Hindi and English in a sentence, which is acceptable.
    **Notice 2:** Ensure leniency in evaluating the phrasing as long as the guideline's intent is met.
"""

PROMPT_HOLD = f"""
    **Assessment Instructions**
    {LLM_INSTRUCTIONS}
    You need to identify if the agent has used any of these or similar statements anywhere in the conversation for putting a customer on hold
    **Guidelines:**
    {HOLD_GUIDELINES}
    **Output formatting considerations**
    {OUTPUT_FORMAT_GUIDELINES}
    **Assessment Criteria:**
    {ASSESSMENT_GUIDELINES}
    **Notice 1:** The agent may combine Hindi and English in a sentence, which is acceptable.
    **Notice 2:** Ensure leniency in evaluating the phrasing as long as the guideline's intent is met.
"""

PROMPT_FURTHER_ASSISTANCE = f"""
    **Assessment Instructions**
    {LLM_INSTRUCTIONS}
    You need to identify if the agent has used any of these or similar statements anywhere in the conversation for putting a customer on hold
    **Guidelines:**
    {ASSISTANCE_GUIDELINES}
    **Output formatting considerations**
    {OUTPUT_FORMAT_GUIDELINES}
    **Assessment Criteria:**
    {ASSESSMENT_GUIDELINES}
    **Notice 1:** The agent may combine Hindi and English in a sentence, which is acceptable.
    **Notice 2:** Ensure leniency in evaluating the phrasing as long as the guideline's intent is met.
"""

# Dictionary of all prompts for easy access
ASSESSMENT_PROMPTS = {
    'opening': PROMPT_OPENING,
    'closing': PROMPT_CLOSING,
    'reassurance': PROMPT_REASSURANCE,
    'hold': PROMPT_HOLD,
    'further_assistance': PROMPT_FURTHER_ASSISTANCE
} 