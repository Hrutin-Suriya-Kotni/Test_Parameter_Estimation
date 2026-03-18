# Model Performance Comparison Report

## Executive Summary

This report compares the performance of **OpenChat-3.5-1210** and **Qwen2.5-7B** models against **Gemini-2.0-Flash** as the ground truth benchmark. The evaluation is based on guideline compliance across 100 conversation test cases with 93 valid comparisons after data cleaning.

## Key Findings

- **Qwen2.5-7B outperforms OpenChat-3.5-1210** across all major metrics
- **Qwen** achieves 73.12% accuracy vs OpenChat's 67.74%
- **Qwen** shows superior precision (89.13%) compared to OpenChat (80.39%)
- Both models have identical recall rates (67.21%) against Gemini

## Performance Metrics

### OpenChat-3.5-1210 vs Gemini-2.0-Flash

| Metric | Value |
|--------|-------|
| **Accuracy** | 67.74% |
| **Precision** | 80.39% |
| **Recall** | 67.21% |
| **F1 Score** | 73.21% |
| **Agreement Rate** | 67.74% |

#### Confusion Matrix
```
                Predicted (OpenChat)
                Not Met    Met
Actual   Not Met   22      10
(Gemini)    Met    20      41
```

**Breakdown:**
- True Positives: 41
- True Negatives: 22  
- False Positives: 10
- False Negatives: 20

### Qwen2.5-7B vs Gemini-2.0-Flash

| Metric | Value |
|--------|-------|
| **Accuracy** | 73.12% |
| **Precision** | 89.13% |
| **Recall** | 67.21% |
| **F1 Score** | 76.64% |
| **Agreement Rate** | 73.12% |

#### Confusion Matrix
```
                Predicted (Qwen)
                Not Met    Met
Actual   Not Met   27       5
(Gemini)    Met    20      41
```

**Breakdown:**
- True Positives: 41
- True Negatives: 27
- False Positives: 5  
- False Negatives: 20

## Model Comparison Table

| Model | Accuracy | Precision | Recall | F1 Score | True Positives | False Positives | Agreement w/ Gemini |
|-------|----------|-----------|---------|----------|----------------|-----------------|-------------------|
| **Qwen2.5-7B** | **73.12%** | **89.13%** | 67.21% | **76.64%** | 41 | **5** | **73.12%** |
| OpenChat-3.5-1210 | 67.74% | 80.39% | 67.21% | 73.21% | 41 | 10 | 67.74% |
| **Difference** | **+5.38%** | **+8.74%** | **0.00%** | **+3.43%** | **0** | **-5** | **+5.38%** |

## Analysis

### Strengths & Weaknesses

**Qwen2.5-7B:**
- ✅ **Higher precision** - Makes fewer false positive errors
- ✅ **Better overall accuracy** 
- ✅ **Superior F1 score** - Better balance of precision/recall
- ⚠️ Same recall as OpenChat - Both miss 20 true positives

**OpenChat-3.5-1210:**
- ⚠️ **More false positives** - 10 vs Qwen's 5
- ⚠️ **Lower precision** - Less reliable when predicting "Met"
- ⚠️ **Lower accuracy** overall
- ✅ Same recall as Qwen

### Critical Insights

1. **Both models struggle with recall** (67.21%) - missing 1/3 of cases Gemini identifies as "Met"
2. **Qwen is more conservative** - significantly fewer false positives (5 vs 10)
3. **OpenChat tends to over-predict** - higher false positive rate
4. **Strong inter-model agreement** (68.82%) despite differences with Gemini

## Recommendations

1. **Use Qwen2.5-7B** for production deployment - superior accuracy and precision
2. **Focus on recall improvement** - both models miss ~33% of positive cases
3. **Consider ensemble approach** - leverage agreement between models
4. **Investigate false negatives** - analyze the 20 cases both models miss

## Technical Details

- **Total Test Cases:** 100
- **Valid Comparisons:** 93 (after removing parse errors)
- **Ground Truth:** Gemini-2.0-Flash-Exp
- **Evaluation Method:** Binary classification (Met/Not Met)
- **Data Source:** Conversation guideline compliance testing

---
*Report generated on: October 28, 2025*  
*Test Data: 20_testing_type1/results/comparison_results.csv*
