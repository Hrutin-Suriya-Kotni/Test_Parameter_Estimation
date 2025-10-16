#!/usr/bin/env python3
"""
Data loader for MISTRAL_BOOM_BOOM project
Handles 3 types of data: type1, type2a, type2b
"""

import pandas as pd
import json
import os
from typing import List, Dict, Any, Tuple


class BoomBoomDataLoader:
    """Loads and processes data for MISTRAL_BOOM_BOOM project"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize data loader
        
        Args:
            data_dir: Directory containing data files
        """
        self.data_dir = data_dir
        self.type1_file = os.path.join(data_dir, "type1_overall_paragraph.csv")
        self.type2a_dir = os.path.join(data_dir, "type2a_json")
        self.type2b_file = os.path.join(data_dir, "type2b_labeled_paragraph.csv")
        
        print(f"📁 BOOM BOOM Data Loader initialized")
        print(f"   Type1 file: {self.type1_file} (exists: {os.path.exists(self.type1_file)})")
        print(f"   Type2a dir: {self.type2a_dir} (exists: {os.path.exists(self.type2a_dir)})")
        print(f"   Type2b file: {self.type2b_file} (exists: {os.path.exists(self.type2b_file)})")
    
    def load_type1_data(self, max_samples: int = None) -> List[Dict[str, Any]]:
        """
        Load Type1 data from CSV
        
        Args:
            max_samples: Maximum number of samples to load (None = all)
            
        Returns:
            List of conversation dictionaries
        """
        try:
            print(f"\n📊 Loading Type1 data from: {self.type1_file}")
            df = pd.read_csv(self.type1_file)
            
            if max_samples:
                df = df.head(max_samples)
            
            conversations = []
            for idx, row in df.iterrows():
                # Assuming CSV has columns like: id, transcript, or similar
                conv_id = row.get('id', row.get('request_id', f'type1_conv_{idx}'))
                
                # Try different possible column names for transcript
                transcript = None
                for col in ['transcript', 'Transcript', 'text', 'conversation', 'paragraph']:
                    if col in row.index and pd.notna(row[col]):
                        transcript = str(row[col])
                        break
                
                if transcript:
                    conversations.append({
                        'id': str(conv_id),
                        'transcript': transcript,
                        'type': 'type1',
                        'metadata': {k: v for k, v in row.items() if k not in ['transcript', 'Transcript']}
                    })
            
            print(f"✅ Loaded {len(conversations)} Type1 conversations")
            return conversations
            
        except Exception as e:
            print(f"❌ Error loading Type1 data: {e}")
            return []
    
    def load_type2a_data(self, max_samples: int = None) -> List[Dict[str, Any]]:
        """
        Load Type2a data from JSON files
        
        Args:
            max_samples: Maximum number of samples to load (None = all)
            
        Returns:
            List of conversation dictionaries
        """
        try:
            print(f"\n📊 Loading Type2a data from: {self.type2a_dir}")
            
            if not os.path.exists(self.type2a_dir):
                print(f"❌ Type2a directory not found")
                return []
            
            json_files = [f for f in os.listdir(self.type2a_dir) if f.endswith('.json')]
            
            if max_samples:
                json_files = json_files[:max_samples]
            
            conversations = []
            for json_file in json_files:
                try:
                    file_path = os.path.join(self.type2a_dir, json_file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Extract conversation ID (from filename or data)
                    conv_id = data.get('conversation_id', os.path.splitext(json_file)[0])
                    
                    # Extract transcript from turns structure
                    transcript = None
                    if isinstance(data, dict):
                        # Handle 'turns' structure (agent/customer conversation)
                        if 'turns' in data and isinstance(data['turns'], list):
                            turns = data['turns']
                            transcript_lines = []
                            for turn in turns:
                                if isinstance(turn, dict):
                                    speaker = turn.get('speaker', 'unknown').capitalize()
                                    text = turn.get('text', '')
                                    if text:
                                        transcript_lines.append(f"{speaker}: {text}")
                            transcript = '\n'.join(transcript_lines)
                        
                        # Try other possible keys if 'turns' not found
                        if not transcript:
                            for key in ['transcript', 'text', 'conversation', 'content', 'messages']:
                                if key in data:
                                    if isinstance(data[key], str):
                                        transcript = data[key]
                                    elif isinstance(data[key], list):
                                        # If it's a list of messages, join them
                                        transcript = '\n'.join([str(msg) for msg in data[key]])
                                    break
                    
                    if transcript:
                        conversations.append({
                            'id': conv_id,
                            'transcript': transcript,
                            'type': 'type2a',
                            'metadata': data if isinstance(data, dict) else {}
                        })
                    
                except Exception as e:
                    print(f"⚠️  Error loading {json_file}: {e}")
                    continue
            
            print(f"✅ Loaded {len(conversations)} Type2a conversations")
            return conversations
            
        except Exception as e:
            print(f"❌ Error loading Type2a data: {e}")
            return []
    
    def load_type2b_data(self, max_samples: int = None) -> List[Dict[str, Any]]:
        """
        Load Type2b data from CSV
        
        Args:
            max_samples: Maximum number of samples to load (None = all)
            
        Returns:
            List of conversation dictionaries
        """
        try:
            print(f"\n📊 Loading Type2b data from: {self.type2b_file}")
            df = pd.read_csv(self.type2b_file)
            
            if max_samples:
                df = df.head(max_samples)
            
            conversations = []
            for idx, row in df.iterrows():
                # Assuming CSV has columns like: id, transcript, labels
                conv_id = row.get('id', row.get('request_id', f'type2b_conv_{idx}'))
                
                # Try different possible column names for transcript
                transcript = None
                for col in ['transcript', 'Transcript', 'text', 'paragraph', 'labeled_paragraph']:
                    if col in row.index and pd.notna(row[col]):
                        transcript = str(row[col])
                        break
                
                if transcript:
                    conversations.append({
                        'id': str(conv_id),
                        'transcript': transcript,
                        'type': 'type2b',
                        'metadata': {k: v for k, v in row.items() if k not in ['transcript', 'Transcript']}
                    })
            
            print(f"✅ Loaded {len(conversations)} Type2b conversations")
            return conversations
            
        except Exception as e:
            print(f"❌ Error loading Type2b data: {e}")
            return []
    
    def load_all_data_types(self, max_samples_per_type: int = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load all 3 types of data
        
        Args:
            max_samples_per_type: Maximum samples per type (None = all)
            
        Returns:
            Dictionary with keys: 'type1', 'type2a', 'type2b'
        """
        print("\n" + "="*60)
        print("📚 Loading ALL Data Types for MISTRAL_BOOM_BOOM")
        print("="*60)
        
        data = {
            'type1': self.load_type1_data(max_samples_per_type),
            'type2a': self.load_type2a_data(max_samples_per_type),
            'type2b': self.load_type2b_data(max_samples_per_type)
        }
        
        print("\n" + "="*60)
        print("📊 Data Loading Summary:")
        print(f"   Type1: {len(data['type1'])} conversations")
        print(f"   Type2a: {len(data['type2a'])} conversations")
        print(f"   Type2b: {len(data['type2b'])} conversations")
        print(f"   Total: {sum(len(v) for v in data.values())} conversations")
        print("="*60)
        
        return data
    
    def get_data_by_type(self, data_type: str, max_samples: int = None) -> List[Dict[str, Any]]:
        """
        Load specific data type
        
        Args:
            data_type: 'type1', 'type2a', or 'type2b'
            max_samples: Maximum samples to load
            
        Returns:
            List of conversations
        """
        if data_type == 'type1':
            return self.load_type1_data(max_samples)
        elif data_type == 'type2a':
            return self.load_type2a_data(max_samples)
        elif data_type == 'type2b':
            return self.load_type2b_data(max_samples)
        else:
            print(f"❌ Unknown data type: {data_type}")
            return []


# Test function
if __name__ == "__main__":
    print("🧪 Testing BOOM BOOM Data Loader")
    print("="*60)
    
    loader = BoomBoomDataLoader()
    
    # Test each data type
    print("\n🔍 Testing Type1...")
    type1_data = loader.load_type1_data(max_samples=3)
    if type1_data:
        print(f"Sample: {type1_data[0]['id']}")
        print(f"Transcript preview: {type1_data[0]['transcript'][:100]}...")
    
    print("\n🔍 Testing Type2a...")
    type2a_data = loader.load_type2a_data(max_samples=3)
    if type2a_data:
        print(f"Sample: {type2a_data[0]['id']}")
        print(f"Transcript preview: {type2a_data[0]['transcript'][:100]}...")
    
    print("\n🔍 Testing Type2b...")
    type2b_data = loader.load_type2b_data(max_samples=3)
    if type2b_data:
        print(f"Sample: {type2b_data[0]['id']}")
        print(f"Transcript preview: {type2b_data[0]['transcript'][:100]}...")
    
    print("\n✅ Data loader testing complete!")

