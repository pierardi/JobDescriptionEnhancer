# 🚀 RUN THIS PROJECT - START HERE

I've created everything you need to run this TechScreen Interview Generation System! Here's what you have:

---

## 📦 What I've Created For You

### 1. **HOW_TO_RUN.md** (⭐ START HERE)
Complete guide with **3 options**:
- **Quick Demo** (30 seconds, no API key needed)
- **Automated Setup** (5 minutes with real API)
- **Manual Setup** (full control)

### 2. **setup.sh** (Automated Setup Script)
One-command setup:
```bash
./setup.sh
```
Does everything: creates venv, installs packages, sets up database.

### 3. **demo.py** (No API Key Demo)
See what the system does without needing Claude API:
```bash
python demo.py
```

### 4. **QUICK_START.md**
Fast reference guide for getting up and running.

---

## ⚡ Fastest Way to Run (3 Steps)

### Option 1: See Demo First (No API Key)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python demo.py
```
✅ See the system work in 30 seconds!

### Option 2: Run With Real API
```bash
# 1. Auto-setup
./setup.sh

# 2. Add your Claude API key to .env
nano .env  # Add: CLAUDE_API_KEY=sk-ant-...

# 3. Start server
source venv/bin/activate
python app.py
```
✅ Full system running in 5 minutes!

---

## 🎯 What This System Does

This is a **complete AI-powered interview generation system** that:

1. **Enhances Job Descriptions** using WORK methodology
   - Takes basic JDs → Makes them specific and deliverable-focused
   - Uses Claude AI to understand what the role really needs

2. **Generates Technical Interviews**
   - Creates 5 scenario-based questions
   - Each question has 8-10 evaluation criteria
   - Directly tests job requirements

3. **Stores Everything**
   - Database of enhanced JDs
   - Interview questions and criteria
   - Full audit trail

---

## 🗂️ Project Structure

```
/mnt/project/  (Your project files)
├── app.py                          # Flask application
├── models.py                       # Database models
├── interview_routes.py             # API endpoints
├── jd_enhancement_service.py       # JD enhancement logic
├── interview_generation_service.py # Interview generation
├── claude_client.py                # Claude API client
├── config.py                       # Configuration
├── prompts.py                      # AI prompts
├── requirements.txt                # Dependencies
├── test_client.py                  # API test client
├── test_services.py                # Unit tests
│
├── README.md                       # Full documentation
├── QUICK_START.md                  # Quick setup guide
├── HOW_TO_RUN.md                   # How to run (this file)
├── WORK_METHODOLOGY_GUIDE.md       # WORK methodology
├── TWO_WORKFLOWS.md                # Workflow explanations
├── INTEGRATION_GUIDE_FOR_PETER.md  # Integration guide
│
└── My helpful additions:
    ├── setup.sh                    # Automated setup script
    └── demo.py                     # Demo without API key
```

---

## 📖 Documentation Hierarchy

**Start here:**
1. **HOW_TO_RUN.md** ← You are here!
2. **QUICK_START.md** ← Fast reference

**For understanding:**
3. **README.md** ← Complete API docs
4. **WORK_METHODOLOGY_GUIDE.md** ← How to write better JDs
5. **TWO_WORKFLOWS.md** ← Workflow choices

**For integration:**
6. **INTEGRATION_GUIDE_FOR_PETER.md** ← Add to your app
7. **CHANGES_MADE.md** ← What was built

---

## 🔑 Getting a Claude API Key

1. Go to: https://console.anthropic.com/
2. Sign up or log in
3. Go to "API Keys"
4. Create a new key
5. Copy it to your `.env` file

**Cost:** Pay-as-you-go, ~$0.15-0.25 per complete workflow

---

## ⚙️ Quick Commands Reference

```bash
# Setup
./setup.sh                          # Automated setup

# Run demo (no API key)
python demo.py                      # See what it does

# Start server
source venv/bin/activate
python app.py                       # Start Flask

# Test it
python test_client.py               # Full API test
curl http://localhost:5000/health   # Quick health check

# View database (SQLite)
sqlite3 techscreen.db
.tables                             # Show tables
SELECT * FROM job_descriptions;     # View data
.quit                               # Exit
```

---

## 🎓 Learning Path

### Beginner Path (Just exploring)
1. Run `python demo.py` to see what it does
2. Read `QUICK_START.md` 
3. Try running with real API: `./setup.sh`
4. Test with `python test_client.py`

### Developer Path (Want to integrate)
1. Run demo first: `python demo.py`
2. Get it running: `./setup.sh` + add API key
3. Read: `README.md` for API docs
4. Read: `INTEGRATION_GUIDE_FOR_PETER.md`
5. Integrate into your application

### Product Path (Understanding features)
1. Run demo: `python demo.py`
2. Read: `WORK_METHODOLOGY_GUIDE.md`
3. Read: `TWO_WORKFLOWS.md`
4. Test different scenarios with `test_client.py`

---

## 🐛 Troubleshooting

### Python/Environment Issues
```bash
# Check Python version
python3 --version  # Need 3.9+

# Create fresh venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### API Key Issues
```bash
# Check .env exists
ls -la .env

# Check key is set
cat .env | grep CLAUDE_API_KEY

# Make sure it starts with: sk-ant-api03-
```

### Port Issues
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill

# Or use different port in app.py (last line):
# app.run(debug=True, host='0.0.0.0', port=5001)
```

### Database Issues
```bash
# Reset database
rm techscreen.db
python app.py  # Will recreate
```

---

## ✅ Success Indicators

You'll know it's working when:

1. ✅ `./setup.sh` completes without errors
2. ✅ `python app.py` starts without errors
3. ✅ `curl http://localhost:5000/health` returns:
   ```json
   {"status": "healthy", "environment": "development"}
   ```
4. ✅ `python test_client.py` runs all tests successfully
5. ✅ You can see data in the database

---

## 🎯 Next Steps After Running

### 1. Explore the API
Try different endpoints:
- Enhance a JD: `/api/interview/jd/enhance`
- Generate interview: `/api/interview/generate`
- Complete workflow: `/api/interview/workflow/full`

### 2. Understand WORK Methodology
Read `WORK_METHODOLOGY_GUIDE.md` to learn how to create better job descriptions.

### 3. Test Both Workflows
Read `TWO_WORKFLOWS.md` to understand:
- Workflow 1: JD Enhancement only
- Workflow 2: Complete (JD + Interview)

### 4. Integrate Into Your App
Follow `INTEGRATION_GUIDE_FOR_PETER.md` for step-by-step integration.

---

## 💡 Tips for Success

1. **Start with the demo** - No commitment, see what it does
2. **Use SQLite first** - Simpler setup, switch to MySQL later
3. **Read the prompts** - See `prompts.py` to understand AI behavior
4. **Test incrementally** - Health check → Simple JD → Full workflow
5. **Monitor API costs** - Check https://console.anthropic.com/

---

## 📞 Resources

| Resource | Location |
|----------|----------|
| Claude API Console | https://console.anthropic.com/ |
| Anthropic Docs | https://docs.anthropic.com/ |
| Flask Documentation | https://flask.palletsprojects.com/ |
| SQLAlchemy Docs | https://docs.sqlalchemy.org/ |

---

## 🎉 You're All Set!

**Choose your path:**

- 🏃 **Quick demo?** → `python demo.py`
- 🚀 **Fast setup?** → `./setup.sh`
- 🛠️ **Full control?** → Read `HOW_TO_RUN.md`

Then explore, test, and integrate!

**Questions?** Check the docs in the project folder. Everything is documented!

---

Happy interviewing! 🎯
