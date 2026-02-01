"""
Claude API client service for making API calls to generate JD enhancements and interview questions.
Handles error handling, retries, and response parsing.
"""

import logging
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
import time
from anthropic import Anthropic, APIError, RateLimitError, APIConnectionError
from .config import Config

logger = logging.getLogger(__name__)


class ClaudeClientService:
    """
    Service for interacting with the Claude API.
    Handles authentication, request/response formatting, and error handling.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Claude client.
        
        Args:
            api_key: Claude API key. If not provided, uses CLAUDE_API_KEY from config.
        """
        self.api_key = api_key or Config.CLAUDE_API_KEY
        self.client = Anthropic(api_key=self.api_key)
        self.model = Config.CLAUDE_MODEL
        self.max_tokens = Config.CLAUDE_MAX_TOKENS
        self.max_retries = 3
        self.retry_delay = 2
    
    def call_claude(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Make a call to Claude API with retry logic.
        
        Args:
            system_prompt: System instruction for Claude
            user_prompt: User query/prompt
            max_tokens: Maximum tokens in response (defaults to config value)
            temperature: Temperature for response variability (0-1)
        
        Returns:
            Dictionary with response text and metadata
        
        Raises:
            Exception: If API call fails after max retries
        """
        max_tokens = max_tokens or self.max_tokens
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Claude API call attempt {attempt + 1}/{self.max_retries}")
                
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ]
                )
                
                # Extract text from response
                response_text = response.content[0].text
                
                result = {
                    'success': True,
                    'text': response_text,
                    'usage': {
                        'input_tokens': response.usage.input_tokens,
                        'output_tokens': response.usage.output_tokens,
                        'total_tokens': response.usage.input_tokens + response.usage.output_tokens
                    },
                    'model': response.model,
                    'stop_reason': response.stop_reason
                }
                
                logger.info(f"Claude API call successful. Tokens used: {result['usage']['total_tokens']}")
                return result
                
            except RateLimitError as e:
                logger.warning(f"Rate limit hit on attempt {attempt + 1}. Retrying...")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    logger.error("Max retries exceeded due to rate limiting")
                    raise Exception(f"Claude API rate limit exceeded: {str(e)}")
            
            except APIConnectionError as e:
                logger.warning(f"Connection error on attempt {attempt + 1}. Retrying...")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    logger.error("Max retries exceeded due to connection errors")
                    raise Exception(f"Claude API connection failed: {str(e)}")
            
            except APIError as e:
                logger.error(f"Claude API error: {str(e)}")
                if attempt == self.max_retries - 1:
                    raise Exception(f"Claude API error: {str(e)}")
                time.sleep(self.retry_delay)
            
            except Exception as e:
                logger.error(f"Unexpected error in Claude API call: {str(e)}")
                raise
        
        raise Exception("Claude API call failed after max retries")
    
    def parse_interview_response(self, response_text: str) -> List[Dict[str, Any]]:
        """
        Parse Claude's interview generation response into structured format.
        
        Converts the formatted question response into a list of question objects,
        each with text and criteria.
        
        Args:
            response_text: Raw response from Claude
        
        Returns:
            List of question dictionaries with structure:
            {
                'question_number': int,
                'question_text': str,
                'expected_answer': str,
                'criteria': [
                    {
                        'criterion': str,
                        'description': str
                    },
                    ...
                ]
            }
        """
        questions = []
        current_question = None
        lines = response_text.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Detect question header: [Question N]:
            if line.startswith('[Question ') and ']: ' in line:
                # Save previous question if exists
                if current_question is not None:
                    questions.append(current_question)
                
                # Parse question number and text
                parts = line.split(']: ', 1)
                question_num_part = parts[0]  # e.g., "[Question 1"
                question_num = int(question_num_part.split()[-1])
                question_text = parts[1] if len(parts) > 1 else ''
                
                current_question = {
                    'question_number': question_num,
                    'question_text': question_text,
                    'criteria': []
                }
            
            # Detect Expected Answer section
            elif line.startswith('Expected Answer: ') and current_question:
                current_question['expected_answer'] = line.replace('Expected Answer: ', '')
            
            # Detect criteria (lines that have a colon followed by description)
            elif ': ' in line and current_question and not line.startswith('['):
                parts = line.split(': ', 1)
                criterion_name = parts[0].strip()
                description = parts[1].strip() if len(parts) > 1 else ''
                
                # Validate it looks like a criterion (not metadata)
                if criterion_name and not criterion_name.startswith('---'):
                    current_question['criteria'].append({
                        'criterion': criterion_name,
                        'description': description
                    })
            
            i += 1
        
        # Don't forget the last question
        if current_question is not None:
            questions.append(current_question)
        
        logger.info(f"Parsed {len(questions)} questions from Claude response")
        return questions
    
    def validate_interview_structure(self, questions: List[Dict[str, Any]]) -> bool:
        """
        Validate that interview has correct structure.
        
        Args:
            questions: List of parsed questions
        
        Returns:
            True if valid, raises exception otherwise
        """
        if len(questions) != 5:
            raise ValueError(f"Expected 5 questions, got {len(questions)}")
        
        for i, q in enumerate(questions):
            question_num = q.get('question_number')
            if question_num != i + 1:
                raise ValueError(f"Question numbering is incorrect. Expected {i+1}, got {question_num}")
            
            criteria_count = len(q.get('criteria', []))
            if criteria_count < 8 or criteria_count > 10:
                raise ValueError(
                    f"Question {i+1} has {criteria_count} criteria. "
                    f"Expected 8-10 criteria."
                )
            
            if not q.get('question_text'):
                raise ValueError(f"Question {i+1} is missing question text")
            
            for j, criterion in enumerate(q.get('criteria', [])):
                if not criterion.get('criterion'):
                    raise ValueError(f"Question {i+1}, Criterion {j+1} is missing name")
                if not criterion.get('description'):
                    raise ValueError(f"Question {i+1}, Criterion {j+1} is missing description")
        
        return True


class MockClaudeClient:
    """
    Mock Claude client for testing purposes.
    Returns predefined responses without making actual API calls.
    """
    
    def call_claude(self, system_prompt: str, user_prompt: str, **kwargs) -> Dict[str, Any]:
        """Return mock response"""
        return {
            'success': True,
            'text': "This is a mock response. Replace with actual Claude API when ready.",
            'usage': {'input_tokens': 100, 'output_tokens': 100, 'total_tokens': 200},
            'model': 'claude-opus-4-1',
            'stop_reason': 'end_turn'
        }
    
    def parse_interview_response(self, response_text: str) -> List[Dict[str, Any]]:
        """Return empty list for mock"""
        return []
    
    def validate_interview_structure(self, questions: List[Dict[str, Any]]) -> bool:
        """Always valid for mock"""
        return True
