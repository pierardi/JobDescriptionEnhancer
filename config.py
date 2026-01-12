import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://user:password@localhost/techscreen_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'False') == 'True'
    
    # Claude API
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
    CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', 'claude-opus-4-1')
    CLAUDE_MAX_TOKENS = int(os.getenv('CLAUDE_MAX_TOKENS', '4000'))
    
    # Interview Generation
    INTERVIEW_QUESTION_COUNT = 5
    QUESTION_CRITERIA_MIN = 8
    QUESTION_CRITERIA_MAX = 10
    
    # Caching
    ENABLE_QUESTION_CACHE = os.getenv('ENABLE_QUESTION_CACHE', 'True') == 'True'
    CACHE_SIMILARITY_THRESHOLD = float(os.getenv('CACHE_SIMILARITY_THRESHOLD', '0.85'))
    
    # Security
    ADMIN_ONLY_FEATURE = True  # Only admins can create interviews
    
    # Processing
    ASYNC_PROCESSING = os.getenv('ASYNC_PROCESSING', 'True') == 'True'
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '300'))  # 5 minutes

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    # Use SQLite for local development (no MySQL setup required)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///techscreen_dev.db'
    )

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    CLAUDE_API_KEY = 'test-key'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
