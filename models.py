from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class JobDescription(db.Model):
    """
    Stores both basic and enhanced job descriptions.
    Includes WORK methodology inputs (Work Output, Roles, Knowledge, Competencies).
    """
    __tablename__ = 'job_descriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    req_id = db.Column(db.String(255), nullable=False, unique=True, index=True)
    
    # Original JD
    basic_title = db.Column(db.String(255), nullable=False)
    basic_description = db.Column(db.Text, nullable=False)
    basic_department = db.Column(db.String(255))
    basic_level = db.Column(db.String(50))  # e.g., "Junior", "Senior", "Lead"
    
    # WORK Methodology Inputs (from user)
    # These guide the enhancement process and make it more accurate
    work_output = db.Column(db.Text, nullable=True)  # What will this person deliver/build?
    work_role = db.Column(db.Text, nullable=True)    # What are the key responsibilities/roles?
    work_knowledge = db.Column(db.Text, nullable=True)  # What knowledge areas are critical?
    work_competencies = db.Column(db.Text, nullable=True)  # What competencies are essential?
    
    # Enhanced JD (after WORK methodology is applied)
    enhanced_title = db.Column(db.String(255))
    enhanced_description = db.Column(db.Text)
    
    # Metadata
    created_by_user_id = db.Column(db.String(255), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    enhanced_at = db.Column(db.DateTime)
    
    # Relationships
    interviews = db.relationship('Interview', backref='job_description', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<JobDescription {self.req_id} - {self.basic_title}>'


class Interview(db.Model):
    """
    Stores the complete 5-question interview generated from an enhanced job description.
    """
    __tablename__ = 'interviews'
    
    id = db.Column(db.Integer, primary_key=True)
    job_description_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'), nullable=False, index=True)
    req_id = db.Column(db.String(255), nullable=False, index=True)
    
    # Metadata
    interview_name = db.Column(db.String(255), nullable=False)
    created_by_user_id = db.Column(db.String(255), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Interview status
    status = db.Column(db.String(50), default='draft')  # draft, published, archived
    version = db.Column(db.Integer, default=1)
    
    # Relationships
    questions = db.relationship('InterviewQuestion', backref='interview', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert interview to dictionary with all questions"""
        return {
            'id': self.id,
            'req_id': self.req_id,
            'interview_name': self.interview_name,
            'created_at': self.created_at.isoformat(),
            'status': self.status,
            'version': self.version,
            'questions': [q.to_dict() for q in self.questions]
        }
    
    def __repr__(self):
        return f'<Interview {self.req_id} - {self.interview_name}>'


class InterviewQuestion(db.Model):
    """
    Individual question within an interview, with 8-10 criteria.
    """
    __tablename__ = 'interview_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interviews.id'), nullable=False, index=True)
    
    # Question content
    question_number = db.Column(db.Integer, nullable=False)  # 1-5
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), default='technical')  # technical, behavioral, etc.
    
    # Criteria (stored as JSON for flexibility)
    # Format: [
    #   {
    #     "criterion": "Criterion Name",
    #     "description": "1-2 sentence explanation of what to look for",
    #     "is_checked": false
    #   },
    #   ...
    # ]
    criteria = db.Column(db.JSON, nullable=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert question to dictionary"""
        return {
            'id': self.id,
            'question_number': self.question_number,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'criteria': self.criteria
        }
    
    def __repr__(self):
        return f'<InterviewQuestion {self.interview_id} - Q{self.question_number}>'


class QuestionCache(db.Model):
    """
    Caches generated questions to avoid regenerating similar questions.
    Used for optimization when multiple JDs have similar requirements.
    """
    __tablename__ = 'question_cache'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Cache key (hash of the question generation request)
    cache_key = db.Column(db.String(255), nullable=False, unique=True, index=True)
    
    # Original request details
    request_hash = db.Column(db.String(255), nullable=False, index=True)
    topic = db.Column(db.String(255), nullable=False)  # e.g., "CI/CD", "React", "Microservices"
    skill_level = db.Column(db.String(50))  # e.g., "Intermediate", "Advanced"
    
    # Cached response
    question_text = db.Column(db.Text, nullable=False)
    criteria = db.Column(db.JSON, nullable=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used_at = db.Column(db.DateTime, default=datetime.utcnow)
    usage_count = db.Column(db.Integer, default=1)
    
    def increment_usage(self):
        """Increment usage counter and update last used timestamp"""
        self.usage_count += 1
        self.last_used_at = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<QuestionCache {self.topic} - {self.skill_level}>'


class GenerationLog(db.Model):
    """
    Audit log for tracking all JD and interview generation activities.
    Useful for debugging and understanding generation patterns.
    """
    __tablename__ = 'generation_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    
    operation_type = db.Column(db.String(50), nullable=False)  # 'jd_enhancement', 'interview_generation'
    req_id = db.Column(db.String(255), nullable=False, index=True)
    user_id = db.Column(db.String(255), nullable=False, index=True)
    
    # Status and timing
    status = db.Column(db.String(50), nullable=False)  # 'success', 'failed', 'in_progress'
    error_message = db.Column(db.Text)
    tokens_used = db.Column(db.Integer)
    
    # Timestamps
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<GenerationLog {self.operation_type} - {self.req_id} - {self.status}>'
