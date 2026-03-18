#!/usr/bin/env python3
"""
Comprehensive BERTScore Analysis Report
Generates statistical analysis and per-guideline breakdowns for model comparisons.
"""

import pandas as pd
import numpy as np
from scipy import stats
import os
from collections import Counter

def calculate_statistics(scores):
    """Calculate comprehensive statistics for a set of scores."""
    if len(scores) == 0 or scores.isna().all():
        return {
            'count': 0,
            'mean': np.nan,
            'median': np.nan,
            'mode': np.nan,
            'std': np.nan,
            'min': np.nan,
            'max': np.nan,
            'q25': np.nan,
            'q75': np.nan,
            'iqr': np.nan,
            'outliers_low': [],
            'outliers_high': []
        }

    clean_scores = scores.dropna()

    # Basic statistics
    mean_val = clean_scores.mean()
    median_val = clean_scores.median()
    std_val = clean_scores.std()

    # Mode (most frequent value, rounded to 4 decimals)
    rounded_scores = clean_scores.round(4)
    mode_counts = Counter(rounded_scores)
    mode_val = mode_counts.most_common(1)[0][0] if mode_counts else np.nan

    # Quartiles and IQR
    q25 = clean_scores.quantile(0.25)
    q75 = clean_scores.quantile(0.75)
    iqr = q75 - q25

    # Outlier detection using IQR method
    lower_bound = q25 - 1.5 * iqr
    upper_bound = q75 + 1.5 * iqr

    outliers_low = clean_scores[clean_scores < lower_bound].tolist()
    outliers_high = clean_scores[clean_scores > upper_bound].tolist()

    return {
        'count': len(clean_scores),
        'mean': round(mean_val, 4),
        'median': round(median_val, 4),
        'mode': round(mode_val, 4),
        'std': round(std_val, 4),
        'min': round(clean_scores.min(), 4),
        'max': round(clean_scores.max(), 4),
        'q25': round(q25, 4),
        'q75': round(q75, 4),
        'iqr': round(iqr, 4),
        'outliers_low': outliers_low,
        'outliers_high': outliers_high
    }

def generate_guideline_analysis(df, model_name):
    """Generate per-guideline analysis for a model."""
    guidelines = df['guideline'].unique()
    guideline_stats = []

    for guideline in sorted(guidelines):
        guideline_data = df[df['guideline'] == guideline]
        f1_scores = guideline_data['bertscore_f1']

        stats_result = calculate_statistics(f1_scores)

        # Agreement analysis for this guideline
        agreement_count = len(guideline_data[guideline_data['agreement'] == 'agreement'])
        disagreement_count = len(guideline_data[guideline_data['agreement'] == 'disagreement'])
        total_count = len(guideline_data)

        guideline_stats.append({
            'guideline': guideline,
            'count': total_count,
            'agreement_rate': round(agreement_count / total_count * 100, 1) if total_count > 0 else 0,
            'mean_f1': stats_result['mean'],
            'median_f1': stats_result['median'],
            'std_f1': stats_result['std'],
            'min_f1': stats_result['min'],
            'max_f1': stats_result['max'],
            'outliers_count': len(stats_result['outliers_low']) + len(stats_result['outliers_high'])
        })

    return pd.DataFrame(guideline_stats)

def main():
    # Model configurations
    models = [
        ('OpenChat', 'bertscore_openchat_vs_gemini.csv'),
        ('Qwen', 'bertscore_qwen_vs_gemini.csv'),
        ('Mistral', 'bertscore_mistral_vs_gemini.csv')
    ]

    # Load all dataframes
    model_dataframes = {}
    overall_stats = []

    print("BERTScore Comprehensive Analysis Report")
    print("=" * 60)

    for model_name, filename in models:
        filepath = f'20_testing_type2b/results/{filename}'
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            model_dataframes[model_name] = df

            # Calculate overall statistics
            f1_scores = df['bertscore_f1']
            stats_result = calculate_statistics(f1_scores)

            # Agreement statistics
            agreement_count = len(df[df['agreement'] == 'agreement'])
            disagreement_count = len(df[df['agreement'] == 'disagreement'])
            total_count = len(df)

            overall_stats.append({
                'model': model_name,
                'total_comparisons': total_count,
                'agreement_count': agreement_count,
                'agreement_rate': round(agreement_count / total_count * 100, 1),
                'disagreement_count': disagreement_count,
                'disagreement_rate': round(disagreement_count / total_count * 100, 1),
                **stats_result
            })

            print(f"\n{model_name} vs Gemini - Overall Statistics:")
            print("-" * 40)
            print(f"Total comparisons: {total_count}")
            print(f"Agreement: {agreement_count} ({agreement_count/total_count*100:.1f}%)")
            print(f"BERTScore F1 - Mean: {stats_result['mean']}, Median: {stats_result['median']}, Std: {stats_result['std']}")
            print(f"Range: {stats_result['min']} - {stats_result['max']}")
            print(f"Outliers: {len(stats_result['outliers_low'])} low, {len(stats_result['outliers_high'])} high")

    # Create overall comparison table
    overall_df = pd.DataFrame(overall_stats)
    print("\nOVERALL MODEL COMPARISON:")
    print("=" * 100)
    comparison_table = overall_df[['model', 'agreement_rate', 'mean', 'median', 'std', 'min', 'max', 'count']].copy()
    comparison_table.columns = ['Model', 'Agreement %', 'Mean F1', 'Median F1', 'Std F1', 'Min F1', 'Max F1', 'Count']
    print(comparison_table.to_string(index=False))

    # Generate per-guideline analysis
    print("\nPER-GUIDELINE ANALYSIS:")
    print("=" * 100)

    guideline_summaries = []
    for model_name, df in model_dataframes.items():
        guideline_df = generate_guideline_analysis(df, model_name)
        guideline_df['model'] = model_name
        guideline_summaries.append(guideline_df)

        print(f"\n{model_name} - Per-Guideline BERTScore Analysis:")
        print("-" * 50)
        display_cols = ['guideline', 'count', 'agreement_rate', 'mean_f1', 'median_f1', 'min_f1', 'max_f1', 'outliers_count']
        display_df = guideline_df[display_cols].copy()
        display_df.columns = ['Guideline', 'Count', 'Agreement %', 'Mean F1', 'Median F1', 'Min F1', 'Max F1', 'Outliers']
        print(display_df.to_string(index=False))

    # Create comprehensive report CSV
    all_guideline_data = pd.concat(guideline_summaries, ignore_index=True)
    all_guideline_data.to_csv('20_testing_type2b/results/bertscore_comprehensive_report.csv', index=False)

    # Summary insights
    print("\nKEY INSIGHTS:")
    print("=" * 50)

    # Best performing model
    best_agreement = overall_df.loc[overall_df['agreement_rate'].idxmax(), 'model']
    best_similarity = overall_df.loc[overall_df['mean'].idxmax(), 'model']

    print(f"1. Highest agreement with Gemini: {best_agreement} ({overall_df['agreement_rate'].max():.1f}%)")
    print(f"2. Highest semantic similarity: {best_similarity} (F1: {overall_df['mean'].max():.4f})")

    # Most consistent model (lowest standard deviation)
    most_consistent = overall_df.loc[overall_df['std'].idxmin(), 'model']
    print(f"3. Most consistent performance: {most_consistent} (Std: {overall_df['std'].min():.4f})")

    # Guidelines with highest/lowest agreement across all models
    combined_guideline_data = all_guideline_data.groupby('guideline').agg({
        'agreement_rate': 'mean',
        'mean_f1': 'mean',
        'count': 'sum'
    }).round(2)

    highest_agreement_guideline = combined_guideline_data['agreement_rate'].idxmax()
    lowest_agreement_guideline = combined_guideline_data['agreement_rate'].idxmin()

    print(f"4. Most agreed-upon guideline: {highest_agreement_guideline} ({combined_guideline_data['agreement_rate'].max():.1f}% avg agreement)")
    print(f"5. Least agreed-upon guideline: {lowest_agreement_guideline} ({combined_guideline_data['agreement_rate'].min():.1f}% avg agreement)")

    print("\nReport saved to: 20_testing_type2b/results/bertscore_comprehensive_report.csv")
if __name__ == "__main__":
    main()
