# Integration Guide for VP Engineering

## Quick Summary

You have a complete, production-ready Python/Flask module that implements:
- JD enhancement using WORK methodology (Claude)
- Interview generation (5 questions, 8-10 criteria each)
- Question caching for optimization
- Comprehensive error handling and logging
- Full database schema with audit trails

**Estimated integration time: 2-3 hours**

---

## File-by-File Integration Checklist

### 1. Core Application Files

- [ ] `app.py` - Flask application factory. Either merge with your existing app factory OR use as-is if you're starting fresh
- [ ] `config.py` - Configuration management. Adapt to use your existing config system if you have one
- [ ] `models.py` - SQLAlchemy models. Add these tables to your existing `models.py` or import this module

### 2. Business Logic (Services)

- [ ] `claude_client.py` - Claude API client. If you already have Claude integration, check if it matches this pattern
- [ ] `jd_enhancement_service.py` - JD enhancement logic. Standalone, no dependencies except models and claude_client
- [ ] `interview_generation_service.py` - Interview generation logic. Depends on models, claude_client, and prompts

### 3. API Layer

- [ ] `interview_routes.py` - Flask blueprint with all endpoints. Check auth decorators (@require_admin, @require_auth) against your system
  - Update decorators to use your actual auth middleware
  - Customize error responses if needed
  - Add your own logging if you have a centralized logging system

### 4. Supporting Files

- [ ] `prompts.py` - Claude prompts (JD enhancement and interview generation)
- [ ] `requirements.txt` - Add these packages to your existing requirements.txt

### 5. Database

- [ ] `001_initial_schema.py` - Alembic migration. Either:
  - Use with `alembic upgrade head` if you're using Alembic
  - OR copy the SQL and run manually

### 6. Testing & Documentation

- [ ] `test_services.py` - Unit tests. Use as reference or run `pytest` to validate
- [ ] `README.md` - Comprehensive documentation (included)
- [ ] `.env.example` - Environment template

---

## Integration Steps

### Step 1: Copy Files to Your Project Structure

```bash
# Your existing project structure
your_app/
├── app.py                      # existing
├── models/
│   └── __init__.py             # existing
│
# ADD THESE NEW FILES:
├── config.py                   # NEW
├── prompts.py                  # NEW
├── claude_client.py            # NEW
├── jd_enhancement_service.py   # NEW
├── interview_generation_service.py  # NEW
├── interview_routes.py         # NEW (or add to routes/)
└── tests/
    └── test_interview.py       # NEW
```

### Step 2: Update Your Database Models

**Option A: Merge into existing models.py**

```python
# In your existing models.py, add:
from datetime import datetime
import json

class JobDescription(db.Model):
    # Copy from models.py provided
    ...

class Interview(db.Model):
    # Copy from models.py provided
    ...

class InterviewQuestion(db.Model):
    # Copy from models.py provided
    ...

class QuestionCache(db.Model):
    # Copy from models.py provided
    ...

class GenerationLog(db.Model):
    # Copy from models.py provided
    ...
```

**Option B: Import as separate module**

```python
# In your app.py
from models import db, JobDescription, Interview, InterviewQuestion, QuestionCache, GenerationLog
```

### Step 3: Update Flask App Configuration

In your Flask app initialization (app factory):

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config  # NEW
from models import db  # Your models
from interview_routes import interview_bp  # NEW

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])  # NEW
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(interview_bp)  # NEW - Add this line
    # ... your other blueprints ...
    
    with app.app_context():
        db.create_all()
    
    return app
```

### Step 4: Database Migration

**If you're using Alembic:**

```bash
# Copy 001_initial_schema.py to your alembic/versions/ directory
cp 001_initial_schema.py alembic/versions/

# Run migration
alembic upgrade head

# Verify tables were created
mysql -u root -p techscreen_db
SHOW TABLES;
```

**If you're NOT using Alembic:**

Run the SQL from `001_initial_schema.py` manually or use Flask-Migrate.

### Step 5: Update Configuration

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
# Edit .env with:
# - CLAUDE_API_KEY (from Anthropic console)
# - DATABASE_URL (your MySQL connection string)
# - Other settings
```

### Step 6: Fix Authentication

The routes use `@require_admin` and `@require_auth` decorators. Update these to match your system:

**In `interview_routes.py`:**

```python
# FIND THIS:
def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_role = request.headers.get('X-User-Role', 'user')
        if user_role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# REPLACE WITH YOUR AUTH SYSTEM:
from flask_login import login_required, current_user
from functools import wraps

def require_admin(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:  # or your admin check
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function
```

### Step 7: Update Claude Client (Optional)

If you already have a Claude client service, you can use yours instead of `claude_client.py`:

```python
# In interview_routes.py, replace:
from claude_client import ClaudeClientService
claude_client = ClaudeClientService()

# With your own:
from your_app.services import YourClaudeClient
claude_client = YourClaudeClient()
```

### Step 8: Dependencies

Add to your `requirements.txt`:

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
SQLAlchemy==2.0.23
alembic==1.13.1
anthropic==0.25.1
python-dotenv==1.0.0
requests==2.31.0
```

Run: `pip install -r requirements.txt`

### Step 9: Test Integration

```bash
# Test the health endpoint
curl http://localhost:5000/health

# Test JD enhancement (with proper auth headers)
curl -X POST http://localhost:5000/api/interview/jd/enhance \
  -H "X-User-ID: admin123" \
  -H "X-User-Role: admin" \
  -H "Content-Type: application/json" \
  -d '{
    "req_id": "REQ-TEST-001",
    "basic_title": "Software Engineer",
    "basic_description": "We need a software engineer"
  }'

# Run tests
pytest tests/test_services.py -v
```

---

## Important Implementation Notes

### Authentication

The code includes placeholder auth decorators. You MUST update:

```python
# These functions in interview_routes.py:
- require_admin()    # Check user is admin
- require_auth()     # Check user is authenticated

# Integration points:
- request.headers.get('X-User-ID')      # Your user ID source
- request.headers.get('X-User-Role')    # Your role source
# OR use: from flask_login import current_user
```

### Claude API Key Management

Never commit `.env` to version control. Set via:
- Development: `.env` file (git ignored)
- Production: Environment variables, secrets manager, or deployment system

### Database Connection

Update `DATABASE_URL` for your MySQL setup:

```
mysql+pymysql://username:password@host:port/database_name
```

Test connection:
```python
from models import db
from app import create_app

app = create_app()
with app.app_context():
    db.session.execute('SELECT 1')
    print("Database connected!")
```

### Logging

Add to your logging configuration:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Services will log to this automatically
```

---

## Testing Your Integration

### Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_services.py::TestJDEnhancementService -v

# With coverage
pytest --cov=. --cov-report=html
```

### Manual Testing

```bash
# Start Flask app
python app.py

# Test endpoint (in another terminal)
python tests/manual_test.py
```

### Debugging

If something fails:

1. Check application logs for stack traces
2. Query `generation_logs` table for operation records
3. Check MySQL connection
4. Verify Claude API key is valid
5. Check environment variables are loaded

---

## Common Issues & Solutions

### Issue: "No module named 'models'"

**Solution:** Make sure models.py is in Python path
```python
# Add to your app.py or __init__.py
import sys
sys.path.insert(0, os.path.dirname(__file__))
```

### Issue: "Database connection error"

**Solution:** Verify DATABASE_URL:
```bash
# Test connection
mysql -u username -p password -h localhost -P 3306 techscreen_db
```

### Issue: "Claude API authentication failed"

**Solution:** Verify CLAUDE_API_KEY:
```bash
# Check it's set in .env
grep CLAUDE_API_KEY .env

# Test with simple API call
python -c "from claude_client import ClaudeClientService; c = ClaudeClientService(); c.call_claude('test', 'test')"
```

### Issue: "Interview generation returns empty questions"

**Solution:** Check Claude response parsing
```python
# In claude_client.py, add debug logging
logger.debug(f"Raw Claude response: {response_text}")
questions = self.parse_interview_response(response_text)
logger.debug(f"Parsed questions: {questions}")
```

---

## Production Checklist

Before deploying to production:

- [ ] Claude API key is configured securely
- [ ] Database is backed up
- [ ] Logging is configured
- [ ] Authentication is properly integrated
- [ ] Error handling is tested
- [ ] Database indexes are created
- [ ] Rate limiting is implemented (optional)
- [ ] Monitoring/alerts are set up
- [ ] HTTPS is enabled
- [ ] Environment variables are set correctly

---

## Support

If you run into issues:

1. Check the `README.md` for detailed documentation
2. Review logs in `generation_logs` table
3. Run tests to isolate the problem
4. Check database schema with `DESCRIBE table_name;`
5. Test Claude API independently

## Questions for Mark

If you have architecture questions after integration, prepare:
- Your existing authentication system details
- Your database naming conventions
- Whether you use Alembic for migrations
- Your logging setup
- Any existing Claude API patterns in your codebase
