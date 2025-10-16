# Comprehensive Model Comparison Report
## Server 5 Base Mistral vs Server 3 OpenChat Mistral

**Generated:** October 12, 2025  
**Test Scope:** 300 conversations per model (3 data types × 5 guidelines × 20 conversations)  
**Total Tests:** 600 conversations analyzed

---

## Executive Summary

This report provides a comprehensive comparison of two Mistral-based models tested on identical datasets for conversation guideline compliance analysis.

### Models Tested

| Model | API Endpoint | Format | Status |
|-------|--------------|--------|--------|
| **Server 5 Base Mistral** | 27.111.72.51:8000/generate | Simple prompt-response | ✅ Production Ready |
| **Server 3 OpenChat Mistral 3.5** | 27.111.72.53:3333/v1/chat/completions | OpenAI-compatible | ⚠️ Reliability Issues |

### Key Performance Metrics

| Metric | Server 5 | Server 3 | Winner |
|--------|----------|----------|--------|
| **Success Rate** | 86.0% (258/300) | 46.3% (139/300) | 🏆 Server 5 |
| **Avg Latency** | 11.91s | 2.19s | 🏆 Server 3 (5.4x faster!) |
| **Met Rate** | 52.3% | 39.6% | 🏆 Server 5 |
| **Avg Tokens** | ~3000 (estimate) | 967 (exact) | - |
| **Token Reporting** | Estimates only | Exact counts | 🏆 Server 3 |
| **Parse Success** | 86% | 46% | 🏆 Server 5 |

---

## Detailed Performance Analysis

### 1. API Reliability

#### Server 5: 86.0% Success Rate ✅
- **Successful**: 258/300 calls
- **Failed**: 42 (14%)
- **Failure Type**: Repetitive text generation on long transcripts
- **Reliability**: Consistent across all test types

#### Server 3: 46.3% Success Rate ⚠️
- **Successful**: 139/300 calls
- **Failed**: 161 (53.7%)
- **Failure Type**: Timeouts on transcripts >3500 chars
- **Reliability**: Highly variable (20%-65% depending on data type)

**Winner:** 🏆 **Server 5** - Far more reliable

---

### 2. Speed Performance

#### Server 5: 11.91s Average ⚡
- Range: 3.36s - 16.92s
- Slower on longer transcripts
- Consistent within data types

#### Server 3: 2.19s Average ⚡⚡⚡
- Range: 1.08s - 3.58s
- **5.4x faster** than Server 5
- Fast on successful calls
- **BUT**: Many calls timeout (>600s) on long transcripts

**Winner:** 🏆 **Server 3** - When it works, it's significantly faster

---

### 3. Compliance Detection Quality

#### Server 5: 52.3% Met Rate
- Met: 135 conversations
- Not Met: 123 conversations
- Balanced detection (not too strict/lenient)
- Consistent across guidelines

#### Server 3: 39.6% Met Rate
- Met: 55 conversations  
- Not Met: 84 conversations
- More strict/conservative
- Variable across guidelines

**Winner:** 🏆 **Server 5** - More balanced detection

---

## Performance by Guideline

### Opening Guideline

| Metric | Server 5 | Server 3 |
|--------|----------|----------|
| Success Rate | 100.0% (60/60) 🟢 | 45.0% (27/60) 🔴 |
| Met | 25 (41.7%) | 14 (51.9%) |
| Not Met | 35 (58.3%) | 13 (48.1%) |
| Avg Latency | 15.54s | 2.54s ⚡ |

**Analysis:** Server 5 has perfect reliability but slower. Server 3 is 6x faster but half the calls timeout.

### Closing Guideline

| Metric | Server 5 | Server 3 |
|--------|----------|----------|
| Success Rate | 81.7% (49/60) 🟡 | 36.7% (22/60) 🔴 |
| Met | 47 (95.9%) | 11 (50.0%) |
| Not Met | 2 (4.1%) | 11 (50.0%) |
| Avg Latency | 9.77s | 2.44s ⚡ |

**Analysis:** Server 5 detects high closing compliance. Server 3 faster but lower success rate.

### Reassurance Guideline

| Metric | Server 5 | Server 3 |
|--------|----------|----------|
| Success Rate | 88.3% (53/60) 🟢 | 50.0% (30/60) 🔴 |
| Met | 47 (88.7%) | 19 (63.3%) |
| Not Met | 6 (11.3%) | 11 (36.7%) |
| Avg Latency | 12.48s | 1.89s ⚡ |

**Analysis:** Server 5 has high reliability and detects strong reassurance compliance. Server 3 is 6.6x faster but less reliable.

### Hold Guideline

| Metric | Server 5 | Server 3 |
|--------|----------|----------|
| Success Rate | 80.0% (48/60) 🟡 | 46.7% (28/60) 🔴 |
| Met | 8 (16.7%) | 1 (3.6%) |
| Not Met | 40 (83.3%) | 27 (96.4%) |
| Avg Latency | 11.64s | 2.42s ⚡ |

**Analysis:** Both models detect LOW hold compliance (agents rarely follow guidelines). Server 3 is 4.8x faster.

### Further Assistance Guideline

| Metric | Server 5 | Server 3 |
|--------|----------|----------|
| Success Rate | 80.0% (48/60) 🟡 | 53.3% (32/60) 🔴 |
| Met | 8 (16.7%) | 10 (31.3%) |
| Not Met | 40 (83.3%) | 22 (68.8%) |
| Avg Latency | 8.80s | 1.93s ⚡ |

**Analysis:** Both detect LOW compliance. Server 3 is 4.6x faster.

---

## Performance by Data Type

### Type1 (Overall Paragraph Format)

| Guideline | Server 5 Success | Server 3 Success | Server 5 Met | Server 3 Met |
|-----------|------------------|------------------|--------------|--------------|
| Opening | 100% | 40% | 25% | 25% |
| Closing | 90% | 40% | 100% | 12.5% |
| Reassurance | 95% | 65% | 89% | 38% |
| Hold | 80% | 35% | 19% | 0% |
| Further Assist | 90% | 65% | 11% | 54% |

**Type1 Average:**
- Server 5: 91% success, 14.68s-11.29s latency
- Server 3: 49% success, 2.39s-3.58s latency

### Type2a (JSON Format)

| Guideline | Server 5 Success | Server 3 Success | Server 5 Met | Server 3 Met |
|-----------|------------------|------------------|--------------|--------------|
| Opening | 100% | 45% | 70% | 100% |
| Closing | 80% | 30% | 94% | 100% |
| Reassurance | 85% | 65% | 88% | 100% |
| Hold | 85% | 60% | 12% | 0% |
| Further Assist | 85% | 50% | 18% | 0% |

**Type2a Average:**
- Server 5: 87% success, 10.23s-16.92s latency
- Server 3: 50% success, 1.08s-2.07s latency

### Type2b (Labeled Paragraph Format)

| Guideline | Server 5 Success | Server 3 Success | Server 5 Met | Server 3 Met |
|-----------|------------------|------------------|--------------|--------------|
| Opening | 100% | 50% | 30% | 30% |
| Closing | 75% | 40% | 93% | 50% |
| Reassurance | 85% | 20% | 88% | 25% |
| Hold | 75% | 45% | 20% | 11% |
| Further Assist | 65% | 45% | 23% | 33% |

**Type2b Average:**
- Server 5: 80% success, 3.36s-15.02s latency
- Server 3: 40% success, 1.80s-2.71s latency

---

## Side-by-Side Comparison

### Reliability Score
```
Server 5: ████████████████░░░░  86%  🏆 WINNER
Server 3: █████████░░░░░░░░░░░  46%
```

### Speed Score  
```
Server 5: ██░░░░░░░░░░░░░░░░░░  11.91s
Server 3: ██████████████████░░  2.19s  🏆 WINNER (5.4x faster!)
```

### Compliance Detection Balance
```
Server 5: ██████████░░░░░░░░░░  52% Met  🏆 WINNER (balanced)
Server 3: ████████░░░░░░░░░░░░  40% Met  (more strict)
```

---

## Strengths & Weaknesses

### Server 5 Base Mistral

#### ✅ Strengths:
1. **High reliability** (86% success) - handles diverse transcript lengths
2. **Balanced compliance detection** (52% Met rate)
3. **Consistent performance** across all data types
4. **Handles long transcripts** well (up to 12,946 chars tested)
5. **Production-ready** - proven on 258 successful evaluations

#### ❌ Weaknesses:
1. **Slow** (11.91s average - 5.4x slower than Server 3)
2. **Token estimates only** (no exact counts from API)
3. **Echoes prompts** in response (requires careful JSON extraction)
4. **Some parse failures** (14%) on repetitive text generation

### Server 3 OpenChat Mistral 3.5

#### ✅ Strengths:
1. **Very fast** (2.19s average - 5.4x faster than Server 5!) ⚡
2. **Exact token counts** from OpenAI-compatible API
3. **Clean JSON responses** when successful
4. **Industry-standard API format** (OpenAI-compatible)
5. **Excellent on short transcripts** (<3000 chars)

#### ❌ Weaknesses:
1. **Low reliability** (46% success) - fails on 53.7% of calls
2. **Cannot handle long transcripts** (>3500 chars cause timeouts)
3. **High timeout rate** on Type1 and Type2b data
4. **Context window issues** despite 8192 token limit
5. **Not production-ready** in current state

---

## Recommendations

### For Production Deployment

#### Use Server 5 if:
✅ **Reliability is critical** (86% vs 46%)  
✅ You have **diverse transcript lengths** (short to very long)  
✅ You need **consistent performance** across data types  
✅ You can tolerate **~12 second latency**  
✅ You want a **proven, stable** solution

#### Use Server 3 if:
✅ **Speed is paramount** (2.2s vs 12s)  
✅ Your transcripts are **consistently short** (<3000 chars)  
✅ You can handle **53% failure rate** on mixed data  
✅ You need **exact token counts** for billing/monitoring  
✅ You prefer **OpenAI-compatible** API format

### Hybrid Approach

Consider routing based on transcript length:
- **Short transcripts** (<3000 chars) → Server 3 (fast, 2s response)
- **Long transcripts** (>3000 chars) → Server 5 (reliable, 12s response)

---

## Performance by Data Type

### Type1 (Overall Paragraph)
```
Server 5: 91% avg success | 9.30s-14.68s latency | Good reliability
Server 3: 49% avg success | 2.23s-3.58s latency | Poor on long texts
```
**Recommendation:** Server 5 for Type1

### Type2a (JSON Format - Shortest transcripts)
```
Server 5: 87% avg success | 10.23s-16.92s latency | Reliable  
Server 3: 50% avg success | 1.08s-2.07s latency | Fast but unstable
```
**Recommendation:** Server 5 for reliability, or Server 3 if speed critical

### Type2b (Labeled Paragraph)
```
Server 5: 80% avg success | 3.36s-15.02s latency | Most reliable
Server 3: 40% avg success | 1.80s-2.71s latency | High failure rate
```
**Recommendation:** Server 5 for Type2b

---

## Cost-Benefit Analysis

### Server 5
- **Time Cost:** ~83 minutes for 300 conversations
- **Success Rate:** 86%
- **Effective Conversations/Hour:** ~186 successful evaluations/hour
- **Pros:** Reliable, handles all transcript sizes
- **Cons:** Slower processing

### Server 3  
- **Time Cost:** Variable (many timeouts at 10+ minutes each)
- **Success Rate:** 46%
- **Effective Conversations/Hour:** ~1640 calls/hour (but only 46% succeed)
- **Pros:** Very fast when successful
- **Cons:** Unreliable, wastes time on timeouts

---

## Technical Details

### Server 5 Configuration
```json
{
  "api_url": "http://27.111.72.51:8000/generate",
  "format": "Simple prompt-response",
  "request": {
    "prompt": "<full_prompt>",
    "max_new_tokens": 512,
    "temperature": 0.1
  },
  "response": {
    "response": "<echoes_prompt_plus_answer>"
  },
  "note": "Echoes full prompt in response - requires JSON extraction"
}
```

### Server 3 Configuration
```json
{
  "api_url": "http://27.111.72.53:3333/v1/chat/completions",
  "model": "openchat/openchat-3.5-1210",
  "format": "OpenAI-compatible",
  "context_limit": 8192,
  "request": {
    "model": "openchat/openchat-3.5-1210",
    "messages": [
      {"role": "system", "content": "..."},
      {"role": "user", "content": "..."}
    ],
    "max_tokens": 512,
    "temperature": 0.1
  },
  "response": {
    "choices": [{"message": {"content": "..."}}],
    "usage": {"prompt_tokens": X, "completion_tokens": Y}
  },
  "note": "Clean OpenAI format with exact token counts"
}
```

---

## Detailed Results by Guideline

### Opening Guideline Results

| Data Type | Server 5 Success | Server 3 Success | Server 5 Met% | Server 3 Met% |
|-----------|------------------|------------------|---------------|---------------|
| Type1 | 20/20 (100%) | 8/20 (40%) | 25% | 25% |
| Type2a | 20/20 (100%) | 9/20 (45%) | 70% | 100% |
| Type2b | 20/20 (100%) | 10/20 (50%) | 30% | 30% |
| **Overall** | **60/60 (100%)** 🏆 | **27/60 (45%)** | **41.7%** | **51.9%** |

**Avg Latency:** Server 5: 15.54s | Server 3: 2.54s ⚡

### Closing Guideline Results

| Data Type | Server 5 Success | Server 3 Success | Server 5 Met% | Server 3 Met% |
|-----------|------------------|------------------|---------------|---------------|
| Type1 | 18/20 (90%) | 8/20 (40%) | 100% | 12.5% |
| Type2a | 16/20 (80%) | 6/20 (30%) | 94% | 100% |
| Type2b | 15/20 (75%) | 8/20 (40%) | 93% | 50% |
| **Overall** | **49/60 (82%)** 🏆 | **22/60 (37%)** | **96%** 🏆 | **50%** |

**Avg Latency:** Server 5: 9.77s | Server 3: 2.44s ⚡

### Reassurance Guideline Results

| Data Type | Server 5 Success | Server 3 Success | Server 5 Met% | Server 3 Met% |
|-----------|------------------|------------------|---------------|---------------|
| Type1 | 19/20 (95%) | 13/20 (65%) | 89% | 38% |
| Type2a | 17/20 (85%) | 13/20 (65%) | 88% | 100% |
| Type2b | 17/20 (85%) | 4/20 (20%) | 88% | 25% |
| **Overall** | **53/60 (88%)** 🏆 | **30/60 (50%)** | **88%** 🏆 | **63%** |

**Avg Latency:** Server 5: 12.48s | Server 3: 1.89s ⚡

### Hold Guideline Results

| Data Type | Server 5 Success | Server 3 Success | Server 5 Met% | Server 3 Met% |
|-----------|------------------|------------------|---------------|---------------|
| Type1 | 16/20 (80%) | 7/20 (35%) | 19% | 0% |
| Type2a | 17/20 (85%) | 12/20 (60%) | 12% | 0% |
| Type2b | 15/20 (75%) | 9/20 (45%) | 20% | 11% |
| **Overall** | **48/60 (80%)** 🏆 | **28/60 (47%)** | **17%** 🏆 | **3.6%** |

**Avg Latency:** Server 5: 11.64s | Server 3: 2.42s ⚡

**Note:** Low Met rates indicate agents rarely follow hold guidelines (not a model issue).

### Further Assistance Guideline Results

| Data Type | Server 5 Success | Server 3 Success | Server 5 Met% | Server 3 Met% |
|-----------|------------------|------------------|---------------|---------------|
| Type1 | 18/20 (90%) | 13/20 (65%) | 11% | 54% |
| Type2a | 17/20 (85%) | 10/20 (50%) | 18% | 0% |
| Type2b | 13/20 (65%) | 9/20 (45%) | 23% | 33% |
| **Overall** | **48/60 (80%)** 🏆 | **32/60 (53%)** | **17%** | **31%** 🏆 |

**Avg Latency:** Server 5: 8.80s | Server 3: 1.93s ⚡

---

## Issues Identified

### Server 5 Issues
1. **Slow latency** (11.91s avg) - not suitable for real-time applications
2. **Token estimates only** - no exact counts for monitoring
3. **Repetitive text generation** (14% failure rate) on some transcripts
4. **Prompt echo** in response requires careful JSON parsing

### Server 3 Issues
1. **High failure rate** (53.7%) - NOT production-ready
2. **Cannot handle long transcripts** - timeouts on >3500 chars
3. **Inconsistent reliability** across data types (20%-65% success)
4. **Context window problems** despite 8192 token limit
5. **Frequent 600s+ timeouts** waste significant time

---

## Final Recommendations

### For Immediate Production Use
🏆 **Server 5 Base Mistral** is the clear choice:
- Proven reliability (86% success)
- Handles all transcript lengths
- Consistent performance
- Ready to deploy

### Server 3 - Action Items Required

❌ **NOT recommended for production** until issues are resolved:

1. **Fix timeout issues** on transcripts >3500 chars
2. **Investigate why context overflows** happen despite dynamic max_tokens
3. **Improve reliability** from 46% to at least 80%
4. **Test with transcript truncation** or chunking for long conversations

### Potential Server 3 Improvements

To make Server 3 production-ready:
1. Implement **automatic transcript truncation** to 3000 chars max
2. Add **retry logic** with exponential backoff
3. Implement **health checks** before each batch
4. Consider **different model** or server configuration
5. Add **circuit breaker** pattern for repeated failures

---

## Conclusion

**Server 5** is the production-ready choice with:
- ✅ 86% reliability
- ✅ Handles all transcript sizes
- ✅ Balanced compliance detection (52% Met rate)
- ⚠️ Trade-off: Slower (12s avg)

**Server 3** shows promise with exceptional speed (5.4x faster) but:
- ❌ 46% reliability (too low for production)
- ❌ Cannot handle long transcripts
- ❌ Needs significant reliability improvements

**Overall Winner:** 🏆 **Server 5 Base Mistral**

---

## Data Files

### Server 5 Results
```
MISTRAL_BOOM_BOOM/server5_base_mistral/
├── README.md
├── type1/ (5 CSV files - 100 conversations)
├── type2a/ (5 CSV files - 100 conversations)
└── type2b/ (5 CSV files - 100 conversations)
```

### Server 3 Results  
```
MISTRAL_BOOM_BOOM/server3_base_openchat_mistral/
├── type1/ (5 CSV files - 100 conversations, 49% success)
├── type2a/ (5 CSV files - 100 conversations, 50% success)
└── type2b/ (5 CSV files - 100 conversations, 40% success)
```

### Quick View Commands
```bash
# Server 5 summary
python3 view_server5_summary.py

# Server 3 summary  
python3 view_server3_summary.py
```

---

**Report End** | Generated: October 12, 2025 | Total Tests: 600 conversations


