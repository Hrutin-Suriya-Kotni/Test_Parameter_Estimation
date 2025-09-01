import pandas as pd
import os
from typing import Tuple, Optional
from config import (
    CRED_DATA_PATH, 
    CRED_FILE_NAME, 
    CRED_TRANSCRIPT_SHEET, 
    CRED_PRIMARY_INFO_SHEET
)

class CREDDataLoader:
    """Handles loading and processing CRED conversation data"""
    
    def __init__(self, data_path: str = CRED_DATA_PATH):
        self.data_path = data_path
        self.file_path = os.path.join(data_path, CRED_FILE_NAME)
        print(f"🔍 Data loader initialized with:")
        print(f"   Data path: {self.data_path}")
        print(f"   File path: {self.file_path}")
        print(f"   File exists: {os.path.exists(self.file_path)}")
    
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load the CRED conversation data from Excel file
        
        Returns:
            Tuple of (transcript_df, primary_info_df)
        """
        try:
            # Load transcript data
            transcript_df = pd.read_excel(
                self.file_path, 
                sheet_name=CRED_TRANSCRIPT_SHEET
            )
            
            # Load primary info data
            primary_info_df = pd.read_excel(
                self.file_path, 
                sheet_name=CRED_PRIMARY_INFO_SHEET
            )
            
            print(f"Loaded transcript data: {len(transcript_df)} rows")
            print(f"Loaded primary info data: {len(primary_info_df)} rows")
            print(f"Transcript columns: {list(transcript_df.columns)}")
            
            return transcript_df, primary_info_df
            
        except FileNotFoundError:
            print(f"Error: File not found at {self.file_path}")
            print(f"Please ensure the Excel file is in the {self.data_path} directory")
            raise
        except Exception as e:
            print(f"Error loading data: {e}")
            raise
    
    def remove_short_calls(self, df: pd.DataFrame, primary_info: pd.DataFrame, 
                          min_duration: int = 120) -> pd.DataFrame:
        """
        Remove calls shorter than the specified duration
        
        Args:
            df: Transcript dataframe
            primary_info: Primary info dataframe
            min_duration: Minimum call duration in seconds
            
        Returns:
            Filtered dataframe
        """
        # Rename column for consistency
        primary_info_renamed = primary_info.copy()
        primary_info_renamed.rename(columns={'Request_id': 'request_id'}, inplace=True)
        
        # Merge dataframes
        merge_df = pd.merge(
            df, 
            primary_info_renamed[['request_id', 'Time_duration_of_Call']], 
            on='request_id'
        )
        
        # Filter by duration
        filtered_df = merge_df[merge_df['Time_duration_of_Call'] >= min_duration]
        filtered_df = filtered_df.drop(columns=['request_id'])
        
        print(f"Filtered to {len(filtered_df)} calls with duration >= {min_duration} seconds")
        return filtered_df
    
    def get_sample_data(self, df: pd.DataFrame, sample_size: int = 5) -> pd.DataFrame:
        """
        Get a sample of the data for testing
        
        Args:
            df: Full dataframe
            sample_size: Number of samples to return
            
        Returns:
            Sample dataframe
        """
        return df.head(sample_size)

# Global data loader instance
data_loader = CREDDataLoader()

def load_conversations(sample_size: int = None):
    """
    Load conversations for testing purposes
    
    Args:
        sample_size: Number of conversations to load (None = load all)
        
    Returns:
        List of conversation dictionaries with 'id' and 'transcript' keys
    """
    try:
        # Load the data
        transcript_df, primary_info_df = data_loader.load_data()
        
        # Get data (all or sample)
        if sample_size is None:
            # Load ALL conversations
            data_df = transcript_df
            print(f"Loading ALL {len(data_df)} conversations from the dataset")
        else:
            # Load sample
            data_df = data_loader.get_sample_data(transcript_df, sample_size)
            print(f"Loading sample of {len(data_df)} conversations")
        
        conversations = []
        for idx, row in data_df.iterrows():
            # Get the transcript text (assuming there's a 'transcript' column)
            transcript_text = row.get('transcript', str(row.get('Transcript', '')))
            
            # Skip empty transcripts
            if transcript_text and str(transcript_text).strip():
                conversations.append({
                    'id': f"conv_{idx+1}",
                    'transcript': str(transcript_text).strip()
                })
        
        print(f"Successfully loaded {len(conversations)} conversations for testing")
        return conversations
        
    except Exception as e:
        print(f"Error loading conversations: {e}")
        print("Returning sample conversation for testing...")
        # Return some dummy data for testing
        return [
            {
                'id': 'conv_1',
                'transcript': 'Hello, this is a test conversation transcript for testing purposes.'
            }
        ]

def load_all_conversations():
    """
    Load ALL conversations from the dataset
    
    Returns:
        List of all conversation dictionaries with 'id' and 'transcript' keys
    """
    return load_conversations(sample_size=None) 