"""
Interview Generation Service - Generates 5-question interviews from enhanced job descriptions.
Uses the Interview Creation Framework to produce structured Q&A with 8-10 evaluation criteria per question.
"""

import logging
import hashlib
from typing import Optional, Dict, Any, List
from datetime import datetime
from .models import db, JobDescription, Interview, InterviewQuestion, QuestionCache, GenerationLog
from .claude_client import ClaudeClientService
from .prompts import INTERVIEW_GENERATION_PROMPT, INTERVIEW_GENERATION_SYSTEM_PROMPT
from .config import Config

logger = logging.getLogger(__name__)


class InterviewGenerationService:
    """
    Service for generating interview questions from enhanced job descriptions.
    Implements caching for similar questions to optimize API usage.
    """
    
    def __init__(self, claude_client: Optional[ClaudeClientService] = None):
        """
        Initialize Interview Generation Service.
        
        Args:
            claude_client: Claude client service. If not provided, creates a new one.
        """
        self.claude_client = claude_client or ClaudeClientService()
        self.enable_cache = Config.ENABLE_QUESTION_CACHE
        self.similarity_threshold = Config.CACHE_SIMILARITY_THRESHOLD
    
    def generate_interview(
        self,
        req_id: str,
        job_description_id: int,
        user_id: str,
        interview_name: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a complete 5-question interview from an enhanced JD.
        
        Args:
            req_id: Requisition ID
            job_description_id: ID of the JobDescription to use
            user_id: ID of user requesting interview generation
            interview_name: Custom name for the interview (optional)
            use_cache: Whether to use cached questions (default True)
        
        Returns:
            Dictionary with:
            {
                'success': bool,
                'interview_id': int,
                'req_id': str,
                'interview': {...},  # Full interview with questions
                'tokens_used': int,
                'cached_questions': int,
                'error': str (if failed)
            }
        """
        
        # Start generation log
        log_entry = GenerationLog(
            operation_type='interview_generation',
            req_id=req_id,
            user_id=user_id,
            status='in_progress',
            started_at=datetime.utcnow()
        )
        db.session.add(log_entry)
        db.session.commit()
        
        try:
            logger.info(f"Starting interview generation for req_id: {req_id}")
            
            # Get the job description
            jd = JobDescription.query.filter_by(id=job_description_id).first()
            if not jd:
                raise ValueError(f"Job description with id {job_description_id} not found")
            
            # Use enhanced description if available, otherwise basic
            jd_content = jd.enhanced_description or jd.basic_description
            
            if not interview_name:
                interview_name = f"{jd.basic_title} - Interview"
            
            # Create interview record
            interview = Interview(
                job_description_id=job_description_id,
                req_id=req_id,
                interview_name=interview_name,
                created_by_user_id=user_id
            )
            db.session.add(interview)
            db.session.flush()  # Get the ID
            
            total_tokens_used = 0
            cached_questions_count = 0
            
            # Call Claude to generate interview
            logger.info("Calling Claude API for interview generation...")
            user_prompt = INTERVIEW_GENERATION_PROMPT.format(jd_content=jd_content)
            
            response = self.claude_client.call_claude(
                system_prompt=INTERVIEW_GENERATION_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                temperature=0.4  # Moderate temperature for creativity with consistency
            )
            
            if not response.get('success'):
                raise Exception(f"Claude API call failed: {response.get('error', 'Unknown error')}")
            
            total_tokens_used += response['usage']['total_tokens']
            
            # Parse the response into structured questions
            logger.info("Parsing Claude response...")
            questions_data = self.claude_client.parse_interview_response(response['text'])
            
            # Validate structure
            self.claude_client.validate_interview_structure(questions_data)
            
            logger.info(f"Successfully parsed {len(questions_data)} questions")
            
            # Create InterviewQuestion records
            for q_data in questions_data:
                # Convert criteria to standardized format
                criteria = [
                    {
                        'criterion': c['criterion'],
                        'description': c['description'],
                        'is_checked': False
                    }
                    for c in q_data.get('criteria', [])
                ]
                
                question = InterviewQuestion(
                    interview_id=interview.id,
                    question_number=q_data['question_number'],
                    question_text=q_data['question_text'],
                    question_type='technical',
                    criteria=criteria
                )
                db.session.add(question)
            
            db.session.commit()
            
            # Update log
            log_entry.status = 'success'
            log_entry.tokens_used = total_tokens_used
            log_entry.completed_at = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"Interview generation completed for req_id {req_id}. "
                       f"Total tokens: {total_tokens_used}, Cached: {cached_questions_count}")
            
            # Return complete interview
            return {
                'success': True,
                'interview_id': interview.id,
                'req_id': req_id,
                'interview_name': interview.interview_name,
                'interview': interview.to_dict(),
                'tokens_used': total_tokens_used,
                'cached_questions': cached_questions_count,
                'created_at': interview.created_at.isoformat()
            }
        
        except Exception as e:
            logger.error(f"Interview generation failed: {str(e)}")
            
            # Update log with error
            log_entry.status = 'failed'
            log_entry.error_message = str(e)
            log_entry.completed_at = datetime.utcnow()
            db.session.commit()
            
            db.session.rollback()
            
            return {
                'success': False,
                'req_id': req_id,
                'error': str(e)
            }
    
    def get_interview(self, interview_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a generated interview by ID.
        
        Args:
            interview_id: Interview ID
        
        Returns:
            Dictionary with complete interview or None if not found
        """
        interview = Interview.query.filter_by(id=interview_id).first()
        
        if not interview:
            return None
        
        return interview.to_dict()
    
    def get_interview_by_req(self, req_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        Retrieve all interviews for a given requisition.
        
        Args:
            req_id: Requisition ID
        
        Returns:
            List of interview dictionaries
        """
        interviews = Interview.query.filter_by(req_id=req_id).all()
        
        if not interviews:
            return None
        
        return [interview.to_dict() for interview in interviews]
    
    def _cache_question(
        self,
        topic: str,
        skill_level: str,
        question_text: str,
        criteria: List[Dict[str, str]]
    ) -> str:
        """
        Cache a generated question for future reuse.
        
        Args:
            topic: Technical topic (e.g., 'CI/CD', 'React')
            skill_level: Skill level (e.g., 'Intermediate', 'Advanced')
            question_text: The question text
            criteria: List of criteria dictionaries
        
        Returns:
            Cache key
        """
        if not self.enable_cache:
            return None
        
        # Create a hash key from topic and skill level
        cache_key_str = f"{topic}:{skill_level}"
        cache_key = hashlib.md5(cache_key_str.encode()).hexdigest()
        
        # Check if this already exists
        existing = QuestionCache.query.filter_by(cache_key=cache_key).first()
        
        if existing:
            existing.increment_usage()
            return existing.cache_key
        
        # Create new cache entry
        cache_entry = QuestionCache(
            cache_key=cache_key,
            request_hash=hashlib.md5(question_text.encode()).hexdigest(),
            topic=topic,
            skill_level=skill_level,
            question_text=question_text,
            criteria=criteria
        )
        db.session.add(cache_entry)
        db.session.commit()
        
        logger.info(f"Cached question for {topic} ({skill_level})")
        
        return cache_key
    
    def _get_cached_question(self, topic: str, skill_level: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a cached question if available.
        
        Args:
            topic: Technical topic
            skill_level: Skill level
        
        Returns:
            Cached question dictionary or None
        """
        if not self.enable_cache:
            return None
        
        cache_key_str = f"{topic}:{skill_level}"
        cache_key = hashlib.md5(cache_key_str.encode()).hexdigest()
        
        cached = QuestionCache.query.filter_by(cache_key=cache_key).first()
        
        if cached:
            cached.increment_usage()
            return {
                'question_text': cached.question_text,
                'criteria': cached.criteria
            }
        
        return None
