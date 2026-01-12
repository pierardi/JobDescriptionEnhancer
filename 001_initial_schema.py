"""
Alembic migration for creating the initial schema.
Generated for interview generation system.

To run this migration:
    alembic upgrade head
"""

from alembic import op
import sqlalchemy as sa


def upgrade():
    """Create all tables for interview generation system."""
    
    # Create job_descriptions table
    op.create_table(
        'job_descriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('req_id', sa.String(255), nullable=False, unique=True),
        sa.Column('basic_title', sa.String(255), nullable=False),
        sa.Column('basic_description', sa.Text(), nullable=False),
        sa.Column('basic_department', sa.String(255), nullable=True),
        sa.Column('basic_level', sa.String(50), nullable=True),
        sa.Column('work_output', sa.Text(), nullable=True),
        sa.Column('work_role', sa.Text(), nullable=True),
        sa.Column('work_knowledge', sa.Text(), nullable=True),
        sa.Column('work_competencies', sa.Text(), nullable=True),
        sa.Column('enhanced_title', sa.String(255), nullable=True),
        sa.Column('enhanced_description', sa.Text(), nullable=True),
        sa.Column('created_by_user_id', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('enhanced_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_job_descriptions_req_id', 'job_descriptions', ['req_id'])
    op.create_index('ix_job_descriptions_created_by_user_id', 'job_descriptions', ['created_by_user_id'])
    
    # Create interviews table
    op.create_table(
        'interviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('job_description_id', sa.Integer(), nullable=False),
        sa.Column('req_id', sa.String(255), nullable=False),
        sa.Column('interview_name', sa.String(255), nullable=False),
        sa.Column('created_by_user_id', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(50), nullable=True),
        sa.Column('version', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['job_description_id'], ['job_descriptions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_interviews_job_description_id', 'interviews', ['job_description_id'])
    op.create_index('ix_interviews_req_id', 'interviews', ['req_id'])
    op.create_index('ix_interviews_created_by_user_id', 'interviews', ['created_by_user_id'])
    
    # Create interview_questions table
    op.create_table(
        'interview_questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('interview_id', sa.Integer(), nullable=False),
        sa.Column('question_number', sa.Integer(), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('question_type', sa.String(50), nullable=True),
        sa.Column('criteria', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['interview_id'], ['interviews.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_interview_questions_interview_id', 'interview_questions', ['interview_id'])
    
    # Create question_cache table
    op.create_table(
        'question_cache',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cache_key', sa.String(255), nullable=False, unique=True),
        sa.Column('request_hash', sa.String(255), nullable=False),
        sa.Column('topic', sa.String(255), nullable=False),
        sa.Column('skill_level', sa.String(50), nullable=True),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('criteria', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
        sa.Column('usage_count', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_question_cache_cache_key', 'question_cache', ['cache_key'])
    op.create_index('ix_question_cache_request_hash', 'question_cache', ['request_hash'])
    
    # Create generation_logs table
    op.create_table(
        'generation_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('operation_type', sa.String(50), nullable=False),
        sa.Column('req_id', sa.String(255), nullable=False),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('tokens_used', sa.Integer(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_generation_logs_req_id', 'generation_logs', ['req_id'])
    op.create_index('ix_generation_logs_user_id', 'generation_logs', ['user_id'])


def downgrade():
    """Drop all tables for interview generation system."""
    
    op.drop_index('ix_generation_logs_user_id', 'generation_logs')
    op.drop_index('ix_generation_logs_req_id', 'generation_logs')
    op.drop_table('generation_logs')
    
    op.drop_index('ix_question_cache_request_hash', 'question_cache')
    op.drop_index('ix_question_cache_cache_key', 'question_cache')
    op.drop_table('question_cache')
    
    op.drop_index('ix_interview_questions_interview_id', 'interview_questions')
    op.drop_table('interview_questions')
    
    op.drop_index('ix_interviews_created_by_user_id', 'interviews')
    op.drop_index('ix_interviews_req_id', 'interviews')
    op.drop_index('ix_interviews_job_description_id', 'interviews')
    op.drop_table('interviews')
    
    op.drop_index('ix_job_descriptions_created_by_user_id', 'job_descriptions')
    op.drop_index('ix_job_descriptions_req_id', 'job_descriptions')
    op.drop_table('job_descriptions')
