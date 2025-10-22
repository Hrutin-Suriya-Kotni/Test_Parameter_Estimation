# 🔄 Pre-Processed Data - Filtering Summary

**Date:** October 22, 2025  
**Criteria:** Excluded conversations where Type2a JSON > 6,000 tokens

---

## 📊 Results

| Data Type | Original | Excluded | Remaining |
|-----------|----------|----------|-----------|
| **Type1 (CSV)** | 85 | 11 | **74** |
| **Type2a (JSON)** | 85 | 11 | **74** |
| **Type2b (CSV)** | 85 | 11 | **74** |

**Total:** 74 conversations retained across all formats

---

## 🚫 Excluded Conversations (11 total)

| # | Conversation ID | Type2a Tokens | Reason |
|---|----------------|---------------|--------|
| 1 | c977f98b | 6,695 | > 6K |
| 2 | d175b0b0 | 10,774 | > 6K |
| 3 | d78e3ed6 | 8,519 | > 6K |
| 4 | d94271a9 | 7,434 | > 6K |
| 5 | db6bfca6 | 7,092 | > 6K |
| 6 | dbc758dd | 11,017 | > 6K |
| 7 | e09812de | 24,097 | > 6K (Extreme) |
| 8 | e25ad441 | 7,571 | > 6K |
| 9 | e7b06e64 | 11,398 | > 6K |
| 10 | ebc71356 | 17,636 | > 6K (Extreme) |
| 11 | f107d468 | 8,411 | > 6K |

---

## 📁 Output Location

```
pre-processed-data/
├── type1_overall_paragraph.csv      (74 conversations)
├── type2b_labeled_paragraph.csv     (74 conversations)
├── type2a_json/                     (74 JSON files)
├── EXCLUDED_CONVERSATIONS.txt       (11 IDs)
└── FILTERING_SUMMARY.md             (this file)
```

---

## ✅ Benefits

- All remaining conversations fit comfortably in Mistral 8K context
- Type2a max tokens reduced from 24,097 → ~5,200
- Improved processing reliability and speed
- 87% of original dataset retained

---

**Filter Script:** `filter_data.py`  
**Source Data:** `data/` directory

