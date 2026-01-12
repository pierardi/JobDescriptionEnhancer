# TechScreen Interview Generation System

A production-ready Python/Flask application that automates the creation of technical interview questions from job descriptions using AI and the WORK methodology.

## Overview

This system provides a complete workflow for:

1. **JD Enhancement** - Transform basic job descriptions into detailed, competency-focused versions using WORK methodology
2. **Interview Generation** - Create 5-question technical interviews with 8-10 evaluation criteria per question
3. **Question Caching** - Optimize API usage by caching similar questions
4. **Audit Logging** - Track all generation activities for debugging and analysis

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Flask API Layer                          │
│                  (interview_routes.py)                      │
└──────────────┬──────────────────────────────────────────────┘
               │
       ┌───────┴────────┬──────────────────┐
       │                │                  │
   ┌───▼───────┐   ┌───▼──────────┐   ┌──▼──────────┐
   │    JD     │   │  Interview   │   │   Claude    │
   │ Enhancement   │  Generation  │   │   Client    │
   │  Service  │   │  Service     │   │  Service    │
   └───────────┘   └──────────────┘   └─────────────┘
       │                │                  │
       └────────────────┼──────────────────┘
                        │
                   ┌────▼──────┐
                   │   MySQL   │
                   │ Database  │
                   └───────────┘
```

## Directory Structure

```
techscreen-interview-generator/
├── app.py                          # Flask application factory
├── config.py                       # Configuration management
├── models.py                       # SQLAlchemy database models
├── prompts.py                      # Claude API prompts
├── claude_client.py                # Claude API client service
├── jd_enhancement_service.py       # JD enhancement business logic
├── interview_generation_service.py # Interview generation business logic
├── interview_routes.py             # Flask API routes/endpoints
├── test_services.py                # Unit tests
├── 001_initial_schema.py           # Alembic migration
└── requirements.txt                # Python dependencies
```

## Setup & Installation

### Prerequisites

- Python 3.9+
- MySQL 5.7+ or MySQL 8.0+
- Claude API Key from Anthropic
- pip (Python package manager)

### 1. Environment Setup

```bash
# Clone or download the codebase
cd techscreen-interview-generator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE techscreen_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Initialize Alembic (if not already done)
alembic init alembic

# Run migrations
alembic upgrade head
```

### 3. Environment Configuration

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_APP=app.py

# Database
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/techscreen_db

# Claude API
CLAUDE_API_KEY=your-anthropic-api-key-here
CLAUDE_MODEL=claude-opus-4-1
CLAUDE_MAX_TOKENS=4000

# Feature Flags
ENABLE_QUESTION_CACHE=True
CACHE_SIMILARITY_THRESHOLD=0.85
ASYNC_PROCESSING=True
REQUEST_TIMEOUT=300

# Logging
SQLALCHEMY_ECHO=False
```

### 4. Initialize Database Schema

```bash
# Run migrations to create tables
alembic upgrade head

# Verify tables were created
mysql -u root -p techscreen_db
SHOW TABLES;
EXIT;
```

### 5. Run Tests (Optional)

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### 6. Start Development Server

```bash
# Run Flask development server
python app.py

# Server will start on http://localhost:5000
# Check health: curl http://localhost:5000/health
```

## API Endpoints

### WORKFLOW 1: JD Enhancement Only (With WORK Methodology Guidance)

**Use this when:** You want to enhance a job description using WORK methodology inputs

#### POST `/api/interview/jd/enhance`

Enhance a basic job description using WORK methodology with user guidance.

**Request Headers:**
```
X-User-ID: admin-user-id
X-User-Role: admin
Content-Type: application/json
```

**Request Body:**
```json
{
  "req_id": "REQ-12345",
  "basic_title": "Senior Software Engineer",
  "basic_description": "We are looking for a senior engineer with experience in building scalable systems...",
  "basic_department": "Engineering",
  "basic_level": "Senior",
  
  "work_output": "Design and build microservices that handle 10,000 transactions per second with real-time fraud detection",
  "work_role": "Lead backend architecture, mentor junior engineers, own service reliability and performance",
  "work_knowledge": "Kafka/RabbitMQ, PostgreSQL/NoSQL, Spring Boot, distributed systems, load balancing, API design",
  "work_competencies": "System design, problem solving, technical depth, communication, mentorship"
}
```

**WORK Fields Explanation:**
- `work_output`: **What will this person deliver/build?** The actual software systems or features
- `work_role`: **What are the key responsibilities?** The day-to-day work and leadership aspects
- `work_knowledge`: **What knowledge areas are critical?** Technologies, frameworks, concepts they need
- `work_competencies`: **What competencies are essential?** Soft skills and professional attributes

**Response (200 OK):**
```json
{
  "success": true,
  "job_description_id": 123,
  "req_id": "REQ-12345",
  "basic_jd": {
    "title": "Senior Software Engineer",
    "department": "Engineering",
    "level": "Senior",
    "description": "..."
  },
  "enhanced_jd": {
    "title": "Senior Software Engineer",
    "description": "Enhanced description with clear deliverables informed by WORK methodology..."
  },
  "work_inputs": {
    "work_output": "Design and build microservices...",
    "work_role": "Lead backend architecture...",
    "work_knowledge": "Kafka/RabbitMQ, PostgreSQL...",
    "work_competencies": "System design, problem solving..."
  },
  "tokens_used": 1250,
  "created_at": "2025-01-09T12:00:00",
  "enhanced_at": "2025-01-09T12:00:05"
}
```

**Note:** WORK fields are optional but highly recommended. With WORK inputs, Claude produces much better, more targeted enhancements.

---

### WORKFLOW 2: Complete Workflow (JD Enhancement + Interview Generation)

**Use this when:** You want to enhance a JD AND generate a 5-question interview from it

#### POST `/api/interview/workflow/full`

Complete workflow in one call: enhance JD with WORK guidance, then generate 5-question interview.

**Request Headers:**
```
X-User-ID: admin-user-id
X-User-Role: admin
Content-Type: application/json
```

**Request Body:**
```json
{
  "req_id": "REQ-12345",
  "basic_title": "Senior Software Engineer",
  "basic_description": "We are looking for a senior engineer...",
  "basic_department": "Engineering",
  "basic_level": "Senior",
  
  "work_output": "Design and build microservices handling 10k transactions/sec",
  "work_role": "Lead backend engineer, mentor juniors, own service reliability",
  "work_knowledge": "Kafka, PostgreSQL, Spring Boot, distributed systems, load balancing",
  "work_competencies": "System design, problem solving, communication, technical depth",
  
  "interview_name": "Senior Engineer Interview - Q1 2025"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "job_description_id": 123,
  "interview_id": 456,
  "req_id": "REQ-12345",
  "interview_name": "Senior Engineer Interview - Q1 2025",
  "interview": {
    "id": 456,
    "req_id": "REQ-12345",
    "interview_name": "Senior Engineer Interview - Q1 2025",
    "created_at": "2025-01-09T12:01:00",
    "status": "draft",
    "version": 1,
    "questions": [
      {
        "id": 1,
        "question_number": 1,
        "question_text": "You're designing a system to process thousands of banking transactions...",
        "question_type": "technical",
        "criteria": [
          {
            "criterion": "Microservices Architecture",
            "description": "Candidate understands how to separate concerns...",
            "is_checked": false
          },
          ...
        ]
      },
      ...
    ]
  },
  "total_tokens_used": 3350,
  "created_at": "2025-01-09T12:00:00"
}
```

#### GET `/api/interview/jd/<req_id>`

Retrieve an enhanced job description.

**Response:**
```json
{
  "success": true,
  "job_description": {
    "job_description_id": 123,
    "req_id": "REQ-12345",
    "basic_jd": {...},
    "enhanced_jd": {...},
    "created_at": "2025-01-09T12:00:00",
    "enhanced_at": "2025-01-09T12:00:05"
  }
}
```

### Interview Generation

#### POST `/api/interview/generate`

Generate a 5-question interview from an enhanced JD.

**Request Headers:**
```
X-User-ID: admin-user-id
X-User-Role: admin
Content-Type: application/json
```

**Request Body:**
```json
{
  "req_id": "REQ-12345",
  "job_description_id": 123,
  "interview_name": "Senior Engineer Interview - Q1 2025"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "interview_id": 456,
  "req_id": "REQ-12345",
  "interview_name": "Senior Engineer Interview - Q1 2025",
  "interview": {
    "id": 456,
    "req_id": "REQ-12345",
    "interview_name": "Senior Engineer Interview - Q1 2025",
    "created_at": "2025-01-09T12:01:00",
    "status": "draft",
    "version": 1,
    "questions": [
      {
        "id": 1,
        "question_number": 1,
        "question_text": "You're designing a system to process thousands of banking transactions...",
        "question_type": "technical",
        "criteria": [
          {
            "criterion": "Microservices Architecture",
            "description": "Candidate understands how to separate concerns into distinct services...",
            "is_checked": false
          },
          ...
        ]
      },
      ...
    ]
  },
  "tokens_used": 2100,
  "cached_questions": 0,
  "created_at": "2025-01-09T12:01:00"
}
```

#### GET `/api/interview/<interview_id>`

Retrieve a generated interview by ID.

**Response:**
```json
{
  "success": true,
  "interview": { ... }
}
```

#### GET `/api/interview/req/<req_id>`

Retrieve all interviews for a requisition.

**Response:**
```json
{
  "success": true,
  "interviews": [
    { ... },
    { ... }
  ]
}
```

### Combined Workflow

#### POST `/api/interview/workflow/create`

Complete workflow: Enhance JD AND generate interview in one call.

**Request Headers:**
```
X-User-ID: admin-user-id
X-User-Role: admin
Content-Type: application/json
```

**Request Body:**
```json
{
  "req_id": "REQ-12345",
  "basic_title": "Senior Software Engineer",
  "basic_description": "We are looking for...",
  "basic_department": "Engineering",
  "basic_level": "Senior",
  "interview_name": "Senior Engineer Interview - Q1 2025"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "job_description_id": 123,
  "interview_id": 456,
  "req_id": "REQ-12345",
  "interview": { ... },
  "total_tokens_used": 3350,
  "created_at": "2025-01-09T12:00:00"
}
```

### Health Check

#### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-09T12:00:00"
}
```

## Database Schema

### job_descriptions
- `id` (PK) - Auto-incrementing primary key
- `req_id` - Requisition ID from ATS (unique)
- `basic_title` - Original job title
- `basic_description` - Original job description
- `basic_department` - Department (optional)
- `basic_level` - Job level (optional)
- `enhanced_title` - Enhanced job title
- `enhanced_description` - Enhanced job description
- `created_by_user_id` - User who created
- `created_at` - Creation timestamp
- `enhanced_at` - Enhancement completion timestamp

### interviews
- `id` (PK) - Auto-incrementing primary key
- `job_description_id` (FK) - Reference to job_descriptions
- `req_id` - Requisition ID (indexed)
- `interview_name` - Name of the interview
- `created_by_user_id` - User who created
- `created_at` - Creation timestamp
- `status` - Status: 'draft', 'published', 'archived'
- `version` - Interview version

### interview_questions
- `id` (PK) - Auto-incrementing primary key
- `interview_id` (FK) - Reference to interviews
- `question_number` - Question number (1-5)
- `question_text` - The actual question
- `question_type` - Type of question (technical, behavioral, etc.)
- `criteria` - JSON array of evaluation criteria
- `created_at` - Creation timestamp

### question_cache
- `id` (PK) - Auto-incrementing primary key
- `cache_key` - Hash key for cache lookup (unique)
- `request_hash` - Hash of the request
- `topic` - Technical topic
- `skill_level` - Skill level (Intermediate, Advanced, etc.)
- `question_text` - Cached question text
- `criteria` - Cached criteria JSON
- `created_at` - Cache creation timestamp
- `last_used_at` - Last usage timestamp
- `usage_count` - Number of times used

### generation_logs
- `id` (PK) - Auto-incrementing primary key
- `operation_type` - Type of operation ('jd_enhancement', 'interview_generation')
- `req_id` - Requisition ID (indexed)
- `user_id` - User ID (indexed)
- `status` - Status: 'success', 'failed', 'in_progress'
- `error_message` - Error message if failed
- `tokens_used` - Claude API tokens used
- `started_at` - Operation start time
- `completed_at` - Operation completion time

## Configuration

Configuration is managed through `config.py` with three environments:

### Development
- Debug mode enabled
- SQL logging enabled (optional)
- Synchronous processing
- SQLite for testing

### Testing
- In-memory SQLite database
- All features enabled
- Mock Claude client

### Production
- Debug mode disabled
- Optimized logging
- Consider async task queue (Celery)
- Production database

## Error Handling

The API returns standardized error responses:

```json
{
  "success": false,
  "error": "Error description",
  "req_id": "REQ-12345"  // When applicable
}
```

### Common HTTP Status Codes

- `200` - Successful request
- `400` - Bad request (missing/invalid fields)
- `401` - Unauthorized (missing authentication)
- `403` - Forbidden (insufficient permissions)
- `404` - Resource not found
- `500` - Server error

## Performance & Optimization

### Question Caching

The system caches generated questions to avoid redundant API calls. Caching is:
- Keyed by topic + skill level
- Tracked by usage count and last used timestamp
- Configurable via `ENABLE_QUESTION_CACHE` config

### Database Indexing

Key indexes on:
- `job_descriptions.req_id` - Fast lookup by requisition
- `interviews.req_id` - Find all interviews for requisition
- `generation_logs.req_id`, `user_id` - Audit trail queries

### API Token Usage

Monitor Claude API token consumption via:
- `GenerationLog.tokens_used` - Per operation
- Logs in application output
- Consider implementing token budgeting

## Logging

The system logs all operations to console and files (with appropriate setup):

```python
import logging
logger = logging.getLogger(__name__)
logger.info("Operation completed successfully")
logger.warning("Potential issue occurred")
logger.error("Error description")
```

Access logs via application logs for audit trail.

## Integration with Existing Flask App

To integrate into your existing Flask application:

### 1. Copy Files

Copy all `.py` files into your project structure:
```
your_app/
├── app.py  (existing)
├── models.py  (NEW)
├── config.py  (NEW)
├── claude_client.py  (NEW)
├── jd_enhancement_service.py  (NEW)
├── interview_generation_service.py  (NEW)
├── interview_routes.py  (NEW)
└── prompts.py  (NEW)
```

### 2. Update Your App Initialization

In your main `app.py` or app factory:

```python
from models import db
from interview_routes import interview_bp

def create_app():
    app = Flask(__name__)
    
    # Your existing configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://...'
    
    # Initialize database
    db.init_app(app)
    
    # Register interview blueprint
    app.register_blueprint(interview_bp)
    
    with app.app_context():
        db.create_all()
    
    return app
```

### 3. Update Database Schema

Add these tables to your existing migrations:

```bash
# Use Alembic or manual SQL to add tables from 001_initial_schema.py
alembic upgrade head
```

### 4. Configure Environment Variables

Add to your `.env`:
```
CLAUDE_API_KEY=your-key
CLAUDE_MODEL=claude-opus-4-1
ENABLE_QUESTION_CACHE=True
```

### 5. Wire Authentication

Update the decorators in `interview_routes.py` to use your auth system:

```python
def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Your authentication logic here
        if not current_user.is_admin:
            return jsonify({'error': 'Admin required'}), 403
        return f(*args, **kwargs)
    return decorated
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest -v

# Run specific test file
pytest test_services.py -v

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest test_services.py::TestJDEnhancementService::test_enhance_jd_success -v
```

## Deployment

### Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
```

### Production Deployment

For production:

1. Use a production WSGI server (Gunicorn, uWSGI)
2. Use a reverse proxy (Nginx, Apache)
3. Enable HTTPS
4. Set up database backups
5. Configure logging and monitoring
6. Use environment-specific configs
7. Implement rate limiting
8. Add request validation
9. Monitor API token usage
10. Set up alerts for failures

## Troubleshooting

### "Claude API Key not found"
- Ensure `CLAUDE_API_KEY` is set in `.env`
- Verify key is valid and active in Anthropic console

### "Database connection failed"
- Check `DATABASE_URL` in `.env`
- Verify MySQL is running
- Check database credentials
- Verify database exists: `SHOW DATABASES;`

### "Module not found"
- Verify all files are in correct location
- Run `pip install -r requirements.txt`
- Check Python path and imports

### "Interview generation failed"
- Check Claude API rate limits
- Verify request tokens don't exceed limit
- Review `generation_logs` table for errors
- Check application logs for details

## Support & Contribution

For issues or questions:
1. Check application logs
2. Review `generation_logs` table
3. Test with mock Claude client
4. Contact development team

## License

Internal TechScreen tool - Proprietary
