"""
JD Enhancement Service - Enhances basic job descriptions using WORK methodology.
Transforms basic JDs into detailed, deliverables-focused descriptions suitable for interview question generation.
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime
from models import db, JobDescription, GenerationLog
from claude_client import ClaudeClientService
from prompts import JD_ENHANCEMENT_PROMPT, JD_ENHANCEMENT_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class JDEnhancementService:
    """
    Service for enhancing job descriptions using Claude and the WORK methodology.
    """
    
    def __init__(self, claude_client: Optional[ClaudeClientService] = None):
        """
        Initialize JD Enhancement Service.
        
        Args:
            claude_client: Claude client service. If not provided, creates a new one.
        """
        self.claude_client = claude_client or ClaudeClientService()
    
    def enhance_jd(
        self,
        req_id: str,
        basic_title: str,
        basic_description: str,
        user_id: str,
        basic_department: Optional[str] = None,
        basic_level: Optional[str] = None,
        work_output: Optional[str] = None,
        work_role: Optional[str] = None,
        work_knowledge: Optional[str] = None,
        work_competencies: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Enhance a basic job description using WORK methodology.
        
        Args:
            req_id: Unique requisition ID from ATS
            basic_title: Original job title
            basic_description: Original job description text
            user_id: ID of user requesting enhancement
            basic_department: Optional department
            basic_level: Optional job level (Junior, Senior, Lead, etc.)
            work_output: WORK - What will this person deliver/build?
            work_role: WORK - What are the key responsibilities/roles?
            work_knowledge: WORK - What knowledge areas are critical?
            work_competencies: WORK - What competencies are essential?
        
        Returns:
            Dictionary with:
            {
                'success': bool,
                'job_description_id': int,
                'basic_jd': {...},
                'enhanced_jd': {...},
                'tokens_used': int,
                'error': str (if failed)
            }
        """
        
        # Start generation log
        log_entry = GenerationLog(
            operation_type='jd_enhancement',
            req_id=req_id,
            user_id=user_id,
            status='in_progress',
            started_at=datetime.utcnow()
        )
        db.session.add(log_entry)
        db.session.commit()
        
        try:
            logger.info(f"Starting JD enhancement for req_id: {req_id}")
            
            # Check if JD already exists
            existing_jd = JobDescription.query.filter_by(req_id=req_id).first()
            if existing_jd:
                logger.warning(f"JD for req_id {req_id} already exists. Updating...")
                jd = existing_jd
            else:
                # Create new JD record
                jd = JobDescription(
                    req_id=req_id,
                    basic_title=basic_title,
                    basic_description=basic_description,
                    basic_department=basic_department,
                    basic_level=basic_level,
                    work_output=work_output,
                    work_role=work_role,
                    work_knowledge=work_knowledge,
                    work_competencies=work_competencies,
                    created_by_user_id=user_id
                )
                db.session.add(jd)
                db.session.flush()  # Get the ID without committing
            
            # Prepare JD content for Claude
            jd_content = f"""
TITLE: {basic_title}
DEPARTMENT: {basic_department or 'Not specified'}
LEVEL: {basic_level or 'Not specified'}

DESCRIPTION:
{basic_description}
            """.strip()
            
            # Build WORK context from user inputs
            work_context_parts = []
            if work_output:
                work_context_parts.append(f"Work Output (what they'll deliver/build):\n{work_output}")
            if work_role:
                work_context_parts.append(f"Key Roles and Responsibilities:\n{work_role}")
            if work_knowledge:
                work_context_parts.append(f"Critical Knowledge Areas:\n{work_knowledge}")
            if work_competencies:
                work_context_parts.append(f"Essential Competencies:\n{work_competencies}")
            
            work_context = "\n\n".join(work_context_parts) if work_context_parts else "No additional context provided"
            
            # Call Claude to enhance JD
            user_prompt = JD_ENHANCEMENT_PROMPT.format(
                work_context=work_context,
                jd_content=jd_content
            )
            
            logger.info("Calling Claude API for JD enhancement...")
            response = self.claude_client.call_claude(
                system_prompt=JD_ENHANCEMENT_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                temperature=0.3  # Lower temperature for consistency
            )
            
            if not response.get('success'):
                raise Exception(f"Claude API call failed: {response.get('error', 'Unknown error')}")
            
            # Extract enhanced description
            enhanced_description = response.get('text', '').strip()
            
            # Update JD with enhanced version
            jd.enhanced_title = basic_title  # Keep original title
            jd.enhanced_description = enhanced_description
            jd.enhanced_at = datetime.utcnow()
            
            # Store WORK inputs if provided
            if work_output:
                jd.work_output = work_output
            if work_role:
                jd.work_role = work_role
            if work_knowledge:
                jd.work_knowledge = work_knowledge
            if work_competencies:
                jd.work_competencies = work_competencies
            
            db.session.commit()
            
            # Update log
            log_entry.status = 'success'
            log_entry.tokens_used = response['usage']['total_tokens']
            log_entry.completed_at = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"JD enhancement completed for req_id {req_id}. Tokens: {response['usage']['total_tokens']}")
            
            return {
                'success': True,
                'job_description_id': jd.id,
                'req_id': req_id,
                'basic_jd': {
                    'title': basic_title,
                    'department': basic_department,
                    'level': basic_level,
                    'description': basic_description
                },
                'enhanced_jd': {
                    'title': jd.enhanced_title,
                    'description': enhanced_description
                },
                'work_inputs': {
                    'work_output': work_output,
                    'work_role': work_role,
                    'work_knowledge': work_knowledge,
                    'work_competencies': work_competencies
                },
                'tokens_used': response['usage']['total_tokens'],
                'created_at': jd.created_at.isoformat(),
                'enhanced_at': jd.enhanced_at.isoformat()
            }
        
        except Exception as e:
            logger.error(f"JD enhancement failed: {str(e)}")
            
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
    
    def get_enhanced_jd(self, req_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an already-enhanced JD.
        
        Args:
            req_id: Requisition ID
        
        Returns:
            Dictionary with JD details or None if not found
        """
        jd = JobDescription.query.filter_by(req_id=req_id).first()
        
        if not jd:
            return None
        
        return {
            'job_description_id': jd.id,
            'req_id': jd.req_id,
            'basic_jd': {
                'title': jd.basic_title,
                'department': jd.basic_department,
                'level': jd.basic_level,
                'description': jd.basic_description
            },
            'enhanced_jd': {
                'title': jd.enhanced_title,
                'description': jd.enhanced_description
            },
            'created_at': jd.created_at.isoformat(),
            'enhanced_at': jd.enhanced_at.isoformat() if jd.enhanced_at else None
        }
