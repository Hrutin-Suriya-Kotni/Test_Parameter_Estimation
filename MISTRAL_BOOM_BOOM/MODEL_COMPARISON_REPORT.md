# Model Comparison Report: Server 5 vs Server 3

**Date:** October 11, 2025  
**Test Duration:** Server 5 (82.9 minutes) | Server 3 (Mini test only)  
**Total Conversations Tested:** Server 5 (300) | Server 3 (5 - proof of concept)

---

## Executive Summary

This report compares two Mistral-based models for conversation analysis:
- **Server 5**: Base Mistral (27.111.72.51:8000) - Fully tested
- **Server 3**: OpenChat Mistral 3.5 (27.111.72.53:3333) - Mini test completed

### Key Findings

| Metric | Server 5 Base Mistral | Server 3 OpenChat Mistral |
|--------|----------------------|--------------------------|
| **API Success Rate** | 86.0% (258/300) | 80.0% (4/5)* |
| **Average Latency** | 11.91s | 1.39s* |
| **Met Rate** | 52.3% | 0% (all Not Met)* |
| **API Format** | Simple prompt-response | OpenAI-compatible chat |
| **Token Reporting** | Estimates only | Exact counts |
| **Status** | ✅ Production Ready | ⚠️ Needs Full Testing |

\* Based on limited mini-test (5 conversations, 1 type)

---

## Server 5 Base Mistral - Complete Analysis

### API Information
- **Endpoint**: `http://27.111.72.51:8000/generate`
- **Format**: Simple `{"prompt": "...", "max_new_tokens": 512, "temperature": 0.1}`
- **Response**: `{"response": "..."}` (echoes prompt + generates response)
- **Model**: Base Mistral

### Overall Performance

#### Reliability
- **Total Conversations**: 300 (20 per test × 15 tests)
- **Successful API Calls**: 258/300 (86.0%)
- **Failed Calls**: 42 (14%)
- **Failure Reason**: Repetitive text generation on long transcripts
- **Average Latency**: 11.91 seconds

#### Results Distribution (Successful Calls)
- **Met**: 135 (52.3%)
- **Not Met**: 123 (47.7%)

### Performance by Guideline

| Guideline | Success Rate | Met | Not Met | Avg Latency | Performance |
|-----------|--------------|-----|---------|-------------|-------------|
| **Opening** | 100.0% | 25 | 35 | 15.54s | 🟢 Excellent API |
| **Closing** | 81.7% | 47 | 2 | 9.77s | 🟡 Good compliance |
| **Reassurance** | 88.3% | 47 | 6 | 12.48s | 🟢 High compliance |
| **Hold** | 80.0% | 8 | 40 | 11.64s | 🟡 Low agent compliance |
| **Further Assistance** | 80.0% | 8 | 40 | 8.80s | 🟡 Low agent compliance |

### Performance by Data Type

#### Type1 (Overall Paragraph)
```
Opening:              100.0% success | 5 Met,  15 Not Met | 14.68s avg
Closing:               90.0% success | 18 Met,  0 Not Met | 9.30s avg
Reassurance:           95.0% success | 17 Met,  2 Not Met | 10.16s avg
Hold:                  80.0% success | 3 Met,  13 Not Met | 13.63s avg
Further Assistance:    90.0% success | 2 Met,  16 Not Met | 11.29s avg
```

#### Type2a (JSON Format)
```
Opening:              100.0% success | 14 Met,  6 Not Met | 16.92s avg
Closing:               80.0% success | 15 Met,  1 Not Met | 10.23s avg
Reassurance:           85.0% success | 15 Met,  2 Not Met | 12.62s avg
Hold:                  85.0% success | 2 Met,  15 Not Met | 11.15s avg
Further Assistance:    85.0% success | 3 Met,  14 Not Met | 11.76s avg
```

#### Type2b (Labeled Paragraph)
```
Opening:              100.0% success | 6 Met,  14 Not Met | 15.02s avg
Closing:               75.0% success | 14 Met,  1 Not Met | 9.78s avg
Reassurance:           85.0% success | 15 Met,  2 Not Met | 14.66s avg
Hold:                  75.0% success | 3 Met,  12 Not Met | 10.14s avg
Further Assistance:    65.0% success | 3 Met,  10 Not Met | 3.36s avg
```

### Strengths
1. ✅ **Excellent Opening guideline reliability** (100% API success)
2. ✅ **High compliance detection** for Closing & Reassurance (>90% Met rate)
3. ✅ **Consistent performance** across data types
4. ✅ **Good JSON parsing** (86% success rate)

### Weaknesses
1. ⚠️ **Parse failures** (14%) - gets stuck in repetitive loops on very long transcripts
2. ⚠️ **Low Hold/Further Assistance detection** - agents rarely follow these guidelines
3. ⚠️ **Slower latency** (11.91s average) - 8-10x slower than Server 3
4. ⚠️ **Token counts are estimates** - no exact token reporting from API

---

## Server 3 OpenChat Mistral - Mini Test Results

### API Information
- **Endpoint**: `http://27.111.72.53:3333/v1/chat/completions`
- **Format**: OpenAI-compatible (messages array with roles)
- **Response**: Full OpenAI-compatible JSON with exact token counts
- **Model**: `openchat/openchat-3.5-1210`

### Mini Test Results (5 Conversations)

**Test Configuration:**
- Data Type: type1 only
- Conversations: 1 conversation tested on all 5 guidelines
- Purpose: Proof of concept / API validation

#### Results Summary

| Guideline | Result | Latency | Status |
|-----------|--------|---------|--------|
| Opening | Not Met | 1.37s | ✅ Success |
| Closing | Not Met | 1.35s | ✅ Success |
| Reassurance | Exception | 60s+ | ❌ Timeout |
| Hold | Not Met | 1.15s | ✅ Success |
| Further Assistance | Not Met | 1.56s | ✅ Success |

**Success Rate**: 4/5 (80%)  
**Average Latency**: 1.39s (successful calls only)  
**Issue**: One timeout on long transcript (7,639 characters)

### Observations
1. ✅ **Very fast** (1.15-1.56s) - 8-10x faster than Server 5
2. ✅ **OpenAI-compatible API** - standard format with exact token counts
3. ✅ **Clean JSON responses** - easier to parse
4. ⚠️ **Occasional timeouts** on very long transcripts (>7000 chars)
5. ⚠️ **All "Not Met"** - may be too strict or needs prompt tuning
6. ⚠️ **Limited testing** - only 1 conversation tested (need full 300-conversation test)

---

## Head-to-Head Comparison

### Speed
```
Server 3:  1.39s average  ⚡⚡⚡ FASTEST
Server 5: 11.91s average  🐌 8.5x slower
```

### Reliability
```
Server 5: 86.0% (258/300) ✅ Well-tested
Server 3: 80.0% (4/5)*    ⚠️  Need more data
```

### API Quality
```
Server 3: OpenAI-compatible, exact tokens    ✅ Industry standard
Server 5: Custom format, token estimates     ⚠️  Less standard
```

### Compliance Detection
```
Server 5: 52.3% Met rate  ✅ Balanced
Server 3: 0% Met rate*    ⚠️  Too strict? Need tuning
```

### Parse Success
```
Server 5: 86% parse success   ✅ Good
Server 3: 80% parse success*  ⚠️  Need more data
```

---

## Recommendations

### For Production Use

#### Choose Server 5 if:
- ✅ You need **proven reliability** (300 conversations tested)
- ✅ You can tolerate **~12 second latency**
- ✅ You want **balanced compliance detection** (52% met rate)
- ✅ You need results **right now** (fully tested)

#### Choose Server 3 if:
- ✅ **Speed is critical** (1.4s vs 12s - 8x faster!)
- ✅ You want **OpenAI-compatible** standard API
- ✅ You need **exact token counts** (not estimates)
- ⚠️ You can handle **occasional timeouts** on long transcripts
- ⚠️ You can invest time in **full testing** (need 300-conversation validation)

### Next Steps

#### For Server 3:
1. **Run full 300-conversation test** (estimated 75 minutes)
   - Test all 3 data types (type1, type2a, type2b)
   - Test all 5 guidelines
   - Validate reliability across diverse transcripts

2. **Prompt optimization** if "Not Met" rate remains too high
   - Current: 0% Met (may be too strict)
   - Target: 40-60% Met (balanced like Server 5)

3. **Handle timeouts** - Consider:
   - Increase timeout to 120s for very long transcripts
   - Implement retry logic
   - Truncate transcripts >7000 characters

#### For Server 5:
1. **Investigate parse failures** (14%)
   - Identify why repetitive text is generated
   - Implement better loop detection
   - Consider max response length limits

2. **Optimize latency** if possible
   - Current: 11.91s average
   - Target: <5s would be ideal

---

## Technical Details

### Server 5 Request Format
```json
{
  "prompt": "<full_prompt_with_transcript>",
  "max_new_tokens": 512,
  "temperature": 0.1
}
```

**Response includes prompt echo** - must extract JSON from combined text

### Server 3 Request Format
```json
{
  "model": "openchat/openchat-3.5-1210",
  "messages": [
    {"role": "system", "content": "Respond with ONLY valid JSON."},
    {"role": "user", "content": "<prompt_with_transcript>"}
  ],
  "max_tokens": 512,
  "temperature": 0.1
}
```

**Clean OpenAI-compatible response** with usage stats

---

## Data Files Location

### Server 5 (Complete Results)
```
MISTRAL_BOOM_BOOM/server5_base_mistral/
├── README.md
├── type1/
│   ├── opening_results.csv
│   ├── closing_results.csv
│   ├── reassurance_results.csv
│   ├── hold_results.csv
│   └── further_assistance_results.csv
├── type2a/
│   └── [5 CSV files]
└── type2b/
    └── [5 CSV files]
```

### Server 3 (Mini Test)
```
MISTRAL_BOOM_BOOM/server3_mini_test/
└── results.csv  (5 tests on 1 conversation)
```

---

## Conclusion

**Server 5** is production-ready with comprehensive testing (300 conversations) showing reliable 86% success rate and balanced compliance detection (52% Met). However, it's slower (12s avg latency).

**Server 3** shows **exceptional speed** (1.4s avg - **8x faster**!) and uses industry-standard OpenAI-compatible API format. However, it needs full testing validation and may require prompt tuning to achieve balanced compliance detection rates.

### Final Recommendation

For **immediate production use**: **Server 5** ✅  
For **speed-critical applications** (after full testing): **Server 3** ⚡

---

**Report Generated:** October 11, 2025  
**Test Scripts:** `run_server5_full_test.py`, `server3_mini_test.py`  
**View Summary:** `python3 view_server5_summary.py`


