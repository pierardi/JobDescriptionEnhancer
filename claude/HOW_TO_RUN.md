# How to Run This Project - Complete Guide

## 🎯 Three Ways to Explore This System

You have **three options** to see how this system works:

1. **Quick Demo (No API Key Needed)** - See what it does in 30 seconds ⚡
2. **Automated Setup** - Get running with real API in 5 minutes 🚀
3. **Manual Setup** - Full control over every step 🛠️

---

## Option 1: Quick Demo (No API Key Needed) ⚡

**Best for:** Just want to see what this does

```bash
# 1. Install dependencies (if not already done)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Run the demo
python demo.py
```

**What you'll see:**
- ✅ Job description enhancement with WORK methodology
- ✅ Interview question generation (5 questions with criteria)
- ✅ Database records created
- ✅ Complete workflow demonstration
- ⚡ No Claude API key required (uses mock mode)

**Time:** 30 seconds

---

## Option 2: Automated Setup (Recommended) 🚀

**Best for:** Want to test with real Claude API quickly

### Step 1: Run Setup Script

```bash
./setup.sh
```

This will:
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Create .env configuration file
- ✅ Initialize database

### Step 2: Add Your Claude API Key

Get your API key from: https://console.anthropic.com/

Then edit the `.env` file:
```bash
nano .env
# or use your favorite editor
```

Change this line:
```
CLAUDE_API_KEY=your-api-key-here
```

To your actual key:
```
CLAUDE_API_KEY=your-anthropic-api-key
```

Save and exit.

### Step 3: Start the Server

```bash
source venv/bin/activate
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
✅ Database initialized
```

### Step 4: Test It

**Option A - Quick Browser Test:**
```
http://localhost:5000/health
```

**Option B - Full Test Suite:**
```bash
# In a new terminal
source venv/bin/activate
python test_client.py
```

**Time:** 5 minutes

---

## Option 3: Manual Setup 🛠️

**Best for:** Want full control and understanding

### 1. Check Prerequisites

```bash
python3 --version  # Should be 3.9+
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create Environment Configuration

Copy the example file:
```bash
cp _env.example .env
```

Edit `.env`:
```bash
nano .env
```

**Required Settings:**
```env
FLASK_ENV=development
FLASK_APP=app.py
DATABASE_URL=sqlite:///techscreen.db
CLAUDE_API_KEY=your-anthropic-api-key
CLAUDE_MODEL=claude-opus-4-1
CLAUDE_MAX_TOKENS=4000
```

### 5. Initialize Database

```bash
python3 << 'EOF'
from app import create_app
from models import db

app = create_app('development')
with app.app_context():
    db.create_all()
    print("✅ Database initialized!")
EOF
```

### 6. Start the Application

```bash
python app.py
```

### 7. Test the API

**Basic Health Check:**
```bash
curl http://localhost:5000/health
```

**Full Test:**
```bash
# New terminal
source venv/bin/activate
python test_client.py
```

**Time:** 10 minutes

---

## 🧪 Testing the System

Once running, you have several ways to test:

### 1. Test Client (Automated)
```bash
python test_client.py
```
Tests all endpoints automatically.

### 2. Manual API Calls

**Enhance a Job Description:**
```bash
curl -X POST http://localhost:5000/api/interview/jd/enhance \
  -H "X-User-ID: test-user" \
  -H "X-User-Role: admin" \
  -H "Content-Type: application/json" \
  -d '{
    "req_id": "REQ-TEST-001",
    "basic_title": "Senior Software Engineer",
    "basic_description": "We need a senior engineer with microservices experience",
    "work_output": "Design and build microservices handling 10k req/sec",
    "work_role": "Lead backend architecture, mentor juniors",
    "work_knowledge": "Kafka, PostgreSQL, Spring Boot",
    "work_competencies": "System design, problem solving"
  }'
```

**Generate Interview:**
```bash
curl -X POST http://localhost:5000/api/interview/generate \
  -H "X-User-ID: test-user" \
  -H "X-User-Role: admin" \
  -H "Content-Type: application/json" \
  -d '{
    "req_id": "REQ-TEST-001",
    "job_description_id": 1,
    "interview_name": "Test Interview"
  }'
```

**Complete Workflow (Both Together):**
```bash
curl -X POST http://localhost:5000/api/interview/workflow/full \
  -H "X-User-ID: test-user" \
  -H "X-User-Role: admin" \
  -H "Content-Type: application/json" \
  -d '{
    "req_id": "REQ-FULL-001",
    "basic_title": "Full Stack Engineer",
    "basic_description": "Need full stack engineer",
    "work_output": "Build full-stack apps",
    "work_role": "Lead development",
    "work_knowledge": "React, Node.js, PostgreSQL",
    "work_competencies": "Full-stack design",
    "interview_name": "Full Stack Interview"
  }'
```

### 3. Browser-Based Testing

Install a REST client like:
- **Postman** - https://www.postman.com/
- **Insomnia** - https://insomnia.rest/
- **Thunder Client** (VS Code extension)

Import these endpoints and test interactively.

---

## 📊 Viewing Your Data

### SQLite Database (Default)

```bash
# Install SQLite CLI if needed
# Mac: brew install sqlite3
# Ubuntu: sudo apt install sqlite3

# Open database
sqlite3 techscreen.db

# View tables
.tables

# View job descriptions
SELECT id, req_id, basic_title FROM job_descriptions;

# View interviews
SELECT id, req_id, interview_name FROM interviews;

# View questions
SELECT interview_id, question_number, question_text FROM interview_questions LIMIT 3;

# Exit
.quit
```

### MySQL Database (Production)

If you switch to MySQL:

```bash
mysql -u username -p techscreen_db

SHOW TABLES;
SELECT * FROM job_descriptions;
SELECT * FROM interviews;
```

---

## 🔧 Configuration Options

### Database Options

**SQLite (Testing):**
```env
DATABASE_URL=sqlite:///techscreen.db
```

**MySQL (Production):**
```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/techscreen_db
```

**PostgreSQL:**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/techscreen_db
```

### Claude Model Options

Available models:
```env
# Highest quality, most expensive
CLAUDE_MODEL=claude-opus-4-1

# Balanced (recommended)
CLAUDE_MODEL=claude-sonnet-4-5

# Fastest, cheapest
CLAUDE_MODEL=claude-haiku-4-5
```

### Feature Flags

```env
# Enable/disable question caching
ENABLE_QUESTION_CACHE=True

# Async processing (for production)
ASYNC_PROCESSING=False

# Show SQL queries (debugging)
SQLALCHEMY_ECHO=True
```

---

## 🐛 Common Issues & Solutions

### Issue: "Module not found"
**Solution:**
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "CLAUDE_API_KEY not found"
**Solution:**
```bash
# Check .env file exists
ls -la .env

# Check key is set
grep CLAUDE_API_KEY .env

# Make sure you saved the file after editing
```

### Issue: "Port 5000 already in use"
**Solution:**
```bash
# Find process using port 5000
lsof -ti:5000

# Kill it
kill $(lsof -ti:5000)

# Or use a different port
# Edit app.py, change last line to:
# app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: "Database locked" (SQLite)
**Solution:**
```bash
# Stop the Flask app
# Delete database
rm techscreen.db

# Restart Flask app (will recreate DB)
python app.py
```

### Issue: "Claude API rate limit"
**Solution:**
- Wait a few seconds and retry
- Check your API usage at https://console.anthropic.com/
- Consider caching (ENABLE_QUESTION_CACHE=True)

### Issue: "Import error with anthropic"
**Solution:**
```bash
pip install --upgrade anthropic
```

---

## 📚 Documentation Files

After running, explore these docs:

| File | Purpose |
|------|---------|
| `QUICK_START.md` | Fast setup guide |
| `README.md` | Complete API documentation |
| `WORK_METHODOLOGY_GUIDE.md` | How to write good WORK inputs |
| `TWO_WORKFLOWS.md` | Understand the two workflows |
| `INTEGRATION_GUIDE_FOR_PETER.md` | How to integrate into your app |
| `CHANGES_MADE.md` | What was built and why |

---

## 🎯 What You Can Do

Once running, the system can:

1. **Enhance Job Descriptions**
   - Input: Basic JD + WORK methodology inputs
   - Output: Detailed, deliverable-focused JD

2. **Generate Interviews**
   - Input: Enhanced JD
   - Output: 5 questions with 8-10 evaluation criteria each

3. **Complete Workflow**
   - Input: Basic JD + WORK inputs
   - Output: Enhanced JD + Full Interview (one call)

4. **Store & Retrieve**
   - All JDs and interviews stored in database
   - Retrieve by requisition ID or interview ID

---

## 💰 API Costs

Claude API is pay-as-you-go:

| Operation | Tokens | Cost (approx) |
|-----------|--------|---------------|
| JD Enhancement | ~1,200-1,500 | $0.05-0.10 |
| Interview Generation | ~2,000-2,500 | $0.10-0.15 |
| Complete Workflow | ~3,200-4,000 | $0.15-0.25 |

Monitor usage at: https://console.anthropic.com/

---

## 🚀 Production Deployment

For production use:

1. **Switch to MySQL**
   ```sql
   CREATE DATABASE techscreen_db;
   ```

2. **Use Production WSGI Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'
   ```

3. **Set Up Nginx Reverse Proxy**
   ```nginx
   location /api/interview {
       proxy_pass http://localhost:5000;
   }
   ```

4. **Enable HTTPS**
   - Use Let's Encrypt
   - Configure SSL certificates

5. **Set Production Config**
   ```env
   FLASK_ENV=production
   DEBUG=False
   ```

See `INTEGRATION_GUIDE_FOR_PETER.md` for full production setup.

---

## ✅ Success Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed from requirements.txt
- [ ] .env file created with Claude API key
- [ ] Database initialized (SQLite or MySQL)
- [ ] Flask app starts without errors
- [ ] Health endpoint responds (http://localhost:5000/health)
- [ ] Test client runs successfully
- [ ] Can enhance a job description
- [ ] Can generate an interview
- [ ] Data appears in database

---

## 🆘 Still Need Help?

1. **Check the logs** - Look at Flask console output for errors
2. **Run the demo** - `python demo.py` to see expected behavior
3. **Review docs** - All documentation is in the project
4. **Test incrementally** - Start with health check, then simple endpoints
5. **Check environment** - Verify .env settings are correct

---

## 🎉 You're Ready!

Pick your path:
- **Quick look?** → Run `python demo.py`
- **Fast setup?** → Run `./setup.sh`
- **Full control?** → Follow manual steps

Then explore the system and integrate it into your application!

Happy interviewing! 🚀
