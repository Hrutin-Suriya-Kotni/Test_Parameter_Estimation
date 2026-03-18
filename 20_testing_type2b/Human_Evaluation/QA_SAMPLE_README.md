# QA Evaluation Sample

This file contains a curated sample for QA team evaluation with anonymized model names and clean data.

## 📄 File: `QA_evaluation_sample.csv`

### 🎯 Purpose
Manual quality assurance evaluation of LLM guideline assessments without model bias.

### 📊 Sample Details

**Total Tests:** 30 (6 per guideline × 5 guidelines)
**Unique Conversations:** 13
**Data Type:** Type2b labeled conversations

### 📋 Guidelines Covered (6 tests each)

1. **Opening** - Greeting and name confirmation (6 tests)
2. **Closing** - Ending call with feedback request (6 tests)  
3. **Reassurance** - Providing assurance to customer (6 tests)
4. **Hold** - Proper hold statements (6 tests)
5. **Further Assistance** - Asking for additional help (6 tests)

### 🏷️ Model Labels (Anonymized)

- **LLM1** = OpenChat-3.5-1210 (8B parameters, vLLM on RTX 4000)
- **LLM2** = Qwen2.5-7B-Instruct (7B parameters, vLLM on RTX 4000)
- **Gemini** = Gemini-2.0-Flash (Ground Truth Benchmark)

### 📊 Status Distribution

**LLM1:**
- Met: 20 (66.7%)
- Not Met: 10 (33.3%)

**LLM2:**
- Met: 17 (56.7%)
- Not Met: 13 (43.3%)

**Gemini (Ground Truth):**
- Met: 20 (66.7%)
- Not Met: 10 (33.3%)

### 🔍 Data Quality

✅ **No Parse Errors** - All tests have clean Met/Not Met statuses
✅ **Complete Transcripts** - Avg 4,543 characters (no truncation)
✅ **Complete Evidences** - Full model reasoning preserved
✅ **Random Sampling** - Unbiased selection (seed=42 for reproducibility)

**Evidence Lengths:**
- LLM1: Avg 188 chars
- LLM2: Avg 240 chars (most detailed)
- Gemini: Avg 178 chars

### 📁 CSV Structure

```csv
conversation_id,transcript,guideline,llm1_status,llm1_evidence,llm2_status,llm2_evidence,gemini_status,gemini_evidence
```

**Columns:**
1. `conversation_id` - Unique conversation identifier
2. `transcript` - Complete conversation (agent + customer messages)
3. `guideline` - Assessment guideline being evaluated
4. `llm1_status` - LLM1 assessment (Met/Not Met)
5. `llm1_evidence` - LLM1's reasoning and evidence
6. `llm2_status` - LLM2 assessment (Met/Not Met)
7. `llm2_evidence` - LLM2's reasoning and evidence
8. `gemini_status` - Gemini assessment (Met/Not Met)
9. `gemini_evidence` - Gemini's reasoning and evidence

### 📋 Filtered Data

**Original Dataset:** 100 rows (20 conversations × 5 guidelines)
**Filtered Out:** 8 rows with parse errors
**Clean Dataset:** 92 rows available
**Selected:** 30 rows (6 random per guideline)

### 🎯 QA Evaluation Instructions

#### For Each Test Row:

1. **Read the complete transcript** (column 2)
2. **Understand the guideline** being assessed (column 3)
3. **Review LLM1's assessment:**
   - Status: Met or Not Met?
   - Evidence: Does it cite actual conversation excerpts?
   - Accuracy: Is the status justified by the evidence?

4. **Review LLM2's assessment:**
   - Status: Met or Not Met?
   - Evidence: Does it cite actual conversation excerpts?
   - Accuracy: Is the status justified by the evidence?

5. **Compare with Gemini (Ground Truth):**
   - Which LLM (1 or 2) agrees with Gemini?
   - If disagreement: Which model is more accurate?
   - Are the evidences compelling?

6. **Manual Assessment:**
   - Read the transcript yourself
   - Decide: Met or Not Met?
   - Compare your judgment with all three models

#### Evaluation Metrics to Track:

- **LLM1 Accuracy:** How often does LLM1 match your assessment?
- **LLM2 Accuracy:** How often does LLM2 match your assessment?
- **Evidence Quality:** Which model provides better reasoning?
- **Gemini Baseline:** How often do you agree with Gemini?

### 💡 Tips for QA Evaluators

1. **Read Full Transcripts:** Don't rely on evidences alone
2. **Check Language Mix:** Transcripts contain Hindi + English
3. **Watch for Edge Cases:** Partial compliance, implied statements
4. **Note Disagreements:** Where models diverge is most interesting
5. **Be Objective:** Don't let model names influence judgment

### 🔄 Reproducibility

- **Random Seed:** 42 (for consistent sampling)
- **Selection:** Stratified by guideline (6 per guideline)
- **Filtering:** Parse errors excluded automatically
- **Sorting:** By guideline then conversation_id

### 📊 Expected QA Output

Create a summary spreadsheet with:
- Test number (1-30)
- Conversation ID
- Guideline
- Your manual assessment (Met/Not Met)
- LLM1 correct? (Yes/No)
- LLM2 correct? (Yes/No)
- Gemini correct? (Yes/No)
- Notes/Comments

### 📝 Sample QA Template

```csv
test_num,conv_id,guideline,qa_assessment,llm1_correct,llm2_correct,gemini_correct,notes
1,c4a380c6...,closing,Met,Yes,Yes,Yes,"All models correct"
2,c5255fb4...,closing,Met,Yes,Yes,Yes,"Clear feedback request"
...
```

---

## 🎉 Ready for QA Evaluation

This sample provides a **balanced, clean, and anonymized** dataset for human quality assessment of LLM performance on guideline compliance evaluation.

**Generated:** 2025-10-29
**Script:** `create_qa_evaluation_sample.py`
**Purpose:** Human evaluation of LLM accuracy

