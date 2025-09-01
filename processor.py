import re
import json
import time
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from api_client import api_client
from prompts import ASSESSMENT_PROMPTS
from config import RETRY_DELAY

class ConversationProcessor:
    """Handles processing conversations and extracting assessment results"""
    
    def __init__(self):
        self.api_client = api_client
    
    def clean_llm_response(self, text: str) -> str:
        """Clean the LLM response by removing code block markers"""
        text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()
        return text
    
    def extract_json_objects(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract JSON objects from the model output
        
        Args:
            text: Raw response text from the API
            
        Returns:
            List of extracted JSON objects
        """
        cleaned = self.clean_llm_response(text)
        try:
            objs = []
            # Look for all {...} blocks
            for match in re.finditer(r'\{[\s\S]*?\}', cleaned):
                try:
                    obj = json.loads(match.group())
                    objs.append(obj)
                except json.JSONDecodeError:
                    continue
            
            if not objs:
                # fallback: try to parse the entire cleaned text
                try:
                    objs = [json.loads(cleaned)]
                except json.JSONDecodeError:
                    print(f"Could not parse JSON from: {cleaned[:200]}...")
                    return []
            
            return objs
        except Exception as e:
            print(f"extract_json_objects: Could not parse JSON. Error: {e}")
            return []
    
    def process_conversation_with_prompt(self, 
                                       df: pd.DataFrame, 
                                       prompt_type: str,
                                       max_conversations: Optional[int] = None) -> Tuple[List[Dict], List[Tuple]]:
        """
        Process conversations with a specific prompt type
        
        Args:
            df: DataFrame containing conversations
            prompt_type: Type of assessment ('opening', 'closing', etc.)
            max_conversations: Maximum number of conversations to process (for testing)
            
        Returns:
            Tuple of (results, failed_chats)
        """
        if prompt_type not in ASSESSMENT_PROMPTS:
            raise ValueError(f"Invalid prompt type: {prompt_type}. Available types: {list(ASSESSMENT_PROMPTS.keys())}")
        
        prompt = ASSESSMENT_PROMPTS[prompt_type]
        results = []
        failed_chats = []
        
        # Limit conversations for testing if specified
        if max_conversations:
            df = df.head(max_conversations)
        
        print(f"Processing {len(df)} conversations for {prompt_type} assessment...")
        
        for index, row in df.iterrows():
            conversation = row["transcript"]
            request_id = row["request_id"]
            full_prompt = conversation + "\n\n" + prompt
            
            print(f"Processing conversation {index + 1}/{len(df)} (ID: {request_id})")
            
            try:
                response_text = self.api_client.call_api(user_prompt=full_prompt)
                if response_text is None:
                    raise Exception("No response from API")
                
                extracted_info = self.extract_json_objects(response_text)
                if not extracted_info:
                    raise Exception("No valid JSON extracted from response")
                
                print(f"Extracted info: {extracted_info}")
                
                result = [item.get('Value', None) for item in extracted_info]
                evidence = [item.get('Evidence', None) for item in extracted_info]
                
                results.append({
                    'request_id': request_id,
                    'parameter_result': result,
                    'parameter_evidence': evidence
                })
                
            except Exception as e:
                failed_chats.append((index, request_id, conversation))
                print(f"Failed chat: {request_id} due to error: {e}")
                continue
            
            # Rate limiting
            time.sleep(RETRY_DELAY)
        
        print(f"Completed {prompt_type} assessment. Success: {len(results)}, Failed: {len(failed_chats)}")
        return results, failed_chats
    
    def process_failed_chats(self, failed_chats: List[Tuple], prompt_type: str) -> List[Dict]:
        """
        Retry processing failed chats
        
        Args:
            failed_chats: List of failed chat tuples
            prompt_type: Type of assessment
            
        Returns:
            List of retry results
        """
        if not failed_chats:
            return []
        
        prompt = ASSESSMENT_PROMPTS[prompt_type]
        retry_results = []
        
        print(f"Retrying {len(failed_chats)} failed chats for {prompt_type}...")
        
        for row in failed_chats:
            index = row[0]
            request_id = row[1]
            conversation = row[2]
            full_prompt = conversation + "\n\n" + prompt
            
            try:
                response_text = self.api_client.call_api(user_prompt=full_prompt)
                if response_text is None:
                    raise Exception("No response from API")
                
                extracted_info = self.extract_json_objects(response_text)
                if not extracted_info:
                    raise Exception("No valid JSON extracted from response")
                
                print(f"Retry extracted info: {extracted_info}")
                
                result = [item.get('Value', None) for item in extracted_info]
                evidence = [item.get('Evidence', None) for item in extracted_info]
                
                retry_results.append({
                    'request_id': request_id,
                    'parameter_result': result,
                    'parameter_evidence': evidence
                })
                
            except Exception as e:
                print(f"Retry failed for chat: {request_id} due to error: {e}")
                continue
            
            time.sleep(RETRY_DELAY)
        
        print(f"Retry completed for {prompt_type}. Success: {len(retry_results)}")
        return retry_results
    
    def merge_results_and_retries(self, results: List[Dict], retry_results: List[Dict]) -> pd.DataFrame:
        """
        Merge main results with retry results
        
        Args:
            results: Main processing results
            retry_results: Retry processing results
            
        Returns:
            Combined DataFrame
        """
        res_df = pd.DataFrame(results)
        if retry_results:
            retry_df = pd.DataFrame(retry_results)
            res_df = pd.concat([res_df, retry_df], ignore_index=True)
        return res_df
    
    def process_all_assessments(self, df: pd.DataFrame, max_conversations: Optional[int] = None) -> Dict[str, pd.DataFrame]:
        """
        Process all assessment types for the given conversations
        
        Args:
            df: DataFrame containing conversations
            max_conversations: Maximum number of conversations to process (for testing)
            
        Returns:
            Dictionary of results for each assessment type
        """
        all_results = {}
        
        for prompt_type in ASSESSMENT_PROMPTS.keys():
            print(f"\n{'='*50}")
            print(f"Processing {prompt_type.upper()} assessment")
            print(f"{'='*50}")
            
            # Process main batch
            results, failed_chats = self.process_conversation_with_prompt(
                df, prompt_type, max_conversations
            )
            
            # Retry failed chats
            retry_results = self.process_failed_chats(failed_chats, prompt_type)
            
            # Merge results
            final_df = self.merge_results_and_retries(results, retry_results)
            all_results[prompt_type] = final_df
            
            print(f"Final results for {prompt_type}: {len(final_df)} successful assessments")
        
        return all_results

# Global processor instance
processor = ConversationProcessor() 