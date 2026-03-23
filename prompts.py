# Assessment prompts for CRED conversation analysis

apology_prompt = """
    You are a QA evaluator analyzing customer service call transcripts. Your job: decide whether the agent **provided an adequate apology** to the customer when needed.

    **CRITICAL EVALUATION RULE:**
    You must evaluate EVERY step sequentially. For each step:
    1. State the step number
    2. Quote the specific agent statement(s) that address this step
    3. Explicitly write "YES" or "NO" for whether the criterion is met
    4. Only proceed to the next step if the current step is "NO"

    If ANY step shows an apology was given OR wasn't needed, immediately mark Apology_result as "Met" with evidence.

    STRICTLY Follow these steps in order:

    0. **Check if apology is required at all:**
        - If the call was too short to determine, mark as "Met" (Evidence: "Call too short to evaluate").
        - If there was no response from the customer, mark as "Met" (Evidence: "No customer response").
        - If the right person is not on the call (e.g., wrong number, someone else picked up), mark as "Met" (Evidence: "Wrong party on call").
        - If the customer had no issue, complaint, frustration, or problem, mark as "Met" (Evidence: "No apology required").
        - If the call was incomplete, cut off, or abruptly ended, mark as "Met" (Evidence: "Incomplete call").
        - Otherwise, proceed to the next step.

    1. **Did the customer express a problem, complaint, frustration, or dissatisfaction?**
        This includes: complaining about service, expressing frustration, reporting an issue/error, mentioning inconvenience, stating dissatisfaction.
        - If NO → Mark "Apology_result" as "Met" (Evidence: "No apology required - customer had no complaint or issue").
        - If YES → Proceed to step 2.

    2. **Did the agent use any apology words or phrases?**
        Search for these words in English or Hindi:
        - English: sorry, apologize, apologies, regret, apologetic
        - Hindi: माफ़ी, माफ, क्षमा, खेद, sorry (in Hindi script)
        - Phrases: "I apologize", "I'm sorry", "we're sorry", "my apologies", "I regret"

        - If YES → Mark "Apology_result" as "Met" with evidence: [Quote the exact apology statement]
        - If NO → Proceed to step 3.

    3. **Mark "Apology_result" as "Not Met".**
        Before marking 'Not Met', review steps 0-2 again and verify:
        - The customer DID have a problem/complaint (Step 1 = YES)
        - The agent DID NOT use any apology words (Step 2 = NO)

        Provide evidence: "Agent did not apologize for [specific customer issue/complaint]"

        **Select ONE category that best describes why the apology was missing:**
        1. "No acknowledgment of customer inconvenience"
        2. "Customer expresses frustration, but agent does not acknowledge it"
        3. "Agent sounds defensive instead of apologetic"
        4. "Providing solutions without addressing customer frustration"
        5. "Using technical or rigid language that lacks warmth"

    **IMPORTANT CLARIFICATIONS:**

    1. **Quality doesn't matter**: If the agent said "sorry" even once, mark as "Met" - regardless of how sincere, detailed, or appropriate it was. You are checking PRESENCE, not QUALITY.

    2. **Timing doesn't matter**: An apology at any point in the call (beginning, middle, or end) counts as "Met".

    3. **Customer satisfaction ≠ Apology evaluation**: Even if the customer remains unhappy after an apology, the apology still counts as given. Focus ONLY on whether apology words were used, not whether the customer accepted it.

    4. **Long transcripts**: For lengthy conversations, you MUST still search the entire transcript for apology words. Do not skip analysis due to transcript length.

    5. **Multiple apologies**: If the agent apologizes multiple times, this still counts as "Met" (mention this in evidence if relevant).

    6. **Evidence requirement**: Your evidence statement must:
    - For "Met": Include the exact quote with apology words, OR state "No apology required - [reason]"
    - For "Not Met": Specify what the customer complained about that warranted an apology
    - NEVER write vague statements like "no apology found" without context

    **INVALID EVIDENCE EXAMPLES (Never do this):**
    - "Agent did not apologize"
    - "No apology detected"
    - "Apology missing"

    **VALID EVIDENCE EXAMPLES:**
    - "I really apologize that you are facing this inconvenience"
    - "No apology required - customer had no complaint or issue"
    - "Agent did not apologize for the delayed refund despite customer expressing frustration multiple times"

    ## OUTPUT FORMAT
    Return your analysis in this exact JSON structure:
    ```json
    {
        "Apology_result": "Met or Not Met",
        "Apology_evidence": "exact quote OR detailed reason",
        "Apology_Category": "leave empty string '' if Met, otherwise select one category from the list above"
    }
    ```

    **CRITICAL RULES:**
    1. If Step 0 or Step 1 results in "No apology required" → Apology_result MUST be "Met"
    2. If Step 2 finds apology words → Apology_result MUST be "Met"
    3. Only mark "Not Met" if customer had a problem AND agent didn't use apology words
    4. Category must be empty string "" when result is "Met"
    5. Never contradict yourself (e.g., "Not Met" with "No apology required")

    ---

    Now analyze this call transcript:
    """

empathy_prompt = """
    Analyze the call transcript and check if the agent showed empathy towards the customer.

    ### Step-by-step evaluation:

    **Step 1: Look for empathy phrases**
    - "I understand your concern"
    - "I can imagine how frustrating this is"
    - "I know this has been difficult"
    - "You're right to be upset"
    - "This must be frustrating"
    - Any sentence where agent recognizes customer's feelings

    **Step 2: Check if customer was upset**
    Did the customer express frustration, anger, or disappointment?

    **Step 3: Make decision**
    - **If empathy phrases found** → Result = "Met" (Evidence: copy exact empathy sentence)
    - **If NO empathy phrases found:**
    - **AND customer was upset** → Result = "Not Met" (Evidence: "Agent did not acknowledge customer's frustration about [issue]")
    - **AND customer was calm** → Result = "Met" (Evidence: "No empathy required")

    ---

    ## CRITICAL RULES - READ CAREFULLY

    1. You are NOT allowed to use the word "acknowledge" in the evidence.
    2. **"No empathy required" = Result MUST be "Met"** (not "Not Met")
    4. **Don't judge quality** - focus only on presence/absence
    5. **Evidence must match result:**
    - "Met" + "No empathy required" ✓ CORRECT
    - "Not Met" + "No empathy required" ✗ WRONG
    6. Provide specific evidence from the conversation supporting your assessment.
        REQUIRED FORMAT:
        - If Empathy_result='Met': Empathy_evidence should start with 'Agent showed empathy for <customer's issue>' or 'No empathy required'. Followed by specific examples of empathetic language or actions.
        - If Empathy_result='Not Met': Empathy_evidence should start with 'Agent did not showed any empathy for <customer's issue>'. Followed by explanation of what empathy was lacking. "
        Replace <customer's issue> with the actual issue (e.g., 'billing dispute', 'service outage', 'frustration with wait time').

    ---

    Now analyze this call transcript:"""

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
    {
        "Unethical_Solicitation": "Met" or "Not Met",
        "Unethical_Solicitation_Evidence": "<detailed evidence>"
    }
    ```

    """

reassurance_prompt = """
    You are a QA evaluator analyzing customer service call transcripts. Your job: decide whether the agent **provided adequate reassurance** to the customer.

    **CRITICAL EVALUATION RULE:**
    You must evaluate EVERY step sequentially. For each step:
    1. State the step number
    2. Quote the specific agent statement(s) that address this step
    3. Explicitly write "YES" or "NO" for whether the criterion is met
    4. Only proceed to the next step if the current step is "NO"

    If ANY step from 2-7 is marked "YES", immediately mark Reassurance_result as "Met" with evidence.

    STRICTLY Follow these steps in order:
    0. If the call was too short to determine, mark as "Met" (Evidence: "Call too short to evaluate").
        - If there was no response from the customer, mark as "Met" (Evidence: "No customer response").
        - If the right person is not on the call (e.g., wrong number, someone else picked up), mark as "Met" (Evidence: "Wrong party on call").
        - If the customer had no issue, the call was smooth, or the issue was already resolved, mark as "Met" (Evidence: "No reassurance required").
        - If the call was incomplete, cut off, or abruptly ended, mark as "Met" (Evidence: "Incomplete call").
        - Otherwise, proceed to the next step.
    1. Did the customer express a problem or concern?
        - If NO → Mark "Reassurance_result" as "Met" (Evidence: "No reassurance needed").
        - If YES → Proceed to step 2.
    2. Did the agent acknowledge the customer's concern and show understanding?
        "Acknowledgment includes: asking clarifying questions, putting the call on hold to investigate, or saying they will check the issue."
    - If YES → Mark "Reassurance_result" as "Met". (Evidence: [Quote the exact acknowledgment statement])
    - If NO → Proceed to step 3.
    3. Did the agent use any reassurance phrases (e.g., "don't worry", "be assured", "I will help you")?
        - If YES → Mark "Reassurance_result" as "Met". (Evidence: [Quote the exact reassurance statement])
        - If NO → Proceed to step 4.
    4. Was the customer's issue beyond the agent's control (e.g., policy restrictions)?
        - If YES → Mark "Reassurance_result" as "Met". (Evidence: [Quote agent's explanation])
        - If NO → Proceed to step 5.
    5. Did the agent try anything to resolve the customer's issue or provide a solution or guide the customer so that he could resolve the issue himself (even if it was not successful)?
    **This includes:** offering to guide through steps, providing instructions, offering alternative solutions, troubleshooting, asking diagnostic questions to help resolve the issue.
        - If YES → Mark "Reassurance_result" as "Met" with evidence: [Quote agent's attempt]
        - If NO → Proceed to step 6.
    6. If the agent was not able to help, did he explained why he couldn't help (e.g., company policy, guidelines, privacy constraints)?
        - If YES → Mark "Reassurance_result" as "Met". (Evidence: [Quote agent's explanation])
        - If NO → Proceed to step 7.
    7. If the agent was not able to help himself, did he offer to escalate or follow up later or directed to the merchant or another department or insurer, etc ?
        "Directing to appropriate parties (merchant, insurer, another department) counts as offering a resolution path."
        - If YES → Mark "Reassurance_result" as "Met". (Evidence: [Quote the exact escalation or follow-up offer])
        - If NO → Proceed to step 8.
    8. Mark "Reassurance_result" as "Not Met".
        "Before marking 'Not Met', review ALL steps again and verify that NONE of the criteria were satisfied. List which step number applies and quote the exact agent statement as evidence."
        Provide evidence: "Agent did not provide reassurance for [quote the exact customer problem or concern]"

    **IMPORTANT CLARIFICATIONS:**

    1. **Customer satisfaction ≠ Reassurance evaluation**: Even if the customer remains unhappy or frustrated throughout the call, the agent can still provide adequate reassurance. Focus ONLY on the agent's actions, not the customer's emotional state or satisfaction level.

    2. **Long transcripts**: For lengthy conversations, you MUST still evaluate each step carefully. Do not skip analysis due to transcript length.

    3. **Multiple reassurance instances**: If the agent uses reassurance phrases like "do not worry", "I will help you", "I understand" multiple times throughout the call, this STRENGTHENS the "Met" determination, not weakens it.

    4. **Evidence requirement**: Your evidence statement must include:
    - The step number where reassurance was met
    - At least ONE direct quote from the agent
    - NEVER write vague statements like "did not provide reassurance" - you must cite specific transcript content

    Note:
    - Focus only on whether reassurance was provided, not on the outcome of the call.
    - Qualify your answers with specific evidence from the transcript.
    - Quality of reassurance does not matter; only presence or absence counts.

    Now analyze this call transcript:
    """

chat_closing_prompt = """
    You are a helpful and objective AI assistant. Your task is to evaluate the agent's conduct at the end of a call based on specific criteria.

    **Assessment Rules:**

    **Mark "Met" if:**
    1. **Further Assistance**: The agent explicitly asked the customer if they had any other issues or needed further assistance (e.g., phrases like "Is there anything else I can assist you with?").
    2. **Effective IVR Survey**: The agent requested feedback from the customer or asked if they could transfer the call to an IVR for feedback, ensuring that the customer’s experience was shared. Additionally, If any keyword or phrase like "feedback IVR", "IVR feedback", "IVR", "feedback", "survey", "survey IVR" or "IVR survey" is found in the transcript, then mark it as "Met".
    4. **Greeting**: The agent ended the call politely with a positive closing statement (e.g., "Have a great day ahead").
    5. If the call ended abruptly due to reasons beyond the agent's control, such as network issues or call disconnection or if anyone (agent or customer) was not able to hear anything at the end of the transcript, or if the call closing was unclear or incomplete, mark "Met" for all parameters.

    **Mark "Not Met" if:**
    - Any of the above criteria were not followed.

    **Considerations:**
    - The agent may use any language (e.g., Hindi, English, or a mix of languages). Equivalent phrases in any language that align with the intent of these guidelines should be considered as satisfying the criteria.

    **Output Format:**

    Please output a JSON object as follows:
    ```json
    {
        "Further_Assistance": "Met" or "Not Met",
        "Further_Assistance_Evidence": "<specific phrases or actions>",
        "Effective_IVR_Survey": "Met" or "Not Met",
        "Effective_IVR_Survey_Evidence": "<specific phrases or actions>",
        "Greeting": "Met" or "Not Met",
        "Greeting_Evidence": "<specific phrases or actions>"
    }
    ```
    """

chat_opening_prompt = """
    You are a helpful and objective AI assistant. Please read the above transcript.


    Follow the instructions below to check if the agent has greeted the customer in accordance with the guidelines provided. Your output should be deterministic and consistent for the same prompt.

    Mark the output as 'Met' if the agent’s greeting matches the guidelines provided. Otherwise, mark it as 'Not Met'.

    Provide a reason for your decision. If you mark it as 'Met' give the exact statement used by the agent in the conversation. If you mark it as 'Not Met' explain what was missing or incorrect based on the guidelines.

    *Guidelines:*
    - Greet the customer by using any 'Good morning/Good afternoon/Good evening/Hello/morning/afternoon/evening'. Mark as 'Met' if any of the mentioned greeting phrases is present in the conversation
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
    - My Name
    - morning this is
    - morning, this is
    - morning. this is
    - afternoon. This is
    - afternoon This is
    - afternoon, This is
    - Evening, this is
    - Evening. This is
    - Evening this is
    - sir. This is
    - morning this side
    - morning, this side
    - morning. this side
    - afternoon. This side
    - afternoon This side
    - afternoon, This side
    - Evening, this side
    - Evening. This side
    - Evening this side
    - sir. This side
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
    - Am I talking to
    - Am I speaking with
    - Am I connected with
    The agent doesn't need to say his/her full name.
    If the agent use these kind of statement anywhere in the transcript mark it as Met.


    The agent may use any language (e.g., Hindi, English, or a mix of languages) and any equivalent phrases that meet the intent of these guidelines.

    Provide your assessment in a clear and concise manner. Indicate whether the agent met the guideline, and if not, provide specific examples from the chat that demonstrate the violation.

    *Output Format:*

    json
    {
        "Greeting_the_customer": "Met" or "Not Met",
        "Greeting_the_customer_evidence": "<detailed evidence>",
        "Self_introduction": "Met" or "Not Met",
        "Self_introduction_evidence": "<detailed evidence>",
        "Identity_confirmation": "Met" or "Not Met",
        "Identity_confirmation_evidence": "<detailed evidence>"

    }

    *Notice 1:* The agent may combine Hindi and English guidelines in a sentence, and this is acceptable.
    *Notice 2:* The agent's and customer's names can be in Hindi or English, and either is correct.


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

# Dictionary of prompts for easy access.
# Note: opening/chat_opening/chat_closing intentionally excluded.
ASSESSMENT_PROMPTS = {
    "closing": chat_closing_prompt,
    "reassurance": reassurance_prompt,
    "apology": apology_prompt,
    "empathy": empathy_prompt,
    "unethical_solicitation": unethical_Solicitation_prompt,
    "voice_of_customer": voice_of_customer_prompt,
}
