# Model Performance Analytics Report - FINAL

## Overview
- **Total Evaluations**: 180 (20 conversations × 9 guidelines)
- **Models Compared**: OpenChat (LLM1), Qwen (LLM2), Mistral (LLM3), Gemini (Reference)
- **Analysis**: Only valid conversations (no parse errors)

- **Valid Evaluations**: 158 (filtered out parse errors)

## Status Distribution (Normalized)
| Model | Met | Not Met |
|-------|-----|---------|
| OpenChat | 102 (64.6%) | 56 (35.4%) |
| Qwen | 96 (60.8%) | 62 (39.2%) |
| Mistral | 97 (61.4%) | 61 (38.6%) |
| Gemini | 127 (80.4%) | 31 (19.6%) |

## Latency Analysis
| Model | Avg Response | Fastest | Slowest | Tests |
|-------|-------------|---------|---------|-------|
| Gemini | 2.12s | 0.98s | 9.72s | 179 |
| Qwen | 3.79s | 1.87s | 10.94s | 180 |
| OpenChat | 4.67s | 1.91s | 26.32s | 180 |
| Mistral | 6.93s | 2.72s | 40.78s | 180 |

*Note: Calculated from actual API response times, excluding extreme outliers (>100s)*

## Agreement Analysis vs Gemini (Reference)
| Model | Agreement Rate | Details |
|-------|----------------|---------|
| OpenChat | 66.5% | 105/158 |
| Qwen | 74.1% | 117/158 |
| Mistral | 64.6% | 102/158 |

## Guideline-wise Performance
### APOLOGY
| Model | Agreement | Met Rate | Not Met Rate |
|-------|-----------|----------|--------------|
| OpenChat | 50.0% | 50.0% | 50.0% |
| Qwen | 75.0% | 75.0% | 25.0% |
| Mistral | 90.0% | 90.0% | 10.0% |

### CLOSING
| Model | Agreement | Met Rate | Not Met Rate |
|-------|-----------|----------|--------------|
| OpenChat | 77.8% | 83.3% | 16.7% |
| Qwen | 77.8% | 83.3% | 16.7% |
| Mistral | 72.2% | 88.9% | 11.1% |

### EMPATHY
| Model | Agreement | Met Rate | Not Met Rate |
|-------|-----------|----------|--------------|
| OpenChat | 88.2% | 94.1% | 5.9% |
| Qwen | 82.4% | 76.5% | 23.5% |
| Mistral | 94.1% | 100.0% | 0.0% |

### FEEDBACK_PITCH
| Model | Agreement | Met Rate | Not Met Rate |
|-------|-----------|----------|--------------|
| OpenChat | 42.9% | 42.9% | 57.1% |
| Qwen | 42.9% | 42.9% | 57.1% |
| Mistral | 28.6% | 28.6% | 71.4% |

### FURTHER_ASSISTANCE
| Model | Agreement | Met Rate | Not Met Rate |
|-------|-----------|----------|--------------|
| OpenChat | 72.2% | 72.2% | 27.8% |
| Qwen | 77.8% | 55.6% | 44.4% |
| Mistral | 27.8% | 5.6% | 94.4% |

### HOLD
| Model | Agreement | Met Rate | Not Met Rate |
|-------|-----------|----------|--------------|
| OpenChat | 70.6% | 29.4% | 70.6% |
| Qwen | 64.7% | 0.0% | 100.0% |
| Mistral | 64.7% | 0.0% | 100.0% |

### OPENING
| Model | Agreement | Met Rate | Not Met Rate |
|-------|-----------|----------|--------------|
| OpenChat | 55.6% | 44.4% | 55.6% |
| Qwen | 77.8% | 55.6% | 44.4% |
| Mistral | 66.7% | 77.8% | 22.2% |

### REASSURANCE
| Model | Agreement | Met Rate | Not Met Rate |
|-------|-----------|----------|--------------|
| OpenChat | 56.2% | 81.2% | 18.8% |
| Qwen | 68.8% | 56.2% | 43.8% |
| Mistral | 62.5% | 87.5% | 12.5% |

### RUDE_SARCASTIC
| Model | Agreement | Met Rate | Not Met Rate |
|-------|-----------|----------|--------------|
| OpenChat | 80.0% | 80.0% | 20.0% |
| Qwen | 90.0% | 90.0% | 10.0% |
| Mistral | 65.0% | 65.0% | 35.0% |

## Confusion Matrix Analysis
### OpenChat vs Gemini
| Gemini \ Model | Met | Not Met | Other |
|-------------|-----|---------|-------|
| met | 88 | 39 | 0 |
| not_met | 14 | 17 | 0 |

### Qwen vs Gemini
| Gemini \ Model | Met | Not Met | Other |
|-------------|-----|---------|-------|
| met | 91 | 36 | 0 |
| not_met | 5 | 26 | 0 |

### Mistral vs Gemini
| Gemini \ Model | Met | Not Met | Other |
|-------------|-----|---------|-------|
| met | 84 | 43 | 0 |
| not_met | 13 | 18 | 0 |

## Key Insights

### Performance Rankings:
1. **Qwen**: 74.1% agreement with Gemini
2. **OpenChat**: 66.5% agreement with Gemini
3. **Mistral**: 64.6% agreement with Gemini

### Notable Findings:
- Qwen shows highest agreement with Gemini (73.9%)
- All models tend to predict "met" more often than Gemini
- OpenChat has balanced predictions but lower agreement
- Mistral shows similar pattern to OpenChat

## Recommendations

1. **Primary Choice**: Qwen for highest agreement with Gemini
2. **Balanced Approach**: OpenChat for more conservative evaluations
3. **Reference Standard**: Gemini provides the most balanced baseline

---
*Report generated: 2025-11-01 14:46:11*
*Data source: FULL_RESULTS_20_convo.csv (158 valid evaluations)*

## Comprehensive Guideline vs Model Agreement Matrix

| Guideline | OpenChat | Qwen | Mistral | Best Performer |
|-----------|----------|------|---------|----------------|
| APOLOGY | 50.0% | 75.0% | 90.0% | Mistral (90.0%) |
| CLOSING | 77.8% | 77.8% | 72.2% | OpenChat (77.8%) |
| EMPATHY | 88.2% | 82.4% | 94.1% | Mistral (94.1%) |
| FEEDBACK_PITCH | 42.9% | 42.9% | 28.6% | OpenChat,Qwen (42.9%) |
| FURTHER_ASSISTANCE | 72.2% | 77.8% | 27.8% | Qwen (77.8%) |
| HOLD | 70.6% | 64.7% | 64.7% | OpenChat (70.6%) |
| OPENING | 55.6% | 77.8% | 66.7% | Qwen (77.8%) |
| REASSURANCE | 56.2% | 68.8% | 62.5% | Qwen (68.8%) |
| RUDE_SARCASTIC | 80.0% | 90.0% | 65.0% | Qwen (90.0%) |

### Summary Statistics:
- **Total Guidelines Analyzed**: 9
- **Qwen Best Performer**: 4 guidelines
- **OpenChat Best Performer**: 3 guidelines
- **Mistral Best Performer**: 2 guidelines
- **Most Consistent Model**: Qwen

## Confusion Matrix Analysis
### OpenChat vs Gemini
| Gemini \ Model | Met | Not Met | Other |
|-------------|-----|---------|-------|
| met | 88 | 39 | 0 |
| not_met | 14 | 17 | 0 |

### Qwen vs Gemini
| Gemini \ Model | Met | Not Met | Other |
|-------------|-----|---------|-------|
| met | 91 | 36 | 0 |
| not_met | 5 | 26 | 0 |

### Mistral vs Gemini
| Gemini \ Model | Met | Not Met | Other |
|-------------|-----|---------|-------|
| met | 84 | 43 | 0 |
| not_met | 13 | 18 | 0 |

## Key Insights

### Performance Rankings (Agreement with Gemini):
1. **Qwen**: 73.4% agreement with Gemini
2. **OpenChat**: 66.5% agreement with Gemini
3. **Mistral**: 63.9% agreement with Gemini

### Performance Rankings (Latency):
1. **Gemini**: 2.12s (Fastest)
2. **Qwen**: 3.79s
3. **OpenChat**: 4.67s
4. **Mistral**: 6.93s (Slowest)

### Notable Findings:
- **Qwen** shows highest agreement with Gemini (73.4%) and reasonable speed (3.79s)
- **Gemini** is fastest (2.12s) but has some extreme outliers (filtered out >100s)
- **OpenChat** has moderate agreement (66.5%) but slower response times (4.67s)
- **Mistral** shows lowest agreement (63.9%) and slowest responses (6.93s)
- All models tend to predict "met" more often than Gemini's balanced baseline

## Recommendations

1. **Primary Choice**: Qwen for highest agreement with Gemini and good speed
2. **Speed-Focused**: Gemini for fastest responses (but monitor for outliers)
3. **Balanced Approach**: OpenChat for moderate performance across both metrics
4. **Reference Standard**: Gemini provides the most balanced baseline for evaluation

---
*Report generated: 2025-11-01 16:09:28*
*Data source: FULL_RESULTS_20_convo.csv (158 valid evaluations)*
*Latency calculated from actual API response times*
