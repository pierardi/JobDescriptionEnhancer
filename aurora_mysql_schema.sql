-- Aurora MySQL Compatible Schema for Interview Generation System
-- Compatible with Aurora MySQL 5.7+ and 8.0+
-- 
-- Usage:
--   mysql -u username -p database_name < aurora_mysql_schema.sql
-- 
-- Or from MySQL client:
--   source aurora_mysql_schema.sql;

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- Create job_descriptions table
CREATE TABLE IF NOT EXISTS job_descriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    req_id VARCHAR(255) NOT NULL UNIQUE,
    basic_title VARCHAR(255) NOT NULL,
    basic_description TEXT NOT NULL,
    basic_department VARCHAR(255) DEFAULT NULL,
    basic_level VARCHAR(50) DEFAULT NULL,
    work_output TEXT DEFAULT NULL,
    work_role TEXT DEFAULT NULL,
    work_knowledge TEXT DEFAULT NULL,
    work_competencies TEXT DEFAULT NULL,
    enhanced_title VARCHAR(255) DEFAULT NULL,
    enhanced_description TEXT DEFAULT NULL,
    created_by_user_id VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT NULL,
    enhanced_at DATETIME DEFAULT NULL,
    INDEX ix_job_descriptions_req_id (req_id),
    INDEX ix_job_descriptions_created_by_user_id (created_by_user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create interviews table
CREATE TABLE IF NOT EXISTS interviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_description_id INT NOT NULL,
    req_id VARCHAR(255) NOT NULL,
    interview_name VARCHAR(255) NOT NULL,
    created_by_user_id VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT NULL,
    status VARCHAR(50) DEFAULT 'draft',
    version INT DEFAULT 1,
    INDEX ix_interviews_job_description_id (job_description_id),
    INDEX ix_interviews_req_id (req_id),
    INDEX ix_interviews_created_by_user_id (created_by_user_id),
    FOREIGN KEY (job_description_id) REFERENCES job_descriptions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create interview_questions table
-- Note: For Aurora MySQL 5.7, JSON is stored as LONGTEXT
--       For Aurora MySQL 8.0+, JSON is a native type
CREATE TABLE IF NOT EXISTS interview_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    interview_id INT NOT NULL,
    question_number INT NOT NULL,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) DEFAULT 'technical',
    criteria JSON NOT NULL,
    created_at DATETIME DEFAULT NULL,
    INDEX ix_interview_questions_interview_id (interview_id),
    FOREIGN KEY (interview_id) REFERENCES interviews(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create question_cache table
CREATE TABLE IF NOT EXISTS question_cache (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cache_key VARCHAR(255) NOT NULL UNIQUE,
    request_hash VARCHAR(255) NOT NULL,
    topic VARCHAR(255) NOT NULL,
    skill_level VARCHAR(50) DEFAULT NULL,
    question_text TEXT NOT NULL,
    criteria JSON NOT NULL,
    created_at DATETIME DEFAULT NULL,
    last_used_at DATETIME DEFAULT NULL,
    usage_count INT DEFAULT 1,
    INDEX ix_question_cache_cache_key (cache_key),
    INDEX ix_question_cache_request_hash (request_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create generation_logs table
CREATE TABLE IF NOT EXISTS generation_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operation_type VARCHAR(50) NOT NULL,
    req_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    error_message TEXT DEFAULT NULL,
    tokens_used INT DEFAULT NULL,
    started_at DATETIME DEFAULT NULL,
    completed_at DATETIME DEFAULT NULL,
    INDEX ix_generation_logs_req_id (req_id),
    INDEX ix_generation_logs_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Verify tables were created
SHOW TABLES;

-- Verify charset and collation
SELECT TABLE_NAME, TABLE_COLLATION 
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME IN ('job_descriptions', 'interviews', 'interview_questions', 'question_cache', 'generation_logs');
