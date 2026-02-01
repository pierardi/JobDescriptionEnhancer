-- ============================================================================
-- MySQL Compatible DDL Schema
-- TechScreen Interview Generation System
-- Compatible with RDS MySQL 5.7+ and 8.0+, Aurora MySQL 5.7+ and 8.0+
-- ============================================================================
-- 
-- Usage:
--   1. Create database first:
--      CREATE DATABASE jdenhancer CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--   
--   2. Run this script:
--      mysql -u username -p -h rds-endpoint jdenhancer < schema.sql
--   
--   Or from MySQL client:
--      USE techscreen_db;
--      source schema.sql;
--
-- ============================================================================

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET foreign_key_checks = 1;

-- ============================================================================
-- Table: job_descriptions
-- Stores both basic and enhanced job descriptions with WORK methodology inputs
-- ============================================================================
DROP TABLE IF EXISTS job_descriptions;

CREATE TABLE job_descriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    req_id VARCHAR(255) NOT NULL UNIQUE COMMENT 'Requisition ID from ATS (unique)',
    basic_title VARCHAR(255) NOT NULL COMMENT 'Original job title',
    basic_description TEXT NOT NULL COMMENT 'Original job description',
    basic_department VARCHAR(255) DEFAULT NULL COMMENT 'Department name',
    basic_level VARCHAR(50) DEFAULT NULL COMMENT 'Job level (Junior, Senior, Lead, etc.)',
    
    -- WORK Methodology Inputs
    work_output TEXT DEFAULT NULL COMMENT 'What will this person deliver/build?',
    work_role TEXT DEFAULT NULL COMMENT 'What are the key responsibilities/roles?',
    work_knowledge TEXT DEFAULT NULL COMMENT 'What knowledge areas are critical?',
    work_competencies TEXT DEFAULT NULL COMMENT 'What competencies are essential?',
    
    -- Enhanced JD (after WORK methodology is applied)
    enhanced_title VARCHAR(255) DEFAULT NULL COMMENT 'Enhanced job title',
    enhanced_description TEXT DEFAULT NULL COMMENT 'Enhanced job description',
    
    -- Metadata
    created_by_user_id VARCHAR(255) NOT NULL COMMENT 'User who created this JD',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation timestamp',
    enhanced_at DATETIME DEFAULT NULL COMMENT 'Enhancement completion timestamp',
    
    -- Indexes
    INDEX ix_job_descriptions_req_id (req_id),
    INDEX ix_job_descriptions_created_by_user_id (created_by_user_id)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Job descriptions with basic and enhanced versions';

-- ============================================================================
-- Table: interviews
-- Stores complete 5-question interviews generated from enhanced job descriptions
-- ============================================================================
DROP TABLE IF EXISTS interviews;

CREATE TABLE interviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_description_id INT NOT NULL COMMENT 'Reference to job_descriptions',
    req_id VARCHAR(255) NOT NULL COMMENT 'Requisition ID (indexed for fast lookup)',
    
    -- Interview metadata
    interview_name VARCHAR(255) NOT NULL COMMENT 'Name of the interview',
    created_by_user_id VARCHAR(255) NOT NULL COMMENT 'User who created this interview',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation timestamp',
    
    -- Interview status
    status VARCHAR(50) DEFAULT 'draft' COMMENT 'Status: draft, published, archived',
    version INT DEFAULT 1 COMMENT 'Interview version number',
    
    -- Indexes
    INDEX ix_interviews_job_description_id (job_description_id),
    INDEX ix_interviews_req_id (req_id),
    INDEX ix_interviews_created_by_user_id (created_by_user_id),
    
    -- Foreign key with cascade delete
    FOREIGN KEY (job_description_id) 
        REFERENCES job_descriptions(id) 
        ON DELETE CASCADE
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Generated interviews with 5 questions each';

-- ============================================================================
-- Table: interview_questions
-- Individual questions within an interview, each with 8-10 evaluation criteria
-- ============================================================================
DROP TABLE IF EXISTS interview_questions;

CREATE TABLE interview_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    interview_id INT NOT NULL COMMENT 'Reference to interviews',
    
    -- Question content
    question_number INT NOT NULL COMMENT 'Question number (1-5)',
    question_text TEXT NOT NULL COMMENT 'The actual question text',
    question_type VARCHAR(50) DEFAULT 'technical' COMMENT 'Type: technical, behavioral, etc.',
    
    -- Criteria stored as JSON
    -- Format: [
    --   {
    --     "criterion": "Criterion Name",
    --     "description": "What to look for",
    --     "is_checked": false
    --   },
    --   ...
    -- ]
    -- Note: JSON type is native in MySQL 5.7.8+ and 8.0+ (RDS MySQL and Aurora MySQL)
    -- For earlier versions, this would be LONGTEXT
    criteria JSON NOT NULL COMMENT 'Evaluation criteria (8-10 per question)',
    
    -- Metadata
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation timestamp',
    
    -- Indexes
    INDEX ix_interview_questions_interview_id (interview_id),
    
    -- Foreign key with cascade delete
    FOREIGN KEY (interview_id) 
        REFERENCES interviews(id) 
        ON DELETE CASCADE,
    
    -- Ensure question numbers are unique per interview and between 1-5
    UNIQUE KEY uk_interview_question_number (interview_id, question_number)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Individual interview questions with evaluation criteria';

-- ============================================================================
-- Table: question_cache
-- Caches generated questions to optimize API usage for similar requests
-- ============================================================================
DROP TABLE IF EXISTS question_cache;

CREATE TABLE question_cache (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Cache key (hash of the question generation request)
    cache_key VARCHAR(255) NOT NULL UNIQUE COMMENT 'Hash key for cache lookup',
    request_hash VARCHAR(255) NOT NULL COMMENT 'Hash of the original request',
    
    -- Original request details
    topic VARCHAR(255) NOT NULL COMMENT 'Technical topic (e.g., CI/CD, React, Microservices)',
    skill_level VARCHAR(50) DEFAULT NULL COMMENT 'Skill level (Intermediate, Advanced, etc.)',
    
    -- Cached response
    question_text TEXT NOT NULL COMMENT 'Cached question text',
    criteria JSON NOT NULL COMMENT 'Cached evaluation criteria',
    
    -- Metadata
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Cache creation timestamp',
    last_used_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Last usage timestamp',
    usage_count INT DEFAULT 1 COMMENT 'Number of times this cache was used',
    
    -- Indexes
    INDEX ix_question_cache_cache_key (cache_key),
    INDEX ix_question_cache_request_hash (request_hash)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Cache for generated questions to reduce API calls';

-- ============================================================================
-- Table: generation_logs
-- Audit log for tracking all JD and interview generation activities
-- ============================================================================
DROP TABLE IF EXISTS generation_logs;

CREATE TABLE generation_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Operation details
    operation_type VARCHAR(50) NOT NULL COMMENT 'Type: jd_enhancement, interview_generation',
    req_id VARCHAR(255) NOT NULL COMMENT 'Requisition ID',
    user_id VARCHAR(255) NOT NULL COMMENT 'User ID who performed the operation',
    
    -- Status and timing
    status VARCHAR(50) NOT NULL COMMENT 'Status: success, failed, in_progress',
    error_message TEXT DEFAULT NULL COMMENT 'Error message if operation failed',
    tokens_used INT DEFAULT NULL COMMENT 'Claude API tokens consumed',
    
    -- Timestamps
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Operation start time',
    completed_at DATETIME DEFAULT NULL COMMENT 'Operation completion time',
    
    -- Indexes for fast queries
    INDEX ix_generation_logs_req_id (req_id),
    INDEX ix_generation_logs_user_id (user_id),
    INDEX ix_generation_logs_operation_type (operation_type),
    INDEX ix_generation_logs_status (status),
    INDEX ix_generation_logs_started_at (started_at)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Audit log for all generation operations';

-- ============================================================================
-- Verification Queries
-- ============================================================================

-- Show all created tables
SHOW TABLES;

-- Verify charset and collation for all tables
SELECT 
    TABLE_NAME,
    TABLE_COLLATION,
    TABLE_COMMENT
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME IN (
      'job_descriptions', 
      'interviews', 
      'interview_questions', 
      'question_cache', 
      'generation_logs'
  )
ORDER BY TABLE_NAME;

-- Verify foreign key constraints
SELECT 
    CONSTRAINT_NAME,
    TABLE_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME,
    DELETE_RULE
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = DATABASE()
  AND REFERENCED_TABLE_NAME IS NOT NULL
ORDER BY TABLE_NAME, CONSTRAINT_NAME;

-- Show all indexes
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    COLUMN_NAME,
    SEQ_IN_INDEX,
    NON_UNIQUE
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME IN (
      'job_descriptions', 
      'interviews', 
      'interview_questions', 
      'question_cache', 
      'generation_logs'
  )
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;

-- ============================================================================
-- End of Schema
-- ============================================================================
