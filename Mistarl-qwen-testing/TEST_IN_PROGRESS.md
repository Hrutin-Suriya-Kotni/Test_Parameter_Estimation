# 🔄 OpenChat Testing - In Progress

**Started:** October 22, 2025  
**Server:** 27.111.72.51:3333  
**Model:** openchat/openchat-3.5-1210

---

## 📊 Test Scope

| Component | Count | Details |
|-----------|-------|---------|
| **Conversations** | 74 | Pre-processed (filtered) |
| **Data Types** | 3 | Type1, Type2a, Type2b |
| **Guidelines** | 5 | opening, closing, reassurance, hold, further_assistance |
| **Total Tests** | **1,110** | 74 × 3 × 5 |

---

## ⚙️ Test Configuration

- **Token Limit:** 8,100 tokens
- **Pre-validation:** Checks tokens before sending
- **Action on exceed:** Logs "LIMIT EXCEEDED", skips request
- **Retry Logic:** 3 attempts with 2s delay
- **Rate Limiting:** 0.5s between requests

---

## 🎯 Expected Duration

- **Minimum:** ~9 minutes (555 seconds at 0.5s per test)
- **Realistic:** ~15-20 minutes (with API latency)
- **Status:** Check `results/` folder for output files

---

## 📂 Output Location

```
Mistarl-qwen-testing/results/
└── openchat_test_results_YYYYMMDD_HHMMSS.json
```

---

## 📈 What's Being Tested

### Each Test Includes:
- ✅ Token validation (prompt + conversation < 8,100)
- ✅ API call to OpenChat server
- ✅ JSON response extraction
- ✅ Success/failure logging
- ✅ Latency measurement

### Metrics Collected:
- Success rate per guideline
- Success rate per data type
- Token limit violations
- API failures
- Response latency

---

**Monitor:** `tail -f` the terminal or check results folder periodically

