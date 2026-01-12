# Quick Start Guide

## Running the Full Application

### 1. Start the Flask Backend

In the project root directory:

```bash
# Activate virtual environment (Windows)
.\venv\Scripts\Activate.ps1

# Or on Mac/Linux
source venv/bin/activate

# Run Flask app
python app.py
```

The backend should be running on http://localhost:5000

### 2. Start the React Frontend

In a new terminal, navigate to the frontend directory:

```bash
cd frontend
npm start
```

The React app will automatically open in your browser at http://localhost:3000

## Using the Application

1. **Fill in Job Description Details:**
   - Requisition ID (required): e.g., "REQ-12345"
   - Job Title (required): e.g., "Senior Software Engineer"
   - Department (optional): e.g., "Engineering"
   - Job Level (optional): Select from dropdown
   - Job Description (required): Enter the full job description

2. **Add WORK Methodology Inputs (Optional but Recommended):**
   - Work Output: What deliverables/features will this person build?
   - Work Role: Key responsibilities and day-to-day activities
   - Work Knowledge: Critical technologies, frameworks, concepts
   - Work Competencies: Essential skills and attributes

3. **Interview Name (Optional):**
   - If left empty, will auto-generate based on job title

4. **Click "Create Interview"**
   - The system will:
     - Enhance the job description using WORK methodology
     - Generate 5 technical interview questions
     - Create 8-10 evaluation criteria per question

5. **View Results:**
   - See all generated questions
   - Review evaluation criteria for each question
   - Note the tokens used for API calls

## Troubleshooting

### Backend not responding
- Check that Flask is running on port 5000
- Verify database connection (SQLite should auto-create)
- Check console for error messages

### Frontend can't connect to backend
- Ensure backend is running before starting frontend
- Check that proxy in package.json points to correct backend URL
- Verify CORS settings if accessing from different origin

### API Errors
- Ensure CLAUDE_API_KEY is set if using Claude API features
- Check network tab in browser DevTools for detailed error messages
- Verify request headers are correct (X-User-ID, X-User-Role)

## Development Notes

- The frontend uses a proxy (configured in package.json) to forward API requests
- Default authentication headers are set in `src/api.js`
- Server health status is checked on app load