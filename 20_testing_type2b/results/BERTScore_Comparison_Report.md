# BERTScore Comparison Report

## Overview
- **Total Evaluations**: 180 conversation-guideline pairs per model
- **Models Compared**: OpenChat, Qwen, Mistral (vs Gemini reference)
- **Metrics**: BERTScore F1 (semantic similarity) + Status Agreement
- **Data Source**: `FULL_RESULTS_20_convo.csv`
- **Report Generated**: November 1, 2025

---

## Overall Model Comparison

| Model | Agreement % | Mean F1 | Median F1 | Std F1 | Min F1 | Max F1 | Count |
|-------|-------------|---------|-----------|--------|--------|--------|-------|
| **Qwen** | 73.9% | 0.7867 | 0.8186 | 0.1288 | 0.3494 | 1.0 | 167 |
| **Mistral** | 63.9% | 0.7561 | 0.7782 | 0.1376 | 0.3608 | 1.0 | 164 |
| **OpenChat** | 60.6% | 0.7461 | 0.7774 | 0.1501 | 0.3007 | 1.0 | 159 |

### Agreement vs Disagreement Breakdown

| Model | Total | Agreement | Disagreement | Not Applicable | Low Outliers | High Outliers |
|-------|-------|-----------|--------------|----------------|--------------|---------------|
| **OpenChat** | 180 | 109 (60.6%) | 71 (39.4%) | 0 (0.0%) | 1 | 0 |
| **Qwen** | 180 | 133 (73.9%) | 47 (26.1%) | 0 (0.0%) | 2 | 0 |
| **Mistral** | 180 | 115 (63.9%) | 65 (36.1%) | 0 (0.0%) | 5 | 0 |

---

## Per-Guideline Performance Analysis

### Agreement Rate (%) by Guideline

| Guideline | OpenChat | Qwen | Mistral | Average |
|-----------|----------|------|---------|---------|
| **apology** | 50.0% | 75.0% | 90.0% | 71.7% |
| **closing** | 70.0% | 80.0% | 75.0% | 75.0% |
| **empathy** | 75.0% | 80.0% | 90.0% | 81.7% |
| **feedback_pitch** | 30.0% | 55.0% | 45.0% | 43.3% |
| **further_assistance** | 70.0% | 75.0% | 25.0% | 56.7% |
| **hold** | 70.0% | 70.0% | 60.0% | 66.7% |
| **opening** | 55.0% | 70.0% | 65.0% | 63.3% |
| **reassurance** | 45.0% | 70.0% | 60.0% | 58.3% |
| **rude_sarcastic** | 80.0% | 90.0% | 65.0% | 78.3% |

### BERTScore F1 by Guideline

| Guideline | OpenChat Mean | Qwen Mean | Mistral Mean | OpenChat Range | Qwen Range | Mistral Range |
|-----------|---------------|-----------|--------------|----------------|------------|---------------|
| **apology** | 0.7224 | 0.7888 | 0.7774 | 0.5563–0.9337 | 0.5618–0.9105 | 0.4840–0.9359 |
| **closing** | 0.8098 | 0.8395 | 0.7822 | 0.6743–0.9024 | 0.6083–0.9189 | 0.6530–0.9472 |
| **empathy** | 0.7355 | 0.7777 | 0.7028 | 0.5273–1.0000 | 0.4925–0.9371 | 0.3608–0.8742 |
| **feedback_pitch** | 0.5444 | 0.6029 | 0.7526 | 0.4609–0.6278 | 0.3494–0.7938 | 0.5708–1.0000 |
| **further_assistance** | 0.6009 | 0.7893 | 0.7091 | 0.3007–0.9400 | 0.4690–1.0000 | 0.3750–0.9400 |
| **hold** | 0.7904 | 0.7719 | 0.7747 | 0.4431–0.9555 | 0.4214–0.9022 | 0.4329–1.0000 |
| **opening** | 0.8359 | 0.8930 | 0.8627 | 0.6394–0.9189 | 0.7288–0.9762 | 0.6150–0.9838 |
| **reassurance** | 0.7132 | 0.7446 | 0.7300 | 0.5442–0.9680 | 0.5087–0.9353 | 0.4240–0.9374 |
| **rude_sarcastic** | 0.7789 | 0.7534 | 0.7106 | 0.5173–0.9799 | 0.5303–0.9309 | 0.4541–0.8163 |

### Detailed Per-Guideline Statistics

| Guideline | Model | Count | Agreement % | Mean F1 | Median F1 | Std F1 | Min F1 | Max F1 | Outliers |
|-----------|-------|-------|-------------|---------|-----------|--------|--------|--------|----------|
| apology | OpenChat | 20 | 50.0% | 0.7224 | 0.6932 | 0.1213 | 0.5563 | 0.9337 | 0 |
| apology | Qwen | 20 | 75.0% | 0.7888 | 0.8242 | 0.1012 | 0.5618 | 0.9105 | 0 |
| apology | Mistral | 20 | 90.0% | 0.7774 | 0.8150 | 0.1432 | 0.4840 | 0.9359 | 0 |
| closing | OpenChat | 20 | 70.0% | 0.8098 | 0.8124 | 0.0609 | 0.6743 | 0.9024 | 0 |
| closing | Qwen | 20 | 80.0% | 0.8395 | 0.8572 | 0.0742 | 0.6083 | 0.9189 | 1 |
| closing | Mistral | 20 | 75.0% | 0.7822 | 0.7802 | 0.0645 | 0.6530 | 0.9472 | 3 |
| empathy | OpenChat | 20 | 75.0% | 0.7355 | 0.7405 | 0.1338 | 0.5273 | 1.0000 | 0 |
| empathy | Qwen | 20 | 80.0% | 0.7777 | 0.8327 | 0.1456 | 0.4925 | 0.9371 | 0 |
| empathy | Mistral | 20 | 90.0% | 0.7028 | 0.7463 | 0.1558 | 0.3608 | 0.8742 | 2 |
| feedback_pitch | OpenChat | 20 | 30.0% | 0.5444 | 0.5444 | 0.1180 | 0.4609 | 0.6278 | 0 |
| feedback_pitch | Qwen | 20 | 55.0% | 0.6029 | 0.5408 | 0.1782 | 0.3494 | 0.7938 | 0 |
| feedback_pitch | Mistral | 20 | 45.0% | 0.7526 | 0.7758 | 0.1369 | 0.5708 | 1.0000 | 1 |
| further_assistance | OpenChat | 20 | 70.0% | 0.6009 | 0.5614 | 0.2330 | 0.3007 | 0.9400 | 0 |
| further_assistance | Qwen | 20 | 75.0% | 0.7893 | 0.8074 | 0.1562 | 0.4690 | 1.0000 | 0 |
| further_assistance | Mistral | 20 | 25.0% | 0.7091 | 0.7685 | 0.1753 | 0.3750 | 0.9400 | 0 |
| hold | OpenChat | 20 | 70.0% | 0.7904 | 0.8570 | 0.1482 | 0.4431 | 0.9555 | 0 |
| hold | Qwen | 20 | 70.0% | 0.7719 | 0.8101 | 0.1215 | 0.4214 | 0.9022 | 2 |
| hold | Mistral | 20 | 60.0% | 0.7747 | 0.8396 | 0.1536 | 0.4329 | 1.0000 | 0 |
| opening | OpenChat | 20 | 55.0% | 0.8359 | 0.8573 | 0.0764 | 0.6394 | 0.9189 | 0 |
| opening | Qwen | 20 | 70.0% | 0.8930 | 0.8978 | 0.0631 | 0.7288 | 0.9762 | 1 |
| opening | Mistral | 20 | 65.0% | 0.8627 | 0.8818 | 0.1009 | 0.6150 | 0.9838 | 2 |
| reassurance | OpenChat | 20 | 45.0% | 0.7132 | 0.6914 | 0.1155 | 0.5442 | 0.9680 | 1 |
| reassurance | Qwen | 20 | 70.0% | 0.7446 | 0.7725 | 0.1160 | 0.5087 | 0.9353 | 0 |
| reassurance | Mistral | 20 | 60.0% | 0.7300 | 0.7213 | 0.1334 | 0.4240 | 0.9374 | 0 |
| rude_sarcastic | OpenChat | 20 | 80.0% | 0.7789 | 0.8077 | 0.1160 | 0.5173 | 0.9799 | 2 |
| rude_sarcastic | Qwen | 20 | 90.0% | 0.7534 | 0.7156 | 0.1037 | 0.5303 | 0.9309 | 0 |
| rude_sarcastic | Mistral | 20 | 65.0% | 0.7106 | 0.7220 | 0.0886 | 0.4541 | 0.8163 | 3 |

---

## Outlier Observations

| Model | Lowest F1 Score | Guideline | Highest F1 Score | Guideline |
|-------|-----------------|-----------|------------------|-----------|
| **OpenChat** | 0.3007 | further_assistance | 1.0000 | empathy |
| **Qwen** | 0.3494 | feedback_pitch | 1.0000 | further_assistance |
| **Mistral** | 0.3608 | empathy | 1.0000 | feedback_pitch, hold |

---

## Key Insights

### Performance Rankings
1. **Highest Agreement**: Qwen (73.9%)
2. **Highest Semantic Similarity**: Qwen (Mean F1: 0.7867)
3. **Most Consistent**: Qwen (Lowest Std: 0.1288)

### Agreement vs Semantic Similarity

| Scenario | Average F1 Score |
|----------|------------------|
| Models **agree** on status | ~0.82 |
| Models **disagree** on status | ~0.70 |

### Guideline Difficulty

| Category | Guideline | Avg Agreement | Notes |
|----------|-----------|---------------|-------|
| **Easiest** | empathy | 81.7% | Most consistent across models |
| **Moderate** | rude_sarcastic | 78.3% | High agreement for OpenChat & Qwen |
| **Moderate** | closing | 75.0% | Balanced performance |
| **Challenging** | further_assistance | 56.7% | Mistral struggles (25% agreement) |
| **Most Difficult** | feedback_pitch | 43.3% | Universally challenging |

---

## Recommendations

### Immediate Actions
1. **Investigate `feedback_pitch` disagreements** - lowest avg agreement (43.3%)
   - Review evidence text for all models
   - Clarify evaluation criteria

2. **Review `further_assistance` for Mistral** - only 25% agreement
   - Significant outlier compared to OpenChat (70%) and Qwen (75%)

3. **Analyze outlier cases** per model to understand failure modes
   - OpenChat: F1 < 0.35 on further_assistance
   - Qwen: F1 < 0.40 on feedback_pitch
   - Mistral: F1 < 0.40 on empathy (despite 90% agreement)

### Long-term Improvements
- Align scoring criteria for low-agreement guidelines
- Use high-performing guidelines (empathy, closing) as benchmarks
- Consider domain-specific fine-tuning for challenging guidelines

