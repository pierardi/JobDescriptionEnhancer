# Quick Start Guide - TechScreen Interview Generator

## 🚀 Get Running in 5 Minutes

This guide will get you up and running quickly with a simplified setup using SQLite (no MySQL needed for testing).

---

## Step 1: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

---

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- SQLAlchemy (database ORM)
- Anthropic SDK (Claude API)
- pytest (testing)
- Other required packages

---

## Step 3: Set Up Environment Variables

Create a `.env` file with your Claude API key:

```bash
# Quick setup for testing (creates .env file)
cat > .env << 'EOF'
# Flask Configuration
FLASK_ENV=development
FLASK_APP=app.py

# Database - Using SQLite for quick testing
DATABASE_URL=sqlite:///techscreen.db

# Claude API - GET YOUR KEY FROM: https://console.anthropic.com/
CLAUDE_API_KEY=your-api-key-here

# Model Configuration
CLAUDE_MODEL=claude-opus-4-1
CLAUDE_MAX_TOKENS=4000

# Feature Flags
ENABLE_QUESTION_CACHE=True
ASYNC_PROCESSING=False
EOF
```

**IMPORTANT:** Replace `your-api-key-here` with your actual Claude API key from https://console.anthropic.com/

---

## Step 4: Initialize Database

The app will auto-create the database when you first run it, but you can verify:

```bash
# Run a quick Python script to initialize
python3 << 'EOF'
from app import create_app
from models import db

app = create_app('development')
with app.app_context():
    db.create_all()
    print("✅ Database created successfully!")
EOF
```

---

## Step 5: Start the Server

```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
✅ Database initialized
✅ Flask app created successfully for development
```

---

## Step 6: Test It!

### Option A: Browser Test
Open your browser and go to:
```
http://localhost:5000/health
```

You should see:
```json
{
  "status": "healthy",
  "environment": "development"
}
```

### Option B: Command Line Test
```bash
curl http://localhost:5000/health
```

### Option C: Full API Test
In a new terminal (keep the server running), run the test client:

```bash
# Activate venv first
source venv/bin/activate

# Run test client
python test_client.py
```

This will test all endpoints and show you what the system does!

---

## 🎯 What You'll See

The test client will:
1. ✅ Test health endpoint
2. ✅ Enhance a job description (with WORK methodology)
3. ✅ Retrieve the enhanced JD
4. ✅ Generate a 5-question interview
5. ✅ Retrieve the interview
6. ✅ Test the complete workflow

---

## 📝 Example API Request

Once running, you can test the JD enhancement:

```bash
curl -X POST http://localhost:5000/api/interview/jd/enhance \
  -H "X-User-ID: test-user" \
  -H "X-User-Role: admin" \
  -H "Content-Type: application/json" \
  -d '{
    "req_id": "REQ-001",
    "basic_title": "Senior Software Engineer",
    "basic_description": "We need a senior engineer with microservices experience",
    "work_output": "Design and build microservices handling 10k transactions/sec",
    "work_role": "Lead backend architecture, mentor juniors",
    "work_knowledge": "Kafka, PostgreSQL, Spring Boot, distributed systems",
    "work_competencies": "System design, problem solving, technical depth"
  }'
```

---

## 🐛 Troubleshooting

### Error: "No module named 'flask'"
**Fix:** Make sure you activated the virtual environment:
```bash
source venv/bin/activate
```

### Error: "CLAUDE_API_KEY not found"
**Fix:** Make sure you:
1. Created the `.env` file
2. Added your actual Claude API key
3. Restarted the Flask server

### Error: "Port 5000 already in use"
**Fix:** Either:
1. Kill the process using port 5000: `lsof -ti:5000 | xargs kill`
2. Or change the port in `app.py` (last line): `app.run(debug=True, host='0.0.0.0', port=5001)`

### Error: "Database error"
**Fix:** Delete the database file and restart:
```bash
rm techscreen.db
python app.py
```

---

## 🎓 Next Steps

### 1. Explore the API
Check out `README.md` for complete API documentation

### 2. Test Different Workflows
- **Workflow 1:** JD Enhancement only → `/api/interview/jd/enhance`
- **Workflow 2:** Complete (JD + Interview) → `/api/interview/workflow/full`

See `TWO_WORKFLOWS.md` for details

### 3. Learn About WORK Methodology
Read `WORK_METHODOLOGY_GUIDE.md` to understand how to write better job descriptions

### 4. Integrate Into Your App
See `INTEGRATION_GUIDE_FOR_PETER.md` for integration instructions

---

## 📊 View Your Data

You can inspect the SQLite database:

```bash
# Install sqlite3 if needed
# On Mac: brew install sqlite3
# On Ubuntu: sudo apt-get install sqlite3

# Open database
sqlite3 techscreen.db

# View tables
.tables

# View job descriptions
SELECT * FROM job_descriptions;

# View interviews
SELECT * FROM interviews;

# Exit
.exit
```

---

## 🔄 Switching to MySQL (Production Setup)

When you're ready for production:

1. Install MySQL
2. Create database: `CREATE DATABASE techscreen_db;`
3. Update `.env`:
   ```
   DATABASE_URL=mysql+pymysql://username:password@localhost:3306/techscreen_db
   ```
4. Restart the app

---

## 💰 API Costs

Claude API charges based on tokens:
- JD Enhancement: ~$0.05-0.10 per request
- Interview Generation: ~$0.10-0.15 per request
- Full Workflow: ~$0.15-0.25 per request

Monitor your usage at: https://console.anthropic.com/

---

## 🆘 Need Help?

1. Check `README.md` for full documentation
2. Review `CHANGES_MADE.md` to understand what was built
3. Check logs in the console where Flask is running
4. Test with `test_client.py` to see expected behavior

---

## ✅ You're All Set!

You now have a working interview generation system that:
- ✅ Enhances job descriptions using WORK methodology
- ✅ Generates 5-question technical interviews
- ✅ Uses Claude AI for intelligent enhancement
- ✅ Stores everything in a database
- ✅ Has a complete REST API

Happy interviewing! 🎉
