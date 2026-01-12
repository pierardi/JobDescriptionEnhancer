# TechScreen Interview Generator - React Frontend

A modern React frontend for creating technical interviews from job descriptions using the TechScreen Interview Generation API.

## Features

- 📝 Complete form for job description and WORK methodology inputs
- 🎯 Real-time validation and error handling
- 📊 Beautiful display of generated interviews with evaluation criteria
- ✅ Server health monitoring
- 🎨 Modern, responsive UI design

## Prerequisites

- Node.js 14+ and npm
- Backend Flask API running on http://localhost:5000

## Installation

1. Install dependencies:
```bash
cd frontend
npm install
```

## Running the Application

1. Make sure the Flask backend is running (see main README.md)

2. Start the React development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Configuration

The frontend is configured to proxy API requests to `http://localhost:5000` by default (see `package.json`).

To use a different backend URL, create a `.env` file in the `frontend` directory:

```
REACT_APP_API_URL=http://your-backend-url:5000
```

## Project Structure

```
frontend/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── App.jsx             # Main application component
│   ├── App.css             # Main app styles
│   ├── InterviewForm.jsx   # Form component for creating interviews
│   ├── InterviewForm.css   # Form styles
│   ├── InterviewDisplay.jsx # Component to display generated interviews
│   ├── InterviewDisplay.css # Display styles
│   ├── api.js              # API service functions
│   ├── index.js            # React entry point
│   └── index.css           # Global styles
├── package.json            # Dependencies and scripts
└── README.md               # This file
```

## Usage

1. Fill in the required fields:
   - Requisition ID
   - Job Title
   - Job Description

2. Optionally fill in WORK methodology fields for better results:
   - Work Output: What will this person deliver/build?
   - Work Role: What are the key responsibilities?
   - Work Knowledge: What knowledge areas are critical?
   - Work Competencies: What competencies are essential?

3. Click "Create Interview" to generate a 5-question technical interview

4. View the generated interview with all questions and evaluation criteria

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build` folder.

## API Endpoints Used

- `POST /api/interview/workflow/full` - Create complete interview (JD enhancement + interview generation)
- `GET /health` - Health check

## Authentication

The frontend currently uses default headers:
- `X-User-ID: admin-user-id`
- `X-User-Role: admin`

To customize authentication, modify the `getDefaultHeaders()` function in `src/api.js`.