APOLOGY_EMPATHY_PROMPT = """

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
    {
        "Apology_result": "Met" or "Not Met",
        "Empathy_result": "Met" or "Not Met",
        "Apology_evidence": "<Brief explanation on why this category was selected>",
        "Empathy_evidence": "<Brief explanation on why this category was selected>",
        "Apology_Category": "<Selected category from the list only>",
        "Empathy_Category": "<Selected category from the list only>"
    }
    ```
    Additional Notes:
    ✅ Strict Category Usage: The "Category" field should only contain a value from the predefined list, with no extra explanations.
    ✅ Evidence Column Usage: Any explanation for why the category was selected should be included in the "Evidence" column.
    ✅ No Empty Evidence: If an apology or empathy is "Not Met," ensure the evidence field contains a valid reason rather than "None."
    ✅ Consistent Standards: Ensure every transcript is evaluated using the same criteria.

    Analyze the following call transcript between a customer and an agent. Identify instances where the agent issued an apology or demonstrated empathy. Highlight specific phrases or actions and explain why they qualify. Provide a summary of the agent’s overall behavior throughout the call.

"""

OUTPUT_FORMAT_GUIDELINES = """
  Provide your assessment in a clear and concise manner.

  CRITICAL: You must respond with ONLY a valid JSON object. No additional text before or after. Do not include code fences.

  JSON Rules:
  - Use double quotes for all keys and string values
  - Do not add trailing commas
  - Do not include explanations outside the JSON
  - Keep values short and factual; put explanations in the evidence fields
"""

APOLOGY_PROMPT = """
    You are a helpful and objective AI assistant. Review the transcript and determine whether the agent properly apologized when necessary.

    Assessment Criteria:
    - If an apology was NOT needed, mark Apology_result as "Met" and state in Apology_evidence that no apology was required.
    - If an apology WAS needed:
      - If given properly, mark Apology_result as "Met" and include exact statements used and why they adhere to apology guidelines.
      - If NOT properly given, mark Apology_result as "Not Met", select exactly one Apology_Category (from the list), and explain briefly in Apology_evidence.

    Guidelines for Identifying Apologies:
    - Explicit Apologies: Direct expressions of regret (Hindi or English), e.g., "Sorry for the inconvenience"
    - Acknowledgment of fault/issue
    - Empathetic language
    - Reassurance that the issue will be addressed

    Apology_Category (choose exactly one):
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

    Output formatting considerations:
    {OUTPUT_FORMAT_GUIDELINES}

    Return ONLY this JSON:
    {
        "Apology_result": "Met" or "Not Met",
        "Apology_evidence": "<brief explanation or exact quotes>",
        "Apology_Category": "<exactly one from the list; empty if Met>"
    }
"""

EMPATHY_PROMPT = """
    You are a helpful and objective AI assistant. Review the transcript and determine whether the agent demonstrated empathy where appropriate.

    Assessment Criteria:
    - If empathy WAS demonstrated, mark Empathy_result as "Met" and include exact statements showing empathy.
    - If empathy was NOT required, mark Empathy_result as "Met" and state that empathy was not necessary.
    - If empathy was NOT demonstrated when it should have been, mark Empathy_result as "Not Met", choose one Empathy_Category (from the list), and explain briefly in Empathy_evidence.

    Guidelines for Identifying Empathy:
    - Acknowledgment of feelings
    - Apologies/expressions of regret
    - Validation and reassurance
    - Commitment to help

    Empathy_Category (choose exactly one):
    - The agent brushes off or ignores the customer’s concerns or feelings
    - The agent language or tone feels impersonal, scripted, or detached
    - The agent interrupts the customer or doesn’t give them a chance to fully express concerns
    - The agent does not express empathy or regret when a mistake or issue negatively impacts the customer
    - The agent uses generic or irrelevant responses that do not acknowledge the customer’s specific situation

    Output formatting considerations:
    {OUTPUT_FORMAT_GUIDELINES}

    Return ONLY this JSON:
    {
        "Empathy_result": "Met" or "Not Met",
        "Empathy_evidence": "<brief explanation or exact quotes>",
        "Empathy_Category": "<exactly one from the list; empty if Met>"
    }
"""


REASSURANCE_PROMPT = """
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
      {
          "Reassurance_result": "Met" or "Not Met",
          "Reassurance_evidence": "<detailed evidence>",
          "Reassurance_Category": "<Selected category from the list only>"
      }

      ```
"""


FEEDBACK_PITCH_PROMPT = """
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


      Output formatting considerations:
      {OUTPUT_FORMAT_GUIDELINES}

      Return ONLY this JSON:
      {
          "Category": "<Incomplete feedback request/Declined Feedback by the Customer/Customer declined the feedback and then call ended abruptly/Customer declined the feedback and the call ended without any disconnect phrase/The customer agreed to give feedback>",
          "Summary": "<brief summary>",
          "Supporting_Evidence": "<exact phrase(s) from transcript or N/A>"
      }
"""


RUDE_SARCASTIC_PROMPT = """
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

      Output formatting considerations:
      {OUTPUT_FORMAT_GUIDELINES}

      Return ONLY this JSON:
      {
          "Sarcasm_rude_behaviour": "<Met/Not Met>",
          "Sarcasm_rude_behaviour_evidence": "<detailed evidence>"
      }

"""

