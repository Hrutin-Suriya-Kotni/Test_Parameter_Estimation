# Server 3 OpenChat Mistral - Test Results

## API Information
- **Endpoint**: `http://27.111.72.53:3333/v1/chat/completions`
- **Model**: `openchat/openchat-3.5-1210`
- **API Type**: OpenAI-compatible (vLLM backend)
- **Max Context**: 8192 tokens

## Test Configuration
- **Date**: October 11-12, 2025
- **Conversations per test**: 20
- **Total conversations attempted**: 300
- **Data types**: type1, type2a, type2b
- **Guidelines tested**: Opening, Closing, Reassurance, Hold, Further Assistance

## Folder Structure

```
server3_base_openchat_mistral/
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

## Overall Performance Summary

### API Reliability
- **Success Rate**: 46.3% (139/300) ⚠️
- **Failed Calls**: 161 (53.7%)
- **Primary Issue**: Timeouts on transcripts >3500 characters
- **Average Latency**: 2.19 seconds (successful calls)

### Results Distribution (from successful calls)
- **Met**: 55 (39.6%)
- **Not Met**: 84 (60.4%)

### Performance by Guideline

| Guideline | Success Rate | Met | Not Met | Avg Latency | Notes |
|-----------|--------------|-----|---------|-------------|-------|
| Opening | 45.0% (27/60) | 14 | 13 | 2.54s | 🔴 High failure rate |
| Closing | 36.7% (22/60) | 11 | 11 | 2.44s | 🔴 High failure rate |
| Reassurance | 50.0% (30/60) | 19 | 11 | 1.89s | 🟡 Moderate |
| Hold | 46.7% (28/60) | 1 | 27 | 2.42s | 🔴 High failure rate |
| Further Assistance | 53.3% (32/60) | 10 | 22 | 1.93s | 🟡 Moderate |

## Performance by Data Type

### Type1 (Overall Paragraph)
```
Opening:            40% success (8/20)  | Met:  2 | Not Met:  6 | Latency: 3.58s
Closing:            40% success (8/20)  | Met:  1 | Not Met:  7 | Latency: 2.70s
Reassurance:        65% success (13/20) | Met:  5 | Not Met:  8 | Latency: 2.23s
Hold:               35% success (7/20)  | Met:  0 | Not Met:  7 | Latency: 3.47s
Further Assistance: 65% success (13/20) | Met:  7 | Not Met:  6 | Latency: 2.39s
```

### Type2a (JSON Format - Shortest transcripts)
```
Opening:            45% success (9/20)  | Met:  9 | Not Met:  0 | Latency: 1.64s ⚡
Closing:            30% success (6/20)  | Met:  6 | Not Met:  0 | Latency: 2.07s
Reassurance:        65% success (13/20) | Met: 13 | Not Met:  0 | Latency: 1.63s ⚡
Hold:               60% success (12/20) | Met:  0 | Not Met: 12 | Latency: 1.08s ⚡
Further Assistance: 50% success (10/20) | Met:  0 | Not Met: 10 | Latency: 1.53s
```

### Type2b (Labeled Paragraph)
```
Opening:            50% success (10/20) | Met:  3 | Not Met:  7 | Latency: 2.41s
Closing:            40% success (8/20)  | Met:  4 | Not Met:  4 | Latency: 2.56s
Reassurance:        20% success (4/20)  | Met:  1 | Not Met:  3 | Latency: 1.80s
Hold:               45% success (9/20)  | Met:  1 | Not Met:  8 | Latency: 2.71s
Further Assistance: 45% success (9/20)  | Met:  3 | Not Met:  6 | Latency: 1.88s
```

## Key Findings

### ✅ Strengths
1. **Exceptional speed** - 2.19s average (5.4x faster than Server 5!)
2. **Fastest on Type2a** - 1.08-2.07s (JSON format, shorter transcripts)
3. **OpenAI-compatible API** - industry standard format
4. **Exact token counts** - proper usage reporting
5. **When it works, it works fast** - sub-2 second responses common

### ❌ Critical Issues
1. **Low reliability** - 46.3% success rate (53.7% failure)
2. **Cannot handle long transcripts** - timeouts on >3500 characters
3. **Worse on Type2b** - only 40% average success
4. **Context window problems** - fails despite 8192 token limit
5. **Inconsistent** - success rate varies 20%-65% by test

## Comparison with Server 5

| Aspect | Server 5 | Server 3 | Winner |
|--------|----------|----------|--------|
| **Reliability** | 86% | 46% | 🏆 Server 5 |
| **Speed** | 11.91s | 2.19s | 🏆 Server 3 (5.4x faster!) |
| **Met Detection** | 52% | 40% | 🏆 Server 5 |
| **Long Transcripts** | ✅ Handles well | ❌ Times out | 🏆 Server 5 |
| **Token Reporting** | Estimates | Exact | 🏆 Server 3 |
| **Production Ready** | ✅ Yes | ❌ No | 🏆 Server 5 |

## Recommendations

### ❌ NOT Recommended for Production
Server 3 has too many reliability issues:
- 53.7% failure rate
- Cannot handle long transcripts
- Inconsistent across data types
- Wastes time on 10-minute timeouts

### ✅ Potential Use Cases
Server 3 could be useful for:
- **Short transcripts only** (<3000 chars) where speed is critical
- **Type2a data** specifically (best performance, 1.08s latency)
- **Development/testing** where failures are acceptable
- **Scenarios where 5.4x speed** justifies 53% failure rate

### Required Improvements
Before production use:
1. Fix timeout issues on long transcripts
2. Improve reliability from 46% to at least 80%
3. Implement transcript truncation/chunking
4. Add retry logic and fallback mechanisms
5. Consider different model or server configuration

## CSV File Columns

Each CSV file contains:
- `conversation_id` - Unique identifier
- `data_type` - Data format
- `parameter_tested` - Guideline being evaluated
- `success` - Whether API call succeeded (True/False)
- `result_value` - "Met", "Not Met", or error type
- `evidence` - Model's explanation
- `total_latency` - Response time in seconds
- `prompt_tokens` - Exact input token count
- `completion_tokens` - Exact output token count
- `total_tokens` - Total tokens used
- `api_temperature` - 0.1
- `api_max_tokens` - Dynamically adjusted based on input
- Additional metadata

## Server Configuration

The API runs on vLLM with:
```bash
--model "openchat/openchat-3.5-1210"
--port 3333
--max-num-batched-tokens 8192
--max-num-seqs 64
--enable-cuda-graph
--dtype bfloat16
```

**GPU**: NVIDIA RTX 4000 Ada (20GB)

## Next Steps

1. **For production**: Use Server 5 (see ../server5_base_mistral/)
2. **To improve Server 3**: Investigate timeout root cause
3. **Alternative**: Hybrid approach (Server 3 for short, Server 5 for long transcripts)

---

**See full comparison**: [COMPREHENSIVE_MODEL_COMPARISON.md](../COMPREHENSIVE_MODEL_COMPARISON.md)


