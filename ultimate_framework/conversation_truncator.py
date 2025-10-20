"""
Conversation Truncator - Handle conversations that exceed token limits
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ConversationTruncator:
    """Truncate long conversations to fit within model context"""
    
    def __init__(self, max_tokens: int = 7000):
        """
        Initialize truncator
        
        Args:
            max_tokens: Maximum tokens to allow for transcript+prompt
                       (leaves room for response)
        """
        self.max_tokens = max_tokens
    
    def truncate(self, transcript: str, prompt: str) -> Dict[str, Any]:
        """
        Truncate conversation if needed
        
        Args:
            transcript: Full conversation transcript
            prompt: Assessment prompt
        
        Returns:
            Dict with:
                - truncated_transcript: Possibly shortened transcript
                - was_truncated: Boolean
                - original_length: Original character count
                - truncated_length: Final character count
                - truncation_strategy: What was done
        """
        # Estimate tokens (rough: 1 token ≈ 4 chars)
        transcript_chars = len(transcript)
        prompt_chars = len(prompt)
        total_chars = transcript_chars + prompt_chars
        estimated_tokens = total_chars // 4
        
        # If within limits, return as-is
        if estimated_tokens <= self.max_tokens:
            return {
                'truncated_transcript': transcript,
                'was_truncated': False,
                'original_length': transcript_chars,
                'truncated_length': transcript_chars,
                'truncation_strategy': 'none',
                'estimated_tokens': estimated_tokens
            }
        
        # Calculate how much to truncate
        max_transcript_chars = (self.max_tokens * 4) - prompt_chars
        
        if max_transcript_chars < 1000:
            logger.error(f"Prompt too long! Prompt: {prompt_chars} chars, " +
                        f"leaving only {max_transcript_chars} for transcript")
            # Still try to truncate, but warn
        
        # Strategy: Keep beginning + end, remove middle
        # Opening/Closing need both start and end!
        keep_start = int(max_transcript_chars * 0.6)  # 60% from start
        keep_end = int(max_transcript_chars * 0.3)     # 30% from end
        # 10% buffer for truncation marker
        
        truncated = (
            transcript[:keep_start] + 
            "\n\n[... MIDDLE PORTION TRUNCATED DUE TO LENGTH ...]\n\n" +
            transcript[-keep_end:]
        )
        
        logger.warning(f"Conversation truncated: {transcript_chars} → {len(truncated)} chars " +
                      f"(kept {keep_start} start + {keep_end} end)")
        
        return {
            'truncated_transcript': truncated,
            'was_truncated': True,
            'original_length': transcript_chars,
            'truncated_length': len(truncated),
            'truncation_strategy': 'start_end_keep',
            'estimated_tokens': len(truncated) // 4 + prompt_chars // 4,
            'kept_start_chars': keep_start,
            'kept_end_chars': keep_end
        }
    
    def truncate_middle_only(self, transcript: str, prompt: str) -> Dict[str, Any]:
        """
        Alternative: Keep start and end, remove middle more aggressively
        Better for opening/closing assessment
        """
        transcript_chars = len(transcript)
        prompt_chars = len(prompt)
        total_chars = transcript_chars + prompt_chars
        estimated_tokens = total_chars // 4
        
        if estimated_tokens <= self.max_tokens:
            return {
                'truncated_transcript': transcript,
                'was_truncated': False,
                'original_length': transcript_chars,
                'truncated_length': transcript_chars,
                'truncation_strategy': 'none',
                'estimated_tokens': estimated_tokens
            }
        
        max_transcript_chars = (self.max_tokens * 4) - prompt_chars
        
        # Keep first 40% and last 40%, remove middle 20%
        keep_start = int(max_transcript_chars * 0.45)
        keep_end = int(max_transcript_chars * 0.45)
        
        truncated = (
            transcript[:keep_start] + 
            "\n\n[... TRUNCATED ...]\n\n" +
            transcript[-keep_end:]
        )
        
        logger.warning(f"Middle-only truncation: {transcript_chars} → {len(truncated)} chars")
        
        return {
            'truncated_transcript': truncated,
            'was_truncated': True,
            'original_length': transcript_chars,
            'truncated_length': len(truncated),
            'truncation_strategy': 'middle_removed',
            'estimated_tokens': len(truncated) // 4 + prompt_chars // 4,
            'kept_start_chars': keep_start,
            'kept_end_chars': keep_end
        }


if __name__ == "__main__":
    # Test the truncator
    logging.basicConfig(level=logging.INFO)
    
    truncator = ConversationTruncator(max_tokens=7000)
    
    # Simulate long conversation
    long_transcript = "agent: Hello " * 10000  # Very long
    short_prompt = "Check if greeting is present"
    
    result = truncator.truncate(long_transcript, short_prompt)
    
    print(f"Original: {result['original_length']} chars")
    print(f"Truncated: {result['truncated_length']} chars")
    print(f"Was truncated: {result['was_truncated']}")
    print(f"Strategy: {result['truncation_strategy']}")
    print(f"Estimated tokens: {result['estimated_tokens']}")

