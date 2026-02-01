"""
Unit tests for JD Enhancement and Interview Generation services.
Tests cover main flows, error handling, and database operations.

To run tests from project root:
    pytest backend/ -v
    pytest backend/ --cov=backend  # With coverage

To run from backend folder:
    pytest test_services.py -v
"""

import pytest
import json
from datetime import datetime
from flask import Flask
from .config import TestingConfig
from .models import db, JobDescription, Interview, InterviewQuestion
from .jd_enhancement_service import JDEnhancementService
from .interview_generation_service import InterviewGenerationService
from .claude_client import MockClaudeClient


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config.from_object(TestingConfig)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create Flask test client."""
    return app.test_client()


@pytest.fixture
def mock_claude_client():
    """Create mock Claude client."""
    return MockClaudeClient()


class TestJDEnhancementService:
    """Tests for JD Enhancement Service."""
    
    def test_enhance_jd_success(self, app, mock_claude_client):
        """Test successful JD enhancement."""
        with app.app_context():
            service = JDEnhancementService(mock_claude_client)
            
            result = service.enhance_jd(
                req_id='REQ-001',
                basic_title='Senior Engineer',
                basic_description='We need a senior engineer',
                user_id='user123',
                basic_department='Engineering',
                basic_level='Senior'
            )
            
            assert result['success'] == True
            assert result['req_id'] == 'REQ-001'
            assert 'job_description_id' in result
            assert 'enhanced_jd' in result
    
    def test_enhance_jd_creates_db_record(self, app, mock_claude_client):
        """Test that JD enhancement creates database record."""
        with app.app_context():
            service = JDEnhancementService(mock_claude_client)
            
            result = service.enhance_jd(
                req_id='REQ-002',
                basic_title='Engineer',
                basic_description='Job description',
                user_id='user123'
            )
            
            # Verify record in database
            jd = JobDescription.query.filter_by(req_id='REQ-002').first()
            assert jd is not None
            assert jd.basic_title == 'Engineer'
            assert jd.created_by_user_id == 'user123'
    
    def test_enhance_jd_with_work_inputs(self, app, mock_claude_client):
        """Test JD enhancement with WORK methodology inputs."""
        with app.app_context():
            service = JDEnhancementService(mock_claude_client)
            
            result = service.enhance_jd(
                req_id='REQ-005',
                basic_title='Senior Engineer',
                basic_description='We need a senior engineer',
                user_id='user123',
                basic_department='Engineering',
                basic_level='Senior',
                work_output='Design microservices handling 10k transactions/sec',
                work_role='Lead backend engineer, mentor juniors',
                work_knowledge='Kafka, PostgreSQL, Spring Boot',
                work_competencies='System design, problem solving'
            )
            
            assert result['success'] == True
            assert result['work_inputs']['work_output'] == 'Design microservices handling 10k transactions/sec'
            assert result['work_inputs']['work_role'] == 'Lead backend engineer, mentor juniors'
    
    def test_enhance_jd_stores_work_inputs(self, app, mock_claude_client):
        """Test that WORK inputs are stored in database."""
        with app.app_context():
            service = JDEnhancementService(mock_claude_client)
            
            work_output = 'Build distributed system'
            work_role = 'Technical lead'
            work_knowledge = 'Distributed systems'
            work_competencies = 'Leadership'
            
            result = service.enhance_jd(
                req_id='REQ-006',
                basic_title='Engineer',
                basic_description='Job description',
                user_id='user123',
                work_output=work_output,
                work_role=work_role,
                work_knowledge=work_knowledge,
                work_competencies=work_competencies
            )
            
            # Verify in database
            jd = JobDescription.query.filter_by(req_id='REQ-006').first()
            assert jd.work_output == work_output
            assert jd.work_role == work_role
            assert jd.work_knowledge == work_knowledge
            assert jd.work_competencies == work_competencies
    
    def test_enhance_jd_update_same_req_id(self, app, mock_claude_client):
        """Test that re-enhancing same req_id updates existing record."""
        with app.app_context():
            service = JDEnhancementService(mock_claude_client)
            
            # First enhancement
            result1 = service.enhance_jd(
                req_id='REQ-003',
                basic_title='Engineer',
                basic_description='First description',
                user_id='user123'
            )
            
            # Second enhancement of same req_id
            result2 = service.enhance_jd(
                req_id='REQ-003',
                basic_title='Senior Engineer',
                basic_description='Updated description',
                user_id='user456'
            )
            
            # Should have same job_description_id
            assert result1['job_description_id'] == result2['job_description_id']
            
            # Database should have only one record
            count = JobDescription.query.filter_by(req_id='REQ-003').count()
            assert count == 1
    
    def test_get_enhanced_jd(self, app, mock_claude_client):
        """Test retrieving an enhanced JD."""
        with app.app_context():
            service = JDEnhancementService(mock_claude_client)
            
            # Create JD
            service.enhance_jd(
                req_id='REQ-004',
                basic_title='Engineer',
                basic_description='Job description',
                user_id='user123'
            )
            
            # Retrieve JD
            result = service.get_enhanced_jd('REQ-004')
            
            assert result is not None
            assert result['req_id'] == 'REQ-004'
            assert 'basic_jd' in result
            assert 'enhanced_jd' in result
    
    def test_get_nonexistent_jd(self, app, mock_claude_client):
        """Test retrieving non-existent JD."""
        with app.app_context():
            service = JDEnhancementService(mock_claude_client)
            result = service.get_enhanced_jd('NONEXISTENT')
            assert result is None


class TestInterviewGenerationService:
    """Tests for Interview Generation Service."""
    
    def test_generate_interview_success(self, app, mock_claude_client):
        """Test successful interview generation."""
        with app.app_context():
            # First create a JD
            jd = JobDescription(
                req_id='REQ-005',
                basic_title='Engineer',
                basic_description='Job description',
                created_by_user_id='user123'
            )
            db.session.add(jd)
            db.session.commit()
            
            # Generate interview
            service = InterviewGenerationService(mock_claude_client)
            result = service.generate_interview(
                req_id='REQ-005',
                job_description_id=jd.id,
                user_id='user123'
            )
            
            assert result['success'] == True
            assert result['req_id'] == 'REQ-005'
            assert 'interview_id' in result
    
    def test_generate_interview_creates_questions(self, app):
        """Test that interview generation creates question records."""
        with app.app_context():
            # Create a mock client that returns valid interview data
            class MockClientWithQuestions(MockClaudeClient):
                def parse_interview_response(self, response_text):
                    return [
                        {
                            'question_number': 1,
                            'question_text': 'Question 1?',
                            'expected_answer': 'Answer 1',
                            'criteria': [
                                {'criterion': f'Criterion {i}', 'description': f'Description {i}'}
                                for i in range(1, 9)
                            ]
                        } for _ in range(5)
                    ]
            
            # Create JD
            jd = JobDescription(
                req_id='REQ-006',
                basic_title='Engineer',
                basic_description='Job description',
                created_by_user_id='user123'
            )
            db.session.add(jd)
            db.session.commit()
            
            # Generate interview with mock client
            service = InterviewGenerationService(MockClientWithQuestions())
            result = service.generate_interview(
                req_id='REQ-006',
                job_description_id=jd.id,
                user_id='user123'
            )
            
            # Verify interview and questions in database
            interview = Interview.query.filter_by(req_id='REQ-006').first()
            assert interview is not None
            assert len(interview.questions) == 5
    
    def test_get_interview(self, app, mock_claude_client):
        """Test retrieving a generated interview."""
        with app.app_context():
            # Create JD
            jd = JobDescription(
                req_id='REQ-007',
                basic_title='Engineer',
                basic_description='Job description',
                created_by_user_id='user123'
            )
            db.session.add(jd)
            db.session.commit()
            
            # Create interview
            interview = Interview(
                job_description_id=jd.id,
                req_id='REQ-007',
                interview_name='Test Interview',
                created_by_user_id='user123'
            )
            db.session.add(interview)
            db.session.commit()
            
            # Retrieve interview
            service = InterviewGenerationService(mock_claude_client)
            result = service.get_interview(interview.id)
            
            assert result is not None
            assert result['req_id'] == 'REQ-007'
            assert result['interview_name'] == 'Test Interview'
    
    def test_get_interview_by_req(self, app, mock_claude_client):
        """Test retrieving interviews by req_id."""
        with app.app_context():
            # Create JD
            jd = JobDescription(
                req_id='REQ-008',
                basic_title='Engineer',
                basic_description='Job description',
                created_by_user_id='user123'
            )
            db.session.add(jd)
            db.session.commit()
            
            # Create multiple interviews
            for i in range(3):
                interview = Interview(
                    job_description_id=jd.id,
                    req_id='REQ-008',
                    interview_name=f'Interview {i+1}',
                    created_by_user_id='user123'
                )
                db.session.add(interview)
            db.session.commit()
            
            # Retrieve interviews
            service = InterviewGenerationService(mock_claude_client)
            results = service.get_interview_by_req('REQ-008')
            
            assert results is not None
            assert len(results) == 3
    
    def test_get_nonexistent_interview(self, app, mock_claude_client):
        """Test retrieving non-existent interview."""
        with app.app_context():
            service = InterviewGenerationService(mock_claude_client)
            result = service.get_interview(9999)
            assert result is None


class TestInterviewQuestionModel:
    """Tests for InterviewQuestion model."""
    
    def test_question_to_dict(self, app, mock_claude_client):
        """Test converting question to dictionary."""
        with app.app_context():
            # Create JD
            jd = JobDescription(
                req_id='REQ-009',
                basic_title='Engineer',
                basic_description='Job description',
                created_by_user_id='user123'
            )
            db.session.add(jd)
            db.session.commit()
            
            # Create interview
            interview = Interview(
                job_description_id=jd.id,
                req_id='REQ-009',
                interview_name='Test',
                created_by_user_id='user123'
            )
            db.session.add(interview)
            db.session.commit()
            
            # Create question
            criteria = [
                {'criterion': 'Criterion 1', 'description': 'Description 1', 'is_checked': False}
            ]
            question = InterviewQuestion(
                interview_id=interview.id,
                question_number=1,
                question_text='Test question?',
                criteria=criteria
            )
            db.session.add(question)
            db.session.commit()
            
            # Convert to dict
            result = question.to_dict()
            
            assert result['question_number'] == 1
            assert result['question_text'] == 'Test question?'
            assert len(result['criteria']) == 1
