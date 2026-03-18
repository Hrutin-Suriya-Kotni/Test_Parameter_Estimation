# Model Benchmark Report: OpenChat & Qwen vs Gemini (Ground Truth)

## Executive Summary

This report benchmarks **OpenChat-3.5-1210** and **Qwen2.5-7B-Instruct** against **Gemini 2.0 Flash** as the ground truth.

### Overall Agreement with Ground Truth

| Model | Total Tests | Matched | Disagreed | Agreement Rate | Parse Errors |
|-------|-------------|---------|-----------|----------------|---------------|
| **OpenChat-3.5-1210** | 100 | 63 | 37 | **63.0%** | 6 |
| **Qwen2.5-7B-Instruct** | 100 | 73 | 27 | **73.0%** | 1 |

**🎯 Winner:** Qwen with 73.0% agreement

## Detailed Benchmark Results

### Per-Guideline Performance

| Guideline | OpenChat Agreement | Qwen Agreement | Winner |
|-----------|-------------------|----------------|--------|
| Opening | 40.0% (8/20) | 70.0% (14/20) | **Qwen** |
| Closing | 75.0% (15/20) | 80.0% (16/20) | **Qwen** |
| Reassurance | 50.0% (10/20) | 70.0% (14/20) | **Qwen** |
| Hold | 75.0% (15/20) | 70.0% (14/20) | **OpenChat** |
| Further Assistance | 75.0% (15/20) | 75.0% (15/20) | **Tie** |


## Key Findings

### Overall Performance
1. **Qwen leads** with 73.0% agreement vs Qwen's 63.0%
2. **Difference**: 10.0 percentage points
3. **Parse errors**: Qwen (1) vs OpenChat (6)

### Best Performing Guidelines (both models)
  - Closing: Qwen leads (80.0%), average: 77.5%
  - Hold: OpenChat leads (75.0%), average: 72.5%
  - Further_Assistance: OpenChat leads (75.0%), average: 75.0%


## Recommendations

### Primary Model Selection

**Winner: Qwen2.5-7B-Instruct**
- Agreement rate: 73.0%
- Parse errors: 1
- Strengths: Holds advantage in 4/5 guidelines

### Per-Guideline Recommendations

- **Opening**: Use **Qwen** (70.0% agreement, 40.0% vs 70.0%)
- **Closing**: Use **Qwen** (80.0% agreement, 75.0% vs 80.0%)
- **Reassurance**: Use **Qwen** (70.0% agreement, 50.0% vs 70.0%)
- **Hold**: Use **OpenChat** (75.0% agreement, 70.0% vs 75.0%)
- **Further Assistance**: Use **OpenChat** (75.0% agreement, 75.0% vs 75.0%)


## Conclusion

**Qwen2.5-7B-Instruct** performs better overall with 73.0% agreement against Gemini ground truth, compared to OpenChat's 63.0%.

The recommended primary model is **Qwen2.5-7B-Instruct** for production deployment.

---

**Generated**: Benchmark comparison
**Ground Truth**: Gemini 2.0 Flash (66% Met rate)
**Benchmarked Models**: OpenChat-3.5-1210 (63.0%), Qwen2.5-7B-Instruct (73.0%)
**Test Dataset**: 20 conversations × 5 guidelines = 100 tests per model
