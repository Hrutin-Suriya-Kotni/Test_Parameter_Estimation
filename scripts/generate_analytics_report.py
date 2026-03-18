import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# Configuration
OUTPUT_DIR = "20_testing_type2b/Human_Evaluation/REPORTS"
MODEL_MAPPING = {
    'LLM1': 'OpenChat 3.5',
    'LLM2': 'Qwen 2.5',
    'LLM3': 'Cred-Finetune-Mistral',
    'gemini': 'Gemini 2.0 Flash'
}

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

def generate_graphs(results_df, details_df):
    ensure_output_dir()
    # Set style
    plt.style.use('ggplot')
    
    # --- 1. Overall Performance Graph ---
    fig, ax = plt.subplots(figsize=(12, 7))
    
    models = results_df['Model']
    x = np.arange(len(models))
    width = 0.35
    
    rects1 = ax.bar(x - width/2, results_df['Evidence Correctness (%)'], width, label='Correctness (%)', color='#4CAF50')
    rects2 = ax.bar(x + width/2, results_df['Hallucination Rate (%)'], width, label='Hallucination Rate (%)', color='#F44336')
    
    ax.set_ylabel('Percentage')
    ax.set_title('Overall Model Performance: Correctness vs Hallucination')
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=15)
    ax.legend()
    
    # Add value labels
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    
    plt.tight_layout()
    save_path = os.path.join(OUTPUT_DIR, 'overall_performance.png')
    plt.savefig(save_path)
    print(f"Graph saved: {save_path}")
    plt.close()

    # --- 2. Per-Guideline Comparison Graphs ---
    if not details_df.empty:
        guidelines = details_df['Guideline'].unique()
        
        for guideline in guidelines:
            # Filter data for this guideline
            g_data = details_df[details_df['Guideline'] == guideline].copy()
            
            # Ensure consistent order of models
            # We can sort by correctness to make the chart look nice, or keep consistent model order
            # Let's sort by correctness descending
            g_data = g_data.sort_values('Evidence Correctness (%)', ascending=True) # Ascending for barh (bottom to top)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Create horizontal bar chart
            y_pos = np.arange(len(g_data['Model']))
            
            # Color gemini distinctly? Optional. Let's stick to standard blue for all, maybe highlight 'Gemini 2.0 Flash'
            colors = ['#2196F3' if m == 'Gemini 2.0 Flash' else '#9E9E9E' for m in g_data['Model']]
            
            bars = ax.barh(y_pos, g_data['Evidence Correctness (%)'], align='center', color=colors)
            ax.set_yticks(y_pos)
            ax.set_yticklabels(g_data['Model'])
            ax.set_xlabel('Correctness (%)')
            ax.set_title(f'Performance Comparison: {guideline.replace("_", " ").title()}')
            ax.set_xlim(0, 105) # Allow space for labels
            
            # Add values to bars
            for i, v in enumerate(g_data['Evidence Correctness (%)']):
                ax.text(v + 1, i, f"{v}%", color='black', va='center', fontweight='bold')
            
            plt.tight_layout()
            # Clean filename
            safe_name = guideline.replace(" ", "_").replace("/", "-")
            save_path = os.path.join(OUTPUT_DIR, f'performance_{safe_name}.png')
            plt.savefig(save_path)
            print(f"Graph saved: {save_path}")
            plt.close()

def generate_analytics(file_path):
    print(f"Processing file: {file_path}")
    ensure_output_dir()
    
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return

    models = ['LLM1', 'LLM2', 'LLM3', 'gemini']
    
    analytics_data = []
    guideline_analytics = []

    # --- Metrics Calculation ---
    # We first calculate using raw model keys (LLM1, etc) then map names for output results only
    
    # 1. Overall Aggregation
    for raw_model in models:
        # Define column names based on raw inputs
        evidence_col = f'Evidence of {raw_model}' if raw_model != 'gemini' else 'Evidence of Gemini'
        hallucination_col = f'Did {raw_model} hallucinated and provided evidence( yes/no)?'
        if raw_model == 'LLM2':
             hallucination_col = 'DId LLM2 hallucinated and provided evidence( yes/no)'
        elif raw_model == 'gemini':
             hallucination_col = 'Did gemini hallucinated and provided evidence( yes/no)?'
        
        if evidence_col not in df.columns or hallucination_col not in df.columns:
            print(f"Warning: Columns for {raw_model} not found.")
            continue
            
        # Calc
        total_evidence = df[evidence_col].notna().sum()
        correct_evidence = df[df[evidence_col].str.lower().str.strip() == 'correct'].shape[0]
        percent_correct = (correct_evidence / total_evidence * 100) if total_evidence > 0 else 0
        
        total_hallucination_entries = df[hallucination_col].notna().sum()
        hallucination_count = df[df[hallucination_col].str.lower().str.strip() == 'yes'].shape[0]
        percent_hallucination = (hallucination_count / total_hallucination_entries * 100) if total_hallucination_entries > 0 else 0

        # Store with MAPPED NAME
        display_name = MODEL_MAPPING.get(raw_model, raw_model)
        
        analytics_data.append({
            'Model': display_name,
            'Evidence Correctness (%)': round(percent_correct, 2),
            'Hallucination Rate (%)': round(percent_hallucination, 2),
            'Total Validation Samples': total_evidence
        })

    # 2. Per Guideline Aggregation
    if 'guideline' in df.columns:
        guidelines = df['guideline'].unique()
        for guideline in guidelines:
            g_df = df[df['guideline'] == guideline]
            for raw_model in models:
                evidence_col = f'Evidence of {raw_model}' if raw_model != 'gemini' else 'Evidence of Gemini'
                hallucination_col = f'Did {raw_model} hallucinated and provided evidence( yes/no)?'
                
                if raw_model == 'LLM2':
                     hallucination_col = 'DId LLM2 hallucinated and provided evidence( yes/no)'
                elif raw_model == 'gemini':
                     hallucination_col = 'Did gemini hallucinated and provided evidence( yes/no)?'

                if evidence_col not in df.columns: continue

                total_ev = g_df[evidence_col].notna().sum()
                correct_ev = g_df[g_df[evidence_col].str.lower().str.strip() == 'correct'].shape[0]
                pct_correct = (correct_ev / total_ev * 100) if total_ev > 0 else 0
                
                total_hal = g_df[hallucination_col].notna().sum()
                hal_count = g_df[g_df[hallucination_col].str.lower().str.strip() == 'yes'].shape[0]
                pct_hal = (hal_count / total_hal * 100) if total_hal > 0 else 0
                
                display_name = MODEL_MAPPING.get(raw_model, raw_model)
                
                guideline_analytics.append({
                    'Guideline': guideline,
                    'Model': display_name,
                    'Evidence Correctness (%)': round(pct_correct, 2),
                    'Hallucination Rate (%)': round(pct_hal, 2),
                    'Total Samples': total_ev
                })
    
    # Create DataFrames
    results_df = pd.DataFrame(analytics_data)
    details_df = pd.DataFrame(guideline_analytics)
    
    # Save CSVs to REPORTS
    results_df.to_csv(os.path.join(OUTPUT_DIR, 'analytics_report.csv'), index=False)
    details_df.to_csv(os.path.join(OUTPUT_DIR, 'each_model_details.csv'), index=False)
    print("CSVs saved.")

    # Generate Markdown Report
    output_md = os.path.join(OUTPUT_DIR, 'analytics_report.md')
    with open(output_md, 'w') as f:
        f.write("# Analytics Report\n\n")
        f.write("## Overall Performance\n")
        if not results_df.empty:
            cols = results_df.columns
            f.write("| " + " | ".join(cols) + " |\n")
            f.write("|" + "|".join(["---"] * len(cols)) + "|\n")
            for _, row in results_df.iterrows():
                f.write("| " + " | ".join(str(row[c]) for c in cols) + " |\n")
        f.write("\n\n")
    print(f"Markdown report saved: {output_md}")
    
    print("\n--- Report Preview ---")
    print(results_df)

    # Generate Graphs
    try:
        generate_graphs(results_df, details_df)
    except Exception as e:
        print(f"Error generating graphs: {e}")

if __name__ == "__main__":
    # Path to the validated CSV
    csv_path = "20_testing_type2b/Human_Evaluation/FULL_RESULTS_20_convo_Validated.csv"
    if not os.path.exists(csv_path):
        csv_path = "/Users/cleveres_tidiot/Documents/Vocab_AI/Parameter_Testing/" + csv_path
    generate_analytics(csv_path)

if __name__ == "__main__":
    # Path to the validated CSV
    csv_path = "20_testing_type2b/Human_Evaluation/FULL_RESULTS_20_convo_Validated.csv"
    
    # Adjust path if script is run from a different directory, assumes running from 'Parameter_Testing' root or similar
    if not os.path.exists(csv_path):
        # Try absolute path based on previous context if relative fails
        csv_path = "/Users/cleveres_tidiot/Documents/Vocab_AI/Parameter_Testing/" + csv_path
        
    generate_analytics(csv_path)
