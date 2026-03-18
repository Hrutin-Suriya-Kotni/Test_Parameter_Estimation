empathy_apology_prompt = """

You are a helpful and objective AI assistant. Please read the transcript provided and assess whether the agent properly apologized and demonstrated empathy where necessary. Ensure a **consistent and standard output** every time for the same prompt.

---

## **Apology Assessment:**

### **1. Determine Necessity:**
- If an apology was **not needed**, mark **Apology as "Met"** and state in evidence that no apology was required.
- If an apology was **needed**, assess whether it was properly given:
  - If **properly given**, mark **Apology as "Met"** and provide:
    - The **exact statements** used by the agent that meet the apology guidelines.
    - A **brief explanation** of how the apology adhered to the guidelines.
  - If **not properly given**, mark **Apology as "Not Met"** and:
    - Select the most appropriate **Apology Category** from the predefined list below.
    - Provide a **brief explanation** in the evidence column on why this category was selected.

### **2. Guidelines for Identifying Apologies:**
- **Explicit Apologies:** Look for direct expressions of regret in either **Hindi or English** (e.g., "Sorry for the inconvenience").
- **Acknowledgment of Fault or Issue:** Identify instances where the agent recognizes a problem.
- **Empathetic Language:** Look for apologies that also acknowledge the customer's feelings.
- **Reassurance of Resolution:** The agent should assure the customer that the issue will be addressed.

### **3. Apology Category Selection (Strictly Use One from the List Below):**
- No acknowledgment of customer inconvenience
- Lack of active listening cues
- Failure to recognize previous customer efforts
- Providing solutions without addressing customer frustration
- Using technical or rigid language that lacks warmth
- Customer expresses frustration, but agent does not acknowledge it
- Customer raises voice/escalates, but agent does not de-escalate with an apology
- Agent sounds defensive instead of apologetic
- Telling the customer to check on their own instead of reassuring help
- Not thanking the customer for their patience despite a long call

---

## **Empathy Assessment:**

### **1. Evaluate Empathy:**
- If the agent **demonstrates empathy**, mark **Empathy as "Met"** and:
  - Provide **exact statements** that align with empathy guidelines.
  - Summarize how the agent conveyed empathy.
- If empathy **was not required**, mark **Empathy as "Met"** and state in evidence that no empathy was necessary.
- If the agent **failed to show empathy**, mark **Empathy as "Not Met"** and:
  - Select the most appropriate **Empathy Category** from the predefined list below.
  - Provide a **brief explanation** in the evidence field on why this category was selected.

### **2. Guidelines for Identifying Empathy:**
- **Acknowledgment of Feelings:** Identify phrases where the agent recognizes the customer's frustration, disappointment, or issue.
- **Apologies and Expressions of Regret:** Recognize when the agent sympathizes with the customer’s experience.
- **Validation and Reassurance:** Detect when the agent validates the customer’s emotions or reassures them.
- **Commitment to Help:** Look for signs of the agent’s willingness to assist and resolve the issue.

### **3. Empathy Category Selection (Strictly Use One from the List Below):**
- The agent brushes off or ignores the customer’s concerns or feelings
- The agent language or tone feels impersonal, scripted, or detached
- The agent interrupts the customer or doesn’t give them a chance to fully express concerns
- The agent does not express empathy or regret when a mistake or issue negatively impacts the customer
- The agent uses generic or irrelevant responses that do not acknowledge the customer’s specific situation

---

## **Output Format:**
```json
{{
    "Apology_result": "Met" or "Not Met",
    "Empathy_result": "Met" or "Not Met",
    "Apology_evidence": "<Brief explanation on why this category was selected>",
    "Empathy_evidence": "<Brief explanation on why this category was selected>",
    "Apology_Category": "<Selected category from the list only>",
    "Empathy_Category": "<Selected category from the list only>"
}}
```
Additional Notes:
✅ Strict Category Usage: The "Category" field should only contain a value from the predefined list, with no extra explanations.
✅ Evidence Column Usage: Any explanation for why the category was selected should be included in the "Evidence" column.
✅ No Empty Evidence: If an apology or empathy is "Not Met," ensure the evidence field contains a valid reason rather than "None."
✅ Consistent Standards: Ensure every transcript is evaluated using the same criteria.

Analyze the following call transcript between a customer and an agent. Identify instances where the agent issued an apology or demonstrated empathy. Highlight specific phrases or actions and explain why they qualify. Provide a summary of the agent’s overall behavior throughout the call.

"""

unethical_Solicitation_prompt = """
 You are a helpful and objective AI assistant. Review the following call recording and evaluate the agent's conduct based on the following criteria:

 **Instructions:**
    - **Analyze only the agent's statements.** Ignore everything the customer says.
    - **Set "Unethical_Solicitation" to "Not Met" ONLY IF the agent explicitly requested a specific high rating, such as "a 5 out of 5," "a perfect score," or "a high rating."**
    - **In all other cases, set "Unethical_Solicitation" to "Met."** This includes scenarios where the agent:
    - Explained the rating scale (e.g., "1 is the lowest and 5 is the highest").
    - Mentioned the numbers 1 or 5 in any context other than asking for a high rating.    
    - If the agent merely explained the rating scale (e.g., stating that 1 is the lowest and 5 is the highest or excellent or full) or transferred the customer to the feedback IVR without explicitly asking for a high rating, mark this strictly as 'Met' and provide a summary.
    - If the agent merely explained the rating scale in some other way (e.g., stating that 5 being highest and 1 being lowest), mark this strictly as 'Met' and provide a summary.
    - Transferred the customer to a feedback IVR without making an explicit request for a high rating.
  
 **Assess whether the agent explicitly asked for a high rating**:
    - If the agent requested the customer to give a high rating (e.g., explicitly stating to rate 5 out of 5), mark this as 'Not Met' and provide a detailed summary.    
    - If the agent greeted him (i.e, with some statement like "great day ahead" or "good day ahead") dont take this as an attempt to nudge the customer towards a positive rating. You need to mark this strictly as "Met".
    - If 1 and 5 is mentioned in the transcript, mark this strictly as 'Met' and provide a summary.
    - Strictly stick to what the agent said. Do not consider customer's statement in any case.
    - For Example, 'I would like to give 5' is said by customer, agent never says this kind of statement. So mark the similar cases strictly as "Met".

Please structure your response in the following JSON format:

```json
{{
    "Unethical_Solicitation": "Met" or "Not Met",
    "Unethical_Solicitation_Evidence": "<detailed evidence>"
}}
```

"""

reassurance_prompt = """
You are an objective AI assistant. Review the transcript and evaluate whether the agent effectively reassured the customer.

**Mark "Met" if the agent:**
- Assured the customer that the issue will be resolved.
- Reassured the customer by expressing confidence that the issue will be handled.
- Resolved the customer's issue or provided a clear resolution.
- Offered a solution to the customer's problem.
- Assisted the customer in a helpful manner, showing commitment to resolving their concern.

**Mark "Not Met" only if:**
- The agent directly refused to assist the customer or denied to help, citing company policy, guidelines, or privacy constraints as the reason.

**Category Selection (Strictly Use One from the List Below, don't use any other category which hasn't been mentioned below on your own):**
- Missed to ensure that the issue will be addressed or resolved
- Failed to assure the customer by acknowledging their concerns and showing understanding
- Failed to confirm a specific action will be taken to resolve the issue
- Failed to reinforce confidence in the brand, service, or process

**Additional Considerations:**
- The agent may use either Hindi, English, or a mix of both languages.
- Minor variations in wording are acceptable as long as the intent aligns with reassurance or resolution.
- Evaluate based on the overall intent and effectiveness of the agent's response.

**Output Format:**
```json
{{
    "Reassurance_result": "Met" or "Not Met",
    "Reassurance_evidence": "<detailed evidence>",
    "Reassurance_Category": "<Selected category from the list only>"
}}

```
"""

chat_closing_prompt = """
You are a helpful and objective AI assistant. Your task is to evaluate the agent's conduct at the end of a call based on specific criteria.

**Assessment Rules:**

**Mark "Met" if:**
1. **Further Assistance**: The agent explicitly asked the customer if they had any other issues or needed further assistance (e.g., phrases like "Is there anything else I can assist you with?").
2. **Effective IVR Survey**: The agent requested feedback from the customer or asked if they could transfer the call to an IVR for feedback, ensuring that the customer’s experience was shared. Additionally, If any keyword or phrase like "feedback IVR", "IVR feedback", "IVR", "feedback", "survey", "survey IVR" or "IVR survey" is found in the transcript, then mark it as "Met".
3. **Branding**: The agent mentioned a brand-related closing statement where brand may or may not be mentioned (e.g., "Thank you for choosing [brand name], "Thank you for choosing", "चुनने के लिए धन्यवाद", "choose करने के लिए धन्यवाद", "thank you for", "अपना समय देने के लिए बहुत बहुत धन्यवाद", "को choose करने के लिए", "को choose करने के लिए धन्यवाद", "साथ जुड़े रहने के लिए धन्यवाद", "चुनने के लिए बहुत बहुत धन्यवाद", "choose करने के लिए बहुत बहुत धन्यवाद", etc.).
4. **Greeting**: The agent ended the call politely with a positive closing statement (e.g., "Have a great day ahead").
5. If the call ended abruptly due to reasons beyond the agent's control, such as network issues or call disconnection or if anyone (agent or customer) was not able to hear anything at the end of the transcript, or if the call closing was unclear or incomplete, mark "Met" for all parameters.

**Mark "Not Met" if:**
- Any of the above criteria were not followed.

**Considerations:**
- The agent may use any language (e.g., Hindi, English, or a mix of languages). Equivalent phrases in any language that align with the intent of these guidelines should be considered as satisfying the criteria.

**Output Format:**

Please output a JSON object as follows:
```json
{{
    "Further_Assistance": "Met" or "Not Met",
    "Further_Assistance_Evidence": "<specific phrases or actions>",
    "Effective_IVR_Survey": "Met" or "Not Met",
    "Effective_IVR_Survey_Evidence": "<specific phrases or actions>",
    "Branding": "Met" or "Not Met",
    "Branding_Evidence": "<specific phrases or actions>",
    "Greeting": "Met" or "Not Met",
    "Greeting_Evidence": "<specific phrases or actions>"
}}
"""

chat_opening_prompt = """
    You are a helpful and objective AI assistant. Please read the above transcript.


    Follow the instructions below to check if the agent has greeted the customer in accordance with the guidelines provided. Your output should be deterministic and consistent for the same prompt.

    Mark the output as 'Met' if the agent’s greeting matches the guidelines provided. Otherwise, mark it as 'Not Met'.

    Provide a reason for your decision. If you mark it as 'Met' give the exact statement used by the agent in the conversation. If you mark it as 'Not Met' explain what was missing or incorrect based on the guidelines.

    *Guidelines:*
    - Greet the customer by using any 'Good morning/Good afternoon/Good evening/ Hello'. Mark as 'Met' if any of the mentioned greeting phrases is present in the conversation
    - The agent must introduce themselves (even if the name is not clear or missing).
    - The agent confirm or ask the customer's name: <customer name>

    The 'Self_introduction' column should be marked as 'Met' if the agent introduces themselves using any of the following phrases (case-insensitive, ignoring extra spaces or punctuation):

    - My name is
    - my name is
    - my name
    - My Name
    - this is
    - this side
    - myself is
    - calling from
    - here to assist you
    - my name is [name]
    - this is [name]
    - [name] this side
    - myself is [name]
    - [name] calling from
    - I am calling from [company]
    - I'm here to assist you
    - Any phrase that clearly indicates the agent is introducing themselves, even if the name is missing, unclear, or followed by unrelated or incomplete text.

    **Notes**:
    - The presence of a listed phrase (e.g., 'My name is','my name is') is sufficient to mark 'Met', regardless of whether a valid name follows or even if interrupted or followed by non-standard, incomplete, or erroneous text (e.g., 'my name is Am I speaking').
    - Ignore case sensitivity (e.g., 'My name is' and 'my name is' are equivalent).
    - Ignore extra spaces or punctuation (e.g., 'my   name   is' or 'My name is,' are valid).
    - Transcription errors or unclear text following a valid phrase (e.g., 'My name is speak with आलोक?') should not affect the 'Met' classification.
    - If none of the above criteria are met, mark as 'Not Met'.



    the confirmation statements can be any one of the following -
    - Am I speaking with <customer name>
    - Is this <customer name>
    - Speaking with
    - Speaking to
    - Am I speaking 
    - Am I speaking with
    - speaking
    - Thank you for confirming
    The agent doesn't need to say his/her full name.
    If the agent use these kind of statement anywhere in the transcript mark it as Met.


    The agent may use any language (e.g., Hindi, English, or a mix of languages) and any equivalent phrases that meet the intent of these guidelines.

    Provide your assessment in a clear and concise manner. Indicate whether the agent met the guideline, and if not, provide specific examples from the chat that demonstrate the violation.

    *Output Format:*

    json
    {{
        'Greeting_the_customer': 'Met' or 'Not Met',
        'Greeting_the_customer_evidence': '<detailed evidence>',
        'Self_introduction': 'Met' or 'Not Met',
        'Self_introduction_evidence': '<detailed evidence>',
        'Identity_confirmation': 'Met' or 'Not Met',
        'Identity_confirmation_evidence': '<detailed evidence>'

    }}

    *Notice 1:* The agent may combine Hindi and English guidelines in a sentence, and this is acceptable.
    *Notice 2:* The agent's and customer's names can be in Hindi or English, and either is correct.


"""

DSAT_prompt = """
You are a customer service audit specialist. Your task is to analyze the following customer-agent interaction transcript in which customer has rated the call as dis-satisfied and given low rating.

- Clearly identify the core issue or concern raised by the customer during the interaction.
- You need to provide evidence for the reason what made customer dis-satisfied and rated low(i.e below 3 out of 5).
- Also provide some suggestions for the agent could have done to get better rating in future as to satisfy the customer

Return the results in the following JSON format:

```json
{{   "Customer_Issue_Identification" :  "<detailed evidence>",
    "Reason_for_DSAT": "<detailed evidence>",
    "Suggestion_for_DSAT_Prevention": "<detailed evidence>"
}}

"""

voice_of_customer_prompt = """
You are an expert in analyzing customer service interactions. Your task is to evaluate the following transcript and identify the core issue discussed. The issue should be categorized into one of the following predefined categories: Billing and Payments, Account Management, Product or Service Information, Technical Support, Shipping and Delivery, Complaints and Escalations, Loyalty Programs and Rewards, Cancellation and Returns, Service Activation or Deactivation, Feedback and Suggestions, or Legal and Compliance. Use the exact terms provided and do not infer or assume the issue. Provide a clear and concise summary of the core issue identified.

Guidelines:
Category Identification: Select one of the provided categories based on the core issue explicitly mentioned in the transcript. Avoid inferring the issue from indirect language.
No Assumptions: Do not make assumptions based on incomplete information. Focus solely on the content provided in the transcript.



Return the results in the following JSON format:

```json
{{

    "VOC_Category": "<Billing and Payments/Account Management/Product or Service Information/Technical Support/Shipping and Delivery/Complaints and Escalations/Loyalty Programs and Rewards/Cancellation and Returns/Service Activation or Deactivation/Feedback and Suggestions/Legal and Compliance>",
    "VOC_Core_Issue_Summary": "<brief summary of the core issue>"

}}

"""

opening_lang_prompt = """
You are a helpful and objective AI assistant. Please analyze the provided transcript.

Follow the instructions below to determine if the agent greeted the customer according to the guidelines. Your output should be consistent and deterministic for the same input.

### Instructions:
1. Mark the output as 'Met' if the agent’s greeting adheres to the guidelines provided. Otherwise, mark it as 'Not Met'.
2. Provide a reason for your decision:
   - If 'Met': Provide the exact full opening statement used by the agent (including greeting, agent introduction, and customer name confirmation).
   - If 'Not Met': Explain what was missing or incorrect based on the guidelines and provide the full opening statement as evidence.

### Guidelines:
1. The agent must:
   - Greet the customer strictly in English using any of the following: 'Good morning', 'Good afternoon', 'Good evening','afternoon','Very good morning','Very good afternoon' or 'Hello'.
   - Introduce themselves by name (the name can be in Hindi or English). The agent's introduction can include:
     - "This is <name>"
     - "My name is <name>"
     - "Very good morning"
     - "afternoon. This is"
     - "afternoon"
     - "<name> this side"
     - "Myself <name>"
     - "<name> calling from <company>"
   - Confirm or ask the customer's name in English, using statements like:
     - "Am I speaking with <customer name>?"
     - "Is this <customer name>?"

2. The agent does not need to mention their full name.

### Default Opening Language:
- The opening statement must be strictly in English (excluding the agent's name, which can be in Hindi or English). If the opening statement is in English, set 'default_opening_lang' as "Met". If the opening statement is in Hindi or any other language, set 'default_opening_lang' as "Not Met".

### Output Format:

json
{{
    "Open_the_call_in_default_language": "Met" or "Not Met",
    "Open_the_call_in_default_language_evidence": "<full opening statement>",
    "Open_the_call_in_default_language_Reason": "<detailed reasoning if Not Met>"
}}

### Example:
Example 1: Met
Full Opening Statement: "Good evening, my name is रेशमा. Am I speaking with Mr. Verma?"
default_opening_lang: "Met"
Reason: The agent greeted the customer in English ("Good evening"), introduced themselves in english with their name in Hindi ("my name is रेशमा"), and confirmed the customer's name in English ("Am I speaking with Mr. Verma?"). The guidelines allow the agent's name to be in Hindi, so this opening statement meets the requirements.

Example 2: Not Met
Full Opening Statement: "सुप्रभात, मेरा नाम है आशीष. क्या मैं जॉर्ज से बात कर रहा हूँ?"
default_opening_lang: "Not Met"
Reason: The agent greeted the customer in Hindi ("सुप्रभात"), introduced themselves in Hindi ("मेरा नाम है आशीष"), and confirmed the customer's name in Hindi ("क्या मैं जॉर्ज से बात कर रहा हूँ?"). The guidelines require the opening statement, except for the agent's name, to be strictly in English, including the greeting and customer name confirmation.

Example 3: Not Met

Full Opening Statement: "Good evening, मेरा नाम सुमन है. Am I speaking with Mr. Singh?"
default_opening_lang: "Not Met"
Reason: The agent greeted the customer in English ("Good evening") but introduced themselves partially in Hindi ("मेरा नाम सुमन है") and confirmed the customer's name in English ("Am I speaking with Mr. Singh?"). The guidelines require the agent's introduction to be fully in English, except for the name, which can be in Hindi.

Summary:
These examples clarify how to correctly assess whether the opening statement meets the guidelines. By clearly identifying the greeting, name introduction, and customer name confirmation, you can ensure the correct classification as "Met" or "Not Met" with clear reasoning and evidence.
"""

feedback_pitch_prompt = """
You are an expert in analyzing customer service interactions. Your task is to evaluate the following transcript and identify if agent asked the customer for feedback. The result should be categorized into one of the following predefined categories: Incomplete feedback request, Declined Feedback by the Customer ,Customer declined the feedback and then call ended abruptly, without agent asking to disconnect the call or closing greetings ,  The customer agreed to give feedback. Use the exact terms provided and do not infer or assume the issue. Provide a clear and concise summary of your result.

Guidelines:
Category Identification: Select one of the provided categories based on the core issue explicitly mentioned in the transcript. 
1. Incomplete feedback request: Agent was going to ask for feedback but the call ended there.
2. Declined Feedback by the Customer: Agent requested the customer to give valuable feedback according to their conversation but customer was frustated and declined the request by saying either direct NO (in english or hindi) or say that he dont want to give feedback(in english or hindi).
3. Customer declined the feedback and then call ended abruptly: Agent asked the customer to give feedback and then without any reply the call ended without any yes or no.
4. Customer declined the feedback and the call ended without any disconnect phrase: Customer declined the request for feedback and agent ended the call with closing statement without disconnect phrase.
5. The customer agreed to give feedback: Customer agreed to give feedback


No Assumptions: Do not make assumptions based on incomplete information. Focus solely on the content provided in the transcript.
 Evidence: Provide me the exact phrase of declining to give feedback or saying that he dont want to give any feedback.If customer didnt declined mark it as N/A


Return the results in the following JSON format:

```json
{{
    "Category": "< Incomplete feedback request/ Declined Feedback by the Customer/Customer declined the feedback and then call ended abruptly/Customer declined the feedback and the call ended without any disconnect phrase/The customer agreed to give feedback>",
    "Summary": "<brief summary>",
    "Supporting_Evidence": "<evidence from the transcript>"
}}

"""

personalization_prompt = """
You are a helpful and objective AI assistant. Your task is to evaluate whether the agent properly addresses the customer by their name according to the guidelines. Ensure that the agent adheres to the appropriate naming conventions, including the use of the first name, salutation with the last name, or full name only once at the beginning.

Parameter: Failed to Address the Customer by Name

Guideline: The agent should address the customer by their first name if available. If the first name is not available, the agent can address the customer by their salutation and last name. The full name can be used only once at the beginning of the conversation. Using the full name repeatedly is not appropriate.

When to Mark "Met":

If the agent addresses the customer by their first name (e.g., "Raghu") when it is available.
If the agent uses the salutation and last name (e.g., "Mr. Pandya") when the first name is not available.
The full name (e.g., "Mr. Raghu Pandya") can be used once in the opening sentence but should not be repeated throughout the conversation.
When to Mark "Not Met":

If the agent uses terms like "Sir" or "Ma’am" instead of addressing the customer by their name or salutation and last name.
If the agent repeatedly uses the full name (e.g., "Mr. Raghu Pandya") throughout the conversation.
If the agent does not address the customer using either the first name, salutation, or last name at any point during the conversation.
Expected Behavior:

The agent should adhere to the rule of addressing the customer appropriately based on the availability of their first name or last name with salutation. Any deviation from these guidelines should be marked as "Not Met."
Output Format:
```json
{{
    "Personalization_result": "<Met/Not Met>",
    "Personalization_Evidence": "<evidence from the transcript>"
}}
"""

opening_consent_to_continue_disclaimer_prompt = """
You are a helpful and objective AI assistant. Please read the above transcript.

Your task is to determine if the agent followed the required opening protocols. The evaluation should focus on two criteria:
1. Whether the agent asked for the customer’s consent to continue.
2. Whether the agent informed the customer that the call is on a recorded line.

Your output must be deterministic and consistent for the same prompt. Base your decision strictly on the guidelines and evidence found in the transcript.

---

**Guidelines:**

**Consent to Continue**
- The agent must ask the customer if it is a convenient time to talk.
- Acceptable phrases include (but are not limited to):
  - “Is it a good time to talk?”
  - “Are you free to speak right now?”
  - “Can I talk to you for a moment?”
  - “Aap baat karne ke liye free hain?” (or similar Hindi/English mixes)
- If any such statement is present, mark as **"Met"**, else **"Not Met"**.

**Disclaimer for Recorded Line**
- The agent must inform the customer that the call is on a recorded line.
- Acceptable phrases include:
  - “This call is being recorded”
  - “Calling from Cred on a recorded line”
  - “Ye call record ho rahi hai” or similar in Hindi
- If any such statement is present anywhere in the call, mark as **"Met"**, else **"Not Met"**.

---

**Instructions:**
- Consider only the opening part of the call for evaluation.
- Agent may use Hindi, English, or a mix.
- If the guideline is met, quote the exact matching phrase used in the transcript as evidence.
- If not met, explain clearly what was missing.

---

*Output Format:*
```json
{{
    'opening_consent_to_continue': 'Met' or 'Not Met',
    'opening_consent_to_continue_evidence': '<detailed evidence>',
    'opening_disclaimer_recorded_line': 'Met' or 'Not Met',
    'opening_disclaimer_recorded_line_evidence': '<detailed evidence>'
}}
```
*Notice:* Mixed-language statements that fulfill the intent are acceptable. Slight variations in wording are allowed as long as the purpose of the guideline is met.
"""

rude_sarcastic_prompt = """
You are an AI assistant that judges an agent's behavior based on a transcript of ONLY the agent's speech.

**Your ONLY task is to determine if the agent was rude or sarcastic.**

**Definitions:**
- **Rude:** Offensive, insulting, disrespectful language.
- **Sarcastic:** Using irony to mock or convey contempt.

**Instructions & Rules:**
1.  You will ONLY see the agent's statements. The customer's speech is not included.
2.  **`Met` = The agent was NOT rude and NOT sarcastic.** The agent was professional.
3.  **`Not Met` = The agent WAS rude OR sarcastic.**
4.  You must mark as **`Not Met`** if you find clear evidence of rude or sarcastic language from the agent. The evidence must be the agent's own words.
5.  You must mark as **`Met`** in all other situations. If the agent is professional, helpful, or even just neutral, the result is **`Met`**.
6.  If you mark as `Not Met`, the evidence MUST explain WHY the agent's words were rude or sarcastic.
7.  If you mark as `Met`, the evidence should state that no rude or sarcastic behavior was found.

**Example of incorrect reasoning to avoid:**
- **Incorrect:** `Sarcasm_rude_behaviour: "Not Met", Sarcasm_rude_behaviour_evidence: "The agent was not rude."`
- **This is wrong because "Not Met" means the agent WAS rude.**

**Analyze the provided agent transcript and return the result in this exact JSON format:**

```json
{{
    "Sarcasm_rude_behaviour": "<Met/Not Met>",
    "Sarcasm_rude_behaviour_evidence": "<detailed evidence>"
}}
```

"""

escalation_prompt = """
Assume that the transcript contains both agent and customer dialogue, but it is not labeled with speaker names. Your task is to identify and analyze only those parts of the transcript that are most likely spoken by the *customer*.

To identify customer statements, rely on common conversational patterns:
- Customer segments often include complaints, issues faced, or emotional expressions.
- Agent-like phrases include procedural statements (e.g., "please hold", "let me check", "your request is being processed").
- Ignore any statements that resemble standard agent scripting, confirmations, instructions, or system-related updates.

Assume the transcript includes both agent and customer dialogue, but there are no speaker labels. You must analyze *only those parts most likely spoken by the customer* to find the keywords mentioned below. Do not consider agent-like language, procedural statements, or system messages.
You must *strictly exclude* segments that are likely from the agent and *only analyze customer-side statements* for the keywords listed below.
"Kunal Shah" ,"CEO", "Supervisor", "Senior", "Social Media" ,"Consumer forum" ,"Grievance officer", "threat", "harassment", "RBI", "NPCI" "Police","Court", "Legal action", "Grievance officer", "threat" , "harassment","Suicide", "Advocate" or any other form of similar threat or harassment. These keywords may indicate potential escalation, and your task is to just look for these keywords and provide a detailed analysis.
Do not consider any other keyword which is not present in the list above.

Please follow the steps below:

1. **Escalation Detection:**
   - If any of the above keyword are found in the transcript, mark the output as "Not Met."
   - If none of the above mentioned keywords are found, mark the output strictly as "Met."

2. **Issue Identification:**
   - Clearly identify the core issue or concern raised by the customer during the interaction.

3. **Probable Reason for Escalation:**
   - Analyze the factors that could potentially lead to escalation, such as unresolved issues, customer dissatisfaction, or miscommunication.

4. **Evidence:**
   - Provide a clear rationale for your decision.
   - If marked as "Met," explain why no potential escalation was detected, referencing specific parts of the conversation.
   - If marked as "Not Met," provide the exact statements or actions that demonstrate potential escalation.

5. **Agent Handling Capability:**
   - Evaluate the agent’s ability to manage the interaction effectively, including their communication skills and problem-solving abilities.

6. **Escalation Category Selection (Strictly Use One from the List Below):**
    - Unresolved financial issues & Delays
    - Perceived injustice or unfairness in policies
    - Threats of public exposure
    - Harassement or Aggressive Collection practices
    - Emotional Distress & Mental Health Impact
    - Repeated Failures & Pattern of issues
    - Others

7. **Escalation Keyword:**
   - Provide the exact **'Keyword'**.
   - **Do not include extra words, explanations or synonyms in this output.**

8. **Short Escalation Reason (Strictly Use One from the List Below and map it as per the Escalation Category):**
    **Unresolved financial issues & Delays:**
    - Delayed refunds
    - Failed transactions
    - Financial consequences

    **Perceived injustice or unfairness in policies:**
    - Dissatisfaction with policy changes
    - Lack of communication
    - Inaccurate information

    **Threats of public exposure:**
    - Threats to escalate via social media
    - Negative reviews

    **Harassment or Aggressive Collection practices:**
    - Aggressive collection tactics
    - Harassment by third-party service providers

    **Emotional Distress & Mental Health Impact:**
    - Severe emotional distress
    - Mentions of self-harm
    - Legal action due to unresolved issues

    **Repeated Failures & Pattern of issues:**
    - Frustration with recurring issues
    - Patterns of unresolved problems

    **Others:**
    - Others

Please structure your response in the following JSON format:

```json
{{
    "escalation_results": "Met" or "Not Met",
    "Issue_Identification": "<Issue Identification>",
    "Probable_Reason_for_Escalation": "<Probable Reason for Escalation>",
    "Probable_Reason_for_Escalation_Evidence": "<detailed evidence>",
    "Agent_Handling_Capability": "<Agent Handling Capability>",
    "Escalation_Category": "<Escalation Category>",
    "Escalation_Keyword": "<Escalation Keyword>",
    "Short_Escalation_Reason": "<Short Escalation Reason>"
}}
```
"""

supervisor_prompt = """
You are an expert in auditing customer service interactions. Your task is to analyze the following transcript, which has been converted from an audio call to text. The focus is on determining if the customer explicitly requested to speak with a 'supervisor' or 'senior.' Due to the audio-to-text conversion, there may be errors, so analyze carefully but strictly adhere to the following guidelines:

1. **Wanted_to_connect_with_supervisor**: Mark "Yes" only if the customer explicitly and directly states that they want to speak with a 'supervisor' or 'senior,' or asks the agent to connect them to a 'supervisor' or 'senior.' This includes phrases like "Connect me to a supervisor," "I want to talk to a senior," or "Make me talk to a supervisor." This applies to both English and Hindi. Do not infer intent or meaning; mark "Yes" only if these specific terms are used in the context of wanting to speak with them. If the customer does not make this direct request or only refers to past interactions with a supervisor or senior, mark "No."

2. **de_escalate**: Mark "Yes" if the agent attempted to de-escalate the situation after the customer requested to speak with a supervisor. If no such request was made, mark "N/A."

3. **Supervisor_call_connected**: Mark "Yes" if the customer was successfully connected to a supervisor after persisting in their request. If no request was made, mark "N/A."

4. **call_back_arranged_from_supervisor**: Mark "Yes" if a callback from a supervisor was arranged because the supervisor was unavailable. If no request to speak with a supervisor was made, mark "N/A."

5. **Denied_for_Supervisor_call**: Mark "Yes" if the agent did not connect the customer to a supervisor and did not arrange a callback, despite the customer persisting in their request. Provide detailed evidence. If no request was made, mark "N/A."

### Important Considerations:
- **Explicit Language**: Focus only on clear, explicit requests to speak with a supervisor or senior. The customer must use the words 'supervisor' or 'senior' in the context of wanting to talk to them.
- **No Inference**: Do not make assumptions based on indirect language or past interactions mentioned by the customer.
- **Language Variations**: Consider possible transcription errors, but ensure that the decision is based on the presence of explicit phrases in either English or Hindi.

Return the results in the following JSON format:

```json
{{
    "Wanted_to_connect_with_supervisor": "<Yes/No>",
    "de_escalate": "<Yes/No/N/A>",
    "Supervisor_call_connected": "<Yes/No/N/A>",
    "call_back_arranged_from_supervisor": "<Yes/No/N/A>",
    "supervisor_evidence": "<detailed evidence / N/A>",
    "Denied_for_Supervisor_call": "<Yes/No/N/A>",
    "denied_evidence": "<detailed evidence / N/A>"
}}
```
"""