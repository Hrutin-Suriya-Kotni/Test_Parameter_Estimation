#!/usr/bin/env python3
"""
BERTScore Evidence Comparison Script
Compares evidence text from different models using BERTScore to measure semantic similarity.
"""

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

class BERTScoreComparator:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """Initialize with SentenceTransformer model for BERTScore computation."""
        print(f"Loading model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("Model loaded successfully!")

    def calculate_bertscore(self, text1, text2):
        """
        Calculate BERTScore between two texts.
        Returns precision, recall, and F1 score.
        """
        if not text1 or not text2 or pd.isna(text1) or pd.isna(text2):
            return {'precision': np.nan, 'recall': np.nan, 'f1': np.nan}

        # Tokenize and encode both texts
        tokens1 = self.model.tokenizer.tokenize(text1)
        tokens2 = self.model.tokenizer.tokenize(text2)

        # Get embeddings for each token
        embeddings1 = self.model.encode(tokens1, convert_to_tensor=True)
        embeddings2 = self.model.encode(tokens2, convert_to_tensor=True)

        # Calculate similarity matrix
        similarity_matrix = util.cos_sim(embeddings1, embeddings2)

        # Convert to numpy for easier processing
        sim_matrix = similarity_matrix.cpu().numpy()

        # Calculate Precision: for each token in text2, find best match in text1
        precision_scores = []
        for i in range(len(tokens2)):
            best_sim = np.max(sim_matrix[:, i]) if sim_matrix.shape[0] > 0 else 0
            precision_scores.append(best_sim)
        precision = np.mean(precision_scores) if precision_scores else 0

        # Calculate Recall: for each token in text1, find best match in text2
        recall_scores = []
        for i in range(len(tokens1)):
            best_sim = np.max(sim_matrix[i, :]) if sim_matrix.shape[1] > 0 else 0
            recall_scores.append(best_sim)
        recall = np.mean(recall_scores) if recall_scores else 0

        # F1 Score
        if precision + recall == 0:
            f1 = 0
        else:
            f1 = 2 * (precision * recall) / (precision + recall)

        return {
            'precision': round(float(precision), 4),
            'recall': round(float(recall), 4),
            'f1': round(float(f1), 4)
        }

    def determine_agreement(self, status1, status2):
        """
        Determine if two models agree on the status.
        Agreement = both 'met' or both 'not met' (case insensitive)
        """
        if pd.isna(status1) or pd.isna(status2):
            return 'not_applicable'

        status1_clean = str(status1).strip().lower()
        status2_clean = str(status2).strip().lower()

        if status1_clean == status2_clean:
            return 'agreement'
        else:
            return 'disagreement'

def main():
    # Model mappings
    MODEL_MAPPING = {
        'LLM1': 'OpenChat',
        'LLM2': 'Qwen',
        'LLM3': 'Mistral'
    }

    # Initialize BERTScore comparator
    comparator = BERTScoreComparator()

    # Read the full results
    print("Reading FULL_RESULTS_20_convo.csv...")
    df = pd.read_csv('20_testing_type2b/results/FULL_RESULTS_20_convo.csv')
    print(f"Loaded {len(df)} rows")

    # Process each model comparison
    for llm_key, model_name in MODEL_MAPPING.items():
        print(f"\nProcessing {model_name} vs Gemini comparison...")

        # Create comparison dataframe
        comparison_data = []

        for idx, row in df.iterrows():
            if idx % 50 == 0:
                print(f"Processing row {idx}/{len(df)}")

            # Get evidence texts
            model_evidence = row.get(f'{llm_key}_evidence', '')
            gemini_evidence = row.get('gemini_evidence', '')

            # Get statuses
            model_status = row.get(f'{llm_key}_status', '')
            gemini_status = row.get('gemini_status', '')

            # Calculate BERTScore
            bertscore_result = comparator.calculate_bertscore(model_evidence, gemini_evidence)

            # Determine agreement
            agreement = comparator.determine_agreement(model_status, gemini_status)

            # Prepare row data
            row_data = {
                'conversation_id': row.get('conversation_id', ''),
                'guideline': row.get('guideline', ''),
                f'{model_name.lower()}_status': model_status,
                f'{model_name.lower()}_evidence': model_evidence,
                'gemini_status': gemini_status,
                'gemini_evidence': gemini_evidence,
                'agreement': agreement,
                'bertscore_precision': bertscore_result['precision'],
                'bertscore_recall': bertscore_result['recall'],
                'bertscore_f1': bertscore_result['f1']
            }

            comparison_data.append(row_data)

        # Create dataframe and save
        comparison_df = pd.DataFrame(comparison_data)
        output_filename = f'20_testing_type2b/results/bertscore_{model_name.lower()}_vs_gemini.csv'
        comparison_df.to_csv(output_filename, index=False)

        # Summary statistics
        valid_scores = comparison_df.dropna(subset=['bertscore_f1'])
        agreement_count = len(comparison_df[comparison_df['agreement'] == 'agreement'])
        disagreement_count = len(comparison_df[comparison_df['agreement'] == 'disagreement'])
        not_applicable_count = len(comparison_df[comparison_df['agreement'] == 'not_applicable'])

        print(f"  Saved {len(comparison_df)} comparisons to {output_filename}")
        print(f"  Agreement: {agreement_count} rows")
        print(f"  Disagreement: {disagreement_count} rows")
        print(f"  Not Applicable: {not_applicable_count} rows")
        print(f"  Average BERTScore F1: {valid_scores['bertscore_f1'].mean():.4f}")

if __name__ == "__main__":
    main()
