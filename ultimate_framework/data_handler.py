"""
Ultimate Data Handler - Loads and processes all 3 data types
"""

import pandas as pd
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class DataHandler:
    """Handles loading and processing of all three data types"""
    
    def __init__(self, data_base_path: str = "./data"):
        self.base_path = Path(data_base_path)
        logger.info(f"DataHandler initialized with base path: {self.base_path}")
    
    def load_type1(self, filename: str = "type1_overall_paragraph.csv") -> List[Dict[str, Any]]:
        """
        Load Type1 data: Overall paragraph format
        
        Returns:
            List of dicts with keys: conversation_id, transcript
        """
        file_path = self.base_path / filename
        logger.info(f"Loading Type1 data from: {file_path}")
        
        try:
            df = pd.read_csv(file_path)
            conversations = []
            
            for _, row in df.iterrows():
                conversations.append({
                    'conversation_id': row['conversation_id'],
                    'transcript': row['transcript'],
                    'data_type': 'type1'
                })
            
            logger.info(f"Loaded {len(conversations)} Type1 conversations")
            return conversations
            
        except Exception as e:
            logger.error(f"Error loading Type1 data: {e}")
            raise
    
    def load_type2a(self, directory: str = "type2a_json") -> List[Dict[str, Any]]:
        """
        Load Type2a data: JSON structured format with turns
        
        Returns:
            List of dicts with keys: conversation_id, turns, transcript (reconstructed)
        """
        dir_path = self.base_path / directory
        logger.info(f"Loading Type2a data from: {dir_path}")
        
        try:
            conversations = []
            json_files = list(dir_path.glob("*.json"))
            
            for json_file in json_files:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Reconstruct transcript from turns
                transcript = self._reconstruct_transcript_from_turns(data['turns'])
                
                conversations.append({
                    'conversation_id': data['conversation_id'],
                    'turns': data['turns'],
                    'transcript': transcript,
                    'data_type': 'type2a'
                })
            
            logger.info(f"Loaded {len(conversations)} Type2a conversations")
            return conversations
            
        except Exception as e:
            logger.error(f"Error loading Type2a data: {e}")
            raise
    
    def load_type2b(self, filename: str = "type2b_labeled_paragraph.csv") -> List[Dict[str, Any]]:
        """
        Load Type2b data: Labeled paragraph format
        
        Returns:
            List of dicts with keys: conversation_id, transcript
        """
        file_path = self.base_path / filename
        logger.info(f"Loading Type2b data from: {file_path}")
        
        try:
            df = pd.read_csv(file_path)
            conversations = []
            
            for _, row in df.iterrows():
                conversations.append({
                    'conversation_id': row['conversation_id'],
                    'transcript': row['labeled_transcript'],
                    'data_type': 'type2b'
                })
            
            logger.info(f"Loaded {len(conversations)} Type2b conversations")
            return conversations
            
        except Exception as e:
            logger.error(f"Error loading Type2b data: {e}")
            raise
    
    def load_all_types(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load all three data types
        
        Returns:
            Dict with keys: type1, type2a, type2b
        """
        logger.info("Loading all data types...")
        
        return {
            'type1': self.load_type1(),
            'type2a': self.load_type2a(),
            'type2b': self.load_type2b()
        }
    
    def load_specific_type(self, data_type: str) -> List[Dict[str, Any]]:
        """
        Load a specific data type
        
        Args:
            data_type: One of 'type1', 'type2a', 'type2b'
        
        Returns:
            List of conversation dicts
        """
        if data_type == 'type1':
            return self.load_type1()
        elif data_type == 'type2a':
            return self.load_type2a()
        elif data_type == 'type2b':
            return self.load_type2b()
        else:
            raise ValueError(f"Unknown data type: {data_type}. Must be one of: type1, type2a, type2b")
    
    @staticmethod
    def _reconstruct_transcript_from_turns(turns: List[Dict]) -> str:
        """
        Reconstruct a full transcript from turn-by-turn data
        
        Args:
            turns: List of turn dicts with speaker and text
        
        Returns:
            Reconstructed transcript as a single string
        """
        transcript_parts = []
        for turn in turns:
            speaker = turn.get('speaker', 'unknown')
            text = turn.get('text', '')
            transcript_parts.append(f"{speaker}: {text}")
        
        return " ".join(transcript_parts)
    
    def get_dataset_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the datasets
        
        Returns:
            Dict with stats for each data type
        """
        stats = {}
        
        try:
            type1_data = self.load_type1()
            stats['type1'] = {
                'count': len(type1_data),
                'avg_length': sum(len(c['transcript']) for c in type1_data) / len(type1_data),
                'max_length': max(len(c['transcript']) for c in type1_data),
                'min_length': min(len(c['transcript']) for c in type1_data)
            }
        except Exception as e:
            logger.warning(f"Could not load Type1 stats: {e}")
            stats['type1'] = {'error': str(e)}
        
        try:
            type2a_data = self.load_type2a()
            stats['type2a'] = {
                'count': len(type2a_data),
                'avg_length': sum(len(c['transcript']) for c in type2a_data) / len(type2a_data),
                'max_length': max(len(c['transcript']) for c in type2a_data),
                'min_length': min(len(c['transcript']) for c in type2a_data),
                'avg_turns': sum(len(c['turns']) for c in type2a_data) / len(type2a_data)
            }
        except Exception as e:
            logger.warning(f"Could not load Type2a stats: {e}")
            stats['type2a'] = {'error': str(e)}
        
        try:
            type2b_data = self.load_type2b()
            stats['type2b'] = {
                'count': len(type2b_data),
                'avg_length': sum(len(c['transcript']) for c in type2b_data) / len(type2b_data),
                'max_length': max(len(c['transcript']) for c in type2b_data),
                'min_length': min(len(c['transcript']) for c in type2b_data)
            }
        except Exception as e:
            logger.warning(f"Could not load Type2b stats: {e}")
            stats['type2b'] = {'error': str(e)}
        
        return stats


if __name__ == "__main__":
    # Test the data handler
    logging.basicConfig(level=logging.INFO)
    
    handler = DataHandler()
    
    print("\n=== Dataset Statistics ===")
    stats = handler.get_dataset_stats()
    for data_type, type_stats in stats.items():
        print(f"\n{data_type.upper()}:")
        for key, value in type_stats.items():
            print(f"  {key}: {value}")
    
    print("\n=== Testing Data Loading ===")
    print(f"Type1 conversations: {len(handler.load_type1())}")
    print(f"Type2a conversations: {len(handler.load_type2a())}")
    print(f"Type2b conversations: {len(handler.load_type2b())}")

