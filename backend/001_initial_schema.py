"""
Alembic migration for creating the initial schema.
Generated for interview generation system.
Compatible with Aurora MySQL 5.7+ and 8.0+.

To run this migration:
    alembic upgrade head
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    """Create all tables for interview generation system.
    Optimized for Aurora MySQL compatibility with utf8mb4 encoding.
    """
    
    # Get the bind (connection) to check database type
    bind = op.get_bind()
    is_mysql = bind.dialect.name == 'mysql'
    
    # Define JSON type: Aurora MySQL 5.7 uses LONGTEXT for JSON, 8.0+ uses native JSON
    # SQLAlchemy's mysql.JSON automatically handles version differences
    if is_mysql:
        json_type = mysql.JSON
    else:
        json_type = sa.JSON
    
    # Table creation options for Aurora MySQL
    mysql_table_args = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci',
        'mysql_engine': 'InnoDB'
    } if is_mysql else {}
    
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
        sa.PrimaryKeyConstraint('id'),
        **mysql_table_args
    )
    op.create_index('ix_job_descriptions_req_id', 'job_descriptions', ['req_id'])
    op.create_index('ix_job_descriptions_created_by_user_id', 'job_descriptions', ['created_by_user_id'])
    
    # Set charset/collation for MySQL after table creation
    if is_mysql:
        op.execute("ALTER TABLE job_descriptions CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    
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
        sa.ForeignKeyConstraint(['job_description_id'], ['job_descriptions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        **mysql_table_args
    )
    op.create_index('ix_interviews_job_description_id', 'interviews', ['job_description_id'])
    op.create_index('ix_interviews_req_id', 'interviews', ['req_id'])
    op.create_index('ix_interviews_created_by_user_id', 'interviews', ['created_by_user_id'])
    
    # Set charset/collation for MySQL after table creation
    if is_mysql:
        op.execute("ALTER TABLE interviews CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    
    # Create interview_questions table
    op.create_table(
        'interview_questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('interview_id', sa.Integer(), nullable=False),
        sa.Column('question_number', sa.Integer(), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('question_type', sa.String(50), nullable=True),
        sa.Column('criteria', json_type, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['interview_id'], ['interviews.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        **mysql_table_args
    )
    op.create_index('ix_interview_questions_interview_id', 'interview_questions', ['interview_id'])
    
    # Set charset/collation for MySQL after table creation
    if is_mysql:
        op.execute("ALTER TABLE interview_questions CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    
    # Create question_cache table
    op.create_table(
        'question_cache',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cache_key', sa.String(255), nullable=False, unique=True),
        sa.Column('request_hash', sa.String(255), nullable=False),
        sa.Column('topic', sa.String(255), nullable=False),
        sa.Column('skill_level', sa.String(50), nullable=True),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('criteria', json_type, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
        sa.Column('usage_count', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        **mysql_table_args
    )
    op.create_index('ix_question_cache_cache_key', 'question_cache', ['cache_key'])
    op.create_index('ix_question_cache_request_hash', 'question_cache', ['request_hash'])
    
    # Set charset/collation for MySQL after table creation
    if is_mysql:
        op.execute("ALTER TABLE question_cache CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    
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
        sa.PrimaryKeyConstraint('id'),
        **mysql_table_args
    )
    op.create_index('ix_generation_logs_req_id', 'generation_logs', ['req_id'])
    op.create_index('ix_generation_logs_user_id', 'generation_logs', ['user_id'])
    
    # Set charset/collation for MySQL after table creation
    if is_mysql:
        op.execute("ALTER TABLE generation_logs CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")


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
