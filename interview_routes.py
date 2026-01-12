"""
Flask API routes for JD Enhancement and Interview Generation.
These endpoints expose the services to the frontend application.
"""

import logging
from flask import Blueprint, request, jsonify
from datetime import datetime
from functools import wraps
from models import db, JobDescription, Interview
from jd_enhancement_service import JDEnhancementService
from interview_generation_service import InterviewGenerationService
from claude_client import ClaudeClientService

logger = logging.getLogger(__name__)

# Create blueprints
interview_bp = Blueprint('interview', __name__, url_prefix='/api/interview')

# Initialize services
claude_client = ClaudeClientService()
jd_enhancement_service = JDEnhancementService(claude_client)
interview_generation_service = InterviewGenerationService(claude_client)


def require_admin(f):
    """
    Decorator to require admin access.
    Should be customized to work with your actual authentication system.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # TODO: Implement actual authentication check
        # This is a placeholder - integrate with your auth system
        user_id = request.headers.get('X-User-ID')
        user_role = request.headers.get('X-User-Role', 'user')
        
        if user_role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def require_auth(f):
    """
    Decorator to require user authentication.
    Should be customized to work with your actual authentication system.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # TODO: Implement actual authentication check
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


# ============================================================================
# JD ENHANCEMENT ENDPOINTS
# ============================================================================

@interview_bp.route('/jd/enhance', methods=['POST'])
@require_admin
def enhance_jd():
    """
    Enhance a basic job description using WORK methodology.
    WORK inputs are optional but highly recommended for better results.
    
    Request body:
    {
        "req_id": "REQ-12345",
        "basic_title": "Senior Software Engineer",
        "basic_description": "We are looking for a senior engineer...",
        "basic_department": "Engineering",
        "basic_level": "Senior",
        
        "work_output": "Design and build microservices that handle 10k transactions/sec",
        "work_role": "Lead backend engineer, mentor juniors, own service reliability",
        "work_knowledge": "Kafka, PostgreSQL, Spring Boot, distributed systems",
        "work_competencies": "System design, problem solving, technical depth"
    }
    
    WORK fields are OPTIONAL:
    - work_output: What will this person deliver/build?
    - work_role: What are the key responsibilities?
    - work_knowledge: What knowledge areas are critical?
    - work_competencies: What competencies are essential?
    
    Response:
    {
        "success": true,
        "job_description_id": 123,
        "enhanced_jd": {...}
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['req_id', 'basic_title', 'basic_description']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get user ID from request
        user_id = request.headers.get('X-User-ID', 'system')
        
        # Call enhancement service with WORK inputs
        result = jd_enhancement_service.enhance_jd(
            req_id=data['req_id'],
            basic_title=data['basic_title'],
            basic_description=data['basic_description'],
            user_id=user_id,
            basic_department=data.get('basic_department'),
            basic_level=data.get('basic_level'),
            work_output=data.get('work_output'),
            work_role=data.get('work_role'),
            work_knowledge=data.get('work_knowledge'),
            work_competencies=data.get('work_competencies')
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    
    except Exception as e:
        logger.error(f"Error in enhance_jd: {str(e)}")
        return jsonify({'error': str(e)}), 500


@interview_bp.route('/jd/<req_id>', methods=['GET'])
@require_auth
def get_jd(req_id):
    """
    Retrieve an enhanced job description.
    
    Response:
    {
        "success": true,
        "job_description": {...}
    }
    """
    try:
        result = jd_enhancement_service.get_enhanced_jd(req_id)
        
        if result:
            return jsonify({'success': True, 'job_description': result}), 200
        else:
            return jsonify({'error': 'Job description not found'}), 404
    
    except Exception as e:
        logger.error(f"Error in get_jd: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# INTERVIEW GENERATION ENDPOINTS
# ============================================================================

@interview_bp.route('/generate', methods=['POST'])
@require_admin
def generate_interview():
    """
    Generate a 5-question interview from an enhanced job description.
    
    Request body:
    {
        "req_id": "REQ-12345",
        "job_description_id": 123,
        "interview_name": "Senior Engineer Interview - Q4 2025"
    }
    
    Response:
    {
        "success": true,
        "interview_id": 456,
        "interview": {...}
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['req_id', 'job_description_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get user ID from request
        user_id = request.headers.get('X-User-ID', 'system')
        
        # Call interview generation service
        result = interview_generation_service.generate_interview(
            req_id=data['req_id'],
            job_description_id=data['job_description_id'],
            user_id=user_id,
            interview_name=data.get('interview_name'),
            use_cache=data.get('use_cache', True)
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    
    except Exception as e:
        logger.error(f"Error in generate_interview: {str(e)}")
        return jsonify({'error': str(e)}), 500


@interview_bp.route('/<int:interview_id>', methods=['GET'])
@require_auth
def get_interview(interview_id):
    """
    Retrieve a generated interview by ID.
    
    Response:
    {
        "success": true,
        "interview": {...}
    }
    """
    try:
        result = interview_generation_service.get_interview(interview_id)
        
        if result:
            return jsonify({'success': True, 'interview': result}), 200
        else:
            return jsonify({'error': 'Interview not found'}), 404
    
    except Exception as e:
        logger.error(f"Error in get_interview: {str(e)}")
        return jsonify({'error': str(e)}), 500


@interview_bp.route('/req/<req_id>', methods=['GET'])
@require_auth
def get_interviews_by_req(req_id):
    """
    Retrieve all interviews for a given requisition ID.
    
    Response:
    {
        "success": true,
        "interviews": [...]
    }
    """
    try:
        result = interview_generation_service.get_interview_by_req(req_id)
        
        if result:
            return jsonify({'success': True, 'interviews': result}), 200
        else:
            return jsonify({'success': True, 'interviews': []}), 200
    
    except Exception as e:
        logger.error(f"Error in get_interviews_by_req: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# WORKFLOW ENDPOINTS (Two separate workflows)
# ============================================================================

@interview_bp.route('/workflow/jd-only', methods=['POST'])
@require_admin
def workflow_jd_enhancement_only():
    """
    WORKFLOW 1: JD Enhancement Only
    
    Use this when you ONLY want to enhance a job description.
    Answers WORK questions to guide the enhancement.
    
    Request body:
    {
        "req_id": "REQ-12345",
        "basic_title": "Senior Software Engineer",
        "basic_description": "We are looking for...",
        
        "work_output": "Design and build microservices processing 10k transactions/sec",
        "work_role": "Lead backend engineer, mentor juniors, own service reliability",
        "work_knowledge": "Kafka, PostgreSQL, Spring Boot, distributed systems, load balancing",
        "work_competencies": "System design, problem solving, communication, technical depth"
    }
    
    Response:
    {
        "success": true,
        "job_description_id": 123,
        "enhanced_jd": {
            "title": "Senior Software Engineer",
            "description": "Enhanced description with clear deliverables..."
        },
        "work_inputs": {...},
        "tokens_used": 1250
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['req_id', 'basic_title', 'basic_description']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get user ID from request
        user_id = request.headers.get('X-User-ID', 'system')
        
        logger.info(f"Starting JD-only workflow for req_id: {data['req_id']}")
        
        # Call enhancement service with WORK inputs
        result = jd_enhancement_service.enhance_jd(
            req_id=data['req_id'],
            basic_title=data['basic_title'],
            basic_description=data['basic_description'],
            user_id=user_id,
            basic_department=data.get('basic_department'),
            basic_level=data.get('basic_level'),
            work_output=data.get('work_output'),
            work_role=data.get('work_role'),
            work_knowledge=data.get('work_knowledge'),
            work_competencies=data.get('work_competencies')
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    
    except Exception as e:
        logger.error(f"Error in workflow_jd_enhancement_only: {str(e)}")
        return jsonify({'error': str(e)}), 500


@interview_bp.route('/workflow/full', methods=['POST'])
@require_admin
def workflow_full_jd_and_interview():
    """
    WORKFLOW 2: Complete Workflow - JD Enhancement + Interview Generation
    
    Use this when you want to BOTH enhance a JD AND generate a 5-question interview.
    Answers WORK questions to guide the enhancement and interview generation.
    
    Request body:
    {
        "req_id": "REQ-12345",
        "basic_title": "Senior Software Engineer",
        "basic_description": "We are looking for...",
        "basic_department": "Engineering",
        "basic_level": "Senior",
        
        "work_output": "Design and build microservices processing 10k transactions/sec",
        "work_role": "Lead backend engineer, mentor juniors, own service reliability",
        "work_knowledge": "Kafka, PostgreSQL, Spring Boot, distributed systems, load balancing",
        "work_competencies": "System design, problem solving, communication, technical depth",
        
        "interview_name": "Senior Engineer Interview - Q1 2025"
    }
    
    Response:
    {
        "success": true,
        "job_description_id": 123,
        "interview_id": 456,
        "req_id": "REQ-12345",
        "interview": {
            "id": 456,
            "questions": [...]
        },
        "total_tokens_used": 3350
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['req_id', 'basic_title', 'basic_description']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get user ID from request
        user_id = request.headers.get('X-User-ID', 'system')
        
        logger.info(f"Starting complete workflow for req_id: {data['req_id']}")
        
        # Step 1: Enhance JD with WORK inputs
        jd_result = jd_enhancement_service.enhance_jd(
            req_id=data['req_id'],
            basic_title=data['basic_title'],
            basic_description=data['basic_description'],
            user_id=user_id,
            basic_department=data.get('basic_department'),
            basic_level=data.get('basic_level'),
            work_output=data.get('work_output'),
            work_role=data.get('work_role'),
            work_knowledge=data.get('work_knowledge'),
            work_competencies=data.get('work_competencies')
        )
        
        if not jd_result['success']:
            return jsonify(jd_result), 500
        
        total_tokens = jd_result.get('tokens_used', 0)
        
        # Step 2: Generate Interview
        interview_result = interview_generation_service.generate_interview(
            req_id=data['req_id'],
            job_description_id=jd_result['job_description_id'],
            user_id=user_id,
            interview_name=data.get('interview_name')
        )
        
        if not interview_result['success']:
            # JD was enhanced, but interview generation failed
            return jsonify({
                'success': False,
                'error': interview_result.get('error'),
                'job_description_id': jd_result['job_description_id'],
                'message': 'JD was enhanced successfully, but interview generation failed'
            }), 500
        
        total_tokens += interview_result.get('tokens_used', 0)
        
        # Return complete workflow result
        return jsonify({
            'success': True,
            'job_description_id': jd_result['job_description_id'],
            'interview_id': interview_result['interview_id'],
            'req_id': data['req_id'],
            'interview': interview_result['interview'],
            'total_tokens_used': total_tokens,
            'created_at': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Error in workflow_full_jd_and_interview: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# HEALTH CHECK
# ============================================================================

@interview_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify service is running.
    """
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200
