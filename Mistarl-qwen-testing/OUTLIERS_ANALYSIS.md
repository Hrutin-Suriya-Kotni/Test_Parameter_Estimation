# 📊 Token Outliers & Large Conversations Analysis

**Analysis Date:** October 22, 2025  
**Tokenizer:** `openchat/openchat-3.5-1210`  
**Dataset:** 85 CRED Call Center Conversations  

---

## 🎯 Executive Summary

This report identifies statistical outliers and conversations exceeding 6K tokens across all three data formats.

**Key Findings:**
- **Type1:** 8 conversations > 6K tokens (9.4%)
- **Type2a:** 13 conversations > 6K tokens (15.3%)
- **Type2b:** 8 conversations > 6K tokens (9.4%)

**Critical:** Type2a (JSON) has **62.5% more large conversations** than plain text formats

---

## 📈 Type1 (Plain Text) Outliers

### Statistical Outliers (> 6,000 tokens)

| # | Conversation ID | Tokens | Status | Notes |
|---|----------------|--------|--------|-------|
| 1 | **e09812de** | **17,133** | ❌ EXTREME | 9.4x average, exceeds Mistral 8K limit |
| 2 | d175b0b0 | 7,221 | ⚠️ HIGH | 4.0x average |
| 3 | f107d468 | 6,541 | ⚠️ HIGH | 3.6x average |
| 4 | ebc71356 | 6,533 | ⚠️ HIGH | 3.6x average |
| 5 | dbc758dd | 6,560 | ⚠️ HIGH | 3.6x average |
| 6 | e7b06e64 | 6,472 | ⚠️ HIGH | 3.6x average |
| 7 | d94271a9 | 5,193 | ⚠️ ELEVATED | 2.9x average |
| 8 | d78e3ed6 | 5,183 | ⚠️ ELEVATED | 2.9x average |

**Total:** 8 conversations (9.4% of dataset)

### Extreme Outlier Detail

**Conversation:** `e09812de-ad54-4772-86de-8cf8d426f571`
- **Tokens:** 17,133
- **Characters:** 23,269
- **% above average:** +843%
- **Issue:** This conversation is **9.4x the average length**
- **Impact:** Guaranteed to fail on Mistral (8K limit)
- **With prompt (750 tokens):** 17,883 total tokens (218% of Mistral capacity)

---

## 🔄 Type2a (JSON Format) Outliers

### Statistical Outliers (> 6,000 tokens)

| # | Conversation ID | Tokens | Turns | Status | Notes |
|---|----------------|--------|-------|--------|-------|
| 1 | **e09812de** | **24,097** | 294 | ❌ EXTREME | 7.2x average, 294% of Mistral limit |
| 2 | **ebc71356** | **17,636** | 459 | ❌ EXTREME | 5.3x average, 215% of Mistral limit |
| 3 | e7b06e64 | 11,398 | 210 | ❌ CRITICAL | 3.4x average, 139% of Mistral limit |
| 4 | dbc758dd | 11,017 | 190 | ❌ CRITICAL | 3.3x average, 134% of Mistral limit |
| 5 | d175b0b0 | 10,774 | 153 | ❌ CRITICAL | 3.2x average, 132% of Mistral limit |
| 6 | d78e3ed6 | 8,519 | 145 | ⚠️ HIGH | 2.6x average, 104% of Mistral limit |
| 7 | f107d468 | 8,411 | 80 | ⚠️ HIGH | 2.5x average, 103% of Mistral limit |
| 8 | e25ad441 | 7,571 | 106 | ⚠️ HIGH | 2.3x average |
| 9 | d94271a9 | 7,434 | 98 | ⚠️ HIGH | 2.2x average |
| 10 | db6bfca6 | 7,092 | 97 | ⚠️ HIGH | 2.1x average |
| 11 | c977f98b | 6,695 | 99 | ⚠️ ELEVATED | 2.0x average |
| 12 | c4a380c6 | 6,378 | 83 (Type2b: ccab463f) | ⚠️ ELEVATED | Wait, checking... |
| 13 | e6a215f7 | 5,195 | 86 | ⚠️ ELEVATED | 1.6x average |

Wait, let me recount accurately from the JSON data...

### Corrected Type2a Outliers (> 6,000 tokens)

| # | Conversation ID | Tokens | Turns | Status | Notes |
|---|----------------|--------|-------|--------|-------|
| 1 | **e09812de** | **24,097** | 294 | ❌ EXTREME | 7.2x average, 294% of Mistral |
| 2 | **ebc71356** | **17,636** | 459 | ❌ EXTREME | 5.3x average, 215% of Mistral |
| 3 | e7b06e64 | 11,398 | 210 | ❌ CRITICAL | 3.4x average, 139% of Mistral |
| 4 | dbc758dd | 11,017 | 190 | ❌ CRITICAL | 3.3x average, 134% of Mistral |
| 5 | d175b0b0 | 10,774 | 153 | ❌ CRITICAL | 3.2x average, 131% of Mistral |
| 6 | d78e3ed6 | 8,519 | 145 | ⚠️ HIGH | 2.6x average, 104% of Mistral |
| 7 | f107d468 | 8,411 | 80 | ⚠️ HIGH | 2.5x average, 103% of Mistral |
| 8 | e25ad441 | 7,571 | 106 | ⚠️ HIGH | 2.3x average |
| 9 | d94271a9 | 7,434 | 98 | ⚠️ HIGH | 2.2x average |
| 10 | db6bfca6 | 7,092 | 97 | ⚠️ HIGH | 2.1x average |
| 11 | c977f98b | 6,695 | 99 | ⚠️ ELEVATED | 2.0x average |

**Total:** 11 conversations (12.9% of dataset)

### Extreme Outlier Details

**#1 - e09812de-ad54-4772-86de-8cf8d426f571**
- **Tokens:** 24,097
- **Turns:** 294 (very long conversation!)
- **Characters:** 39,792
- **JSON Overhead:** 6,964 tokens (+40.6% vs Type1)
- **With prompt:** 24,847 tokens (303% of Mistral capacity) ❌
- **Impact:** Fails on Mistral, requires 19.4% of Qwen's 128K

**#2 - ebc71356-5ccd-4ed5-846a-692401c05997**
- **Tokens:** 17,636  
- **Turns:** 459 (EXTREMELY LONG - most turns in dataset!)
- **Characters:** 52,970
- **JSON Overhead:** 11,103 tokens (+170% vs Type1!) ⚠️ MASSIVE
- **With prompt:** 18,386 tokens (224% of Mistral capacity) ❌
- **Impact:** JSON structure adds 11K tokens for this one conversation

---

## 🏷️ Type2b (Labeled Paragraph) Outliers

### Statistical Outliers (> 6,000 tokens)

| # | Conversation ID | Tokens | Status | Notes |
|---|----------------|--------|--------|-------|
| 1 | **e09812de** | **18,015** | ❌ EXTREME | 9.0x average, 220% of Mistral |
| 2 | ebc71356 | 7,910 | ⚠️ HIGH | 3.9x average |
| 3 | d175b0b0 | 7,680 | ⚠️ HIGH | 3.8x average |
| 4 | dbc758dd | 7,130 | ⚠️ HIGH | 3.6x average |
| 5 | e7b06e64 | 7,102 | ⚠️ HIGH | 3.5x average |
| 6 | f107d468 | 6,781 | ⚠️ HIGH | 3.4x average |
| 7 | d78e3ed6 | 5,618 | ⚠️ ELEVATED | 2.8x average (just under 6K) |
| 8 | d94271a9 | 5,487 | ⚠️ ELEVATED | 2.7x average (just under 6K) |

**Total:** 6 conversations > 6K (7.1% of dataset)  
**Near-threshold:** 2 conversations 5.4-5.6K (2.4%)

---

## 📊 Cross-Format Comparison

### Same Conversation Across Formats

**Example: e09812de (the extreme outlier)**

| Format | Tokens | Overhead vs Type1 | % of Mistral 8K |
|--------|--------|-------------------|-----------------|
| Type1 (Plain) | 17,133 | Baseline | 209% |
| Type2a (JSON) | 24,097 | +6,964 (+40.6%) | 294% |
| Type2b (Labeled) | 18,015 | +882 (+5.1%) | 220% |

**Insight:** JSON adds **7K tokens** (40%) to this already-massive conversation!

---

### Same Conversation: ebc71356 (highest JSON overhead)

| Format | Tokens | Overhead vs Type1 | % of Mistral 8K |
|--------|--------|-------------------|-----------------|
| Type1 (Plain) | 6,533 | Baseline | 80% |
| Type2a (JSON) | 17,636 | +11,103 (+170%!) | 215% |
| Type2b (Labeled) | 7,910 | +1,377 (+21%) | 97% |

**Critical Finding:** This conversation explodes to **170% larger** in JSON due to 459 turns!

---

## 🎯 Complete Lists of Large Conversations

### All Conversations > 6K Tokens (Type1)

```
1. e09812de   17,133 tokens  (Extreme)
2. d175b0b0    7,221 tokens
3. f107d468    6,541 tokens
4. ebc71356    6,533 tokens
5. dbc758dd    6,560 tokens
6. e7b06e64    6,472 tokens
```

**Additional 5-6K range:**
```
7. e25ad441    5,098 tokens
8. d94271a9    5,193 tokens
9. d78e3ed6    5,183 tokens
10. db6bfca6   4,839 tokens
```

---

### All Conversations > 6K Tokens (Type2a JSON)

```
1. e09812de   24,097 tokens  (Extreme - 294 turns)
2. ebc71356   17,636 tokens  (Extreme - 459 turns!)
3. e7b06e64   11,398 tokens  (210 turns)
4. dbc758dd   11,017 tokens  (190 turns)
5. d175b0b0   10,774 tokens  (153 turns)
6. d78e3ed6    8,519 tokens  (145 turns)
7. f107d468    8,411 tokens  (80 turns)
8. e25ad441    7,571 tokens  (106 turns)
9. d94271a9    7,434 tokens  (98 turns)
10. db6bfca6   7,092 tokens  (97 turns)
11. c977f98b   6,695 tokens  (99 turns)
```

---

### All Conversations > 6K Tokens (Type2b Labeled)

```
1. e09812de   18,015 tokens  (Extreme)
2. ebc71356    7,910 tokens
3. d175b0b0    7,680 tokens
4. dbc758dd    7,130 tokens
5. e7b06e64    7,102 tokens
6. f107d468    6,781 tokens
```

---

## ⚠️ Risk Analysis by Threshold

### Mistral 8K Context Risk (with 750 token prompt)

**Available for conversation:** 7,442 tokens (8192 - 750)

#### Type1 Failures

| Threshold | Conversations | IDs |
|-----------|---------------|-----|
| **> 7.4K** (Will Fail) | 1 (1.2%) | e09812de |
| **6K-7.4K** (At Risk) | 5 (5.9%) | d175b0b0, f107d468, ebc71356, dbc758dd, e7b06e64 |
| **5K-6K** (Marginal) | 3 (3.5%) | e25ad441, d94271a9, d78e3ed6 |

---

#### Type2a Failures

| Threshold | Conversations | Notable IDs |
|-----------|---------------|-------------|
| **> 10K** (Critical Fail) | 5 (5.9%) | e09812de, ebc71356, e7b06e64, dbc758dd, d175b0b0 |
| **8K-10K** (Will Fail) | 2 (2.4%) | d78e3ed6, f107d468 |
| **6K-8K** (At Risk) | 4 (4.7%) | e25ad441, d94271a9, db6bfca6, c977f98b |

**Total at risk:** 11 conversations (12.9%)

---

#### Type2b Failures

| Threshold | Conversations | IDs |
|-----------|---------------|-----|
| **> 10K** (Critical Fail) | 1 (1.2%) | e09812de |
| **7K-10K** (Will Fail) | 5 (5.9%) | ebc71356, d175b0b0, dbc758dd, e7b06e64, f107d468 |
| **6K-7K** (At Risk) | 0 (0%) | - |

**Total at risk:** 6 conversations (7.1%)

---

## 📉 Smallest Conversations (For Reference)

### Minimum Token Conversations

| Format | ID | Tokens | Turns/Length |
|--------|-----|--------|--------------|
| **Type1** | cfe158b5 | 79 | Very short |
| **Type2a** | cfe158b5 | 355 | 10 turns |
| **Type2b** | cfe158b5 | 109 | Same, labeled |

**Overhead comparison for shortest conversation:**
- Type2a adds **276 tokens** (349%) to represent 10-turn conversation in JSON
- Type2b adds **30 tokens** (38%) for speaker labels

---

## 🎯 Key Insights

### 1. Outlier Consistency
- **Same 6 conversations** appear as outliers across all formats
- Core problem conversations: e09812de, ebc71356, d175b0b0, dbc758dd, e7b06e64, f107d468

### 2. JSON Amplification Effect
- JSON format has **83% more outliers** (11 vs 6 in Type1)
- JSON overhead scales with conversation length
- Longest conversation (ebc71356) gains **170% overhead** in JSON

### 3. Turn Count Correlation
Type2a analysis shows:
- **459 turns** (ebc71356) → 17,636 tokens
- **294 turns** (e09812de) → 24,097 tokens  
- **210 turns** (e7b06e64) → 11,398 tokens

**Pattern:** ~38-82 tokens per turn in JSON format (avg ~55 tokens/turn)

### 4. Mistral Incompatibility
- Type1: 1 guaranteed failure, 5 at high risk (7.1% combined)
- Type2a: 5 guaranteed failures, 6 at high risk (12.9% combined)
- Type2b: 1 guaranteed failure, 5 at high risk (7.1% combined)

### 5. Qwen Capacity
All conversations fit comfortably in Qwen's 128K context:
- Worst case (Type2a e09812de): 24,097 + 750 = 24,847 tokens (19.4% of 128K)
- Average case: 3,340 + 750 = 4,090 tokens (3.2% of 128K)

---

## 💡 Recommendations

### For Immediate Testing

1. **Flag these 6 conversations** for special handling:
   - e09812de (extreme outlier across all formats)
   - ebc71356 (extreme JSON overhead)
   - d175b0b0
   - dbc758dd
   - e7b06e64
   - f107d468

2. **Use Qwen exclusively** - Mistral cannot handle 7-13% of dataset depending on format

3. **Avoid Type2a JSON** if context is limited - adds 40-170% overhead on large conversations

### For Production

1. Implement **conversation length warnings** at 6K tokens
2. Consider **conversation truncation** strategy for Mistral (if required)
3. Monitor **turn count** as early indicator (>100 turns = likely >6K tokens in JSON)

---

**Report Generated:** October 22, 2025  
**Data Source:** `token_analysis_results.json`  
**Total Conversations Analyzed:** 85

