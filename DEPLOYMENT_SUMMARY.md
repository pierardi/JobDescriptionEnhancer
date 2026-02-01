# Deployment Summary - AWS Amplify Setup

## What Was Changed

### Files Created:
1. **`amplify.yml`** - Amplify build configuration for React frontend
2. **`Dockerfile`** - Docker configuration for Flask backend (optional, for ECS)
3. **`application.py`** - WSGI entry point for Elastic Beanstalk
4. **`.ebextensions/`** - Elastic Beanstalk configuration
5. **`.ebignore`** - Files to exclude from EB deployment
6. **`frontend/public/_redirects`** - Amplify redirects for React Router
7. **`AMPLIFY_QUICK_START.md`** - Quick deployment guide
8. **`amplify_setup_guide.md`** - Detailed setup guide

### Files Modified:
1. **`app.py`** - Added CORS support for Amplify frontend
2. **`requirements.txt`** - Added `flask-cors` and `gunicorn`
3. **`frontend/src/api.js`** - Updated to use environment variable for API URL

## Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────┐
│  AWS Amplify    │────────▶│ Elastic Beanstalk│────────▶│  RDS MySQL  │
│  (React Frontend)│  HTTPS  │  (Flask Backend) │         │  (Database) │
└─────────────────┘         └──────────────────┘         └─────────────┘
```

## Quick Deployment Steps

### 1. Backend (Elastic Beanstalk)
```bash
eb init -p python-3.11 jdenhancer-app --region us-west-2
eb create jdenhancer-env
eb setenv DATABASE_URL="..." CLAUDE_API_KEY="..." FLASK_ENV=production
eb deploy
```

### 2. Frontend (Amplify)
1. Go to AWS Amplify Console
2. Connect GitHub repo: `pierardi/JobDescriptionEnhancer`
3. Set environment variable: `REACT_APP_API_URL=https://your-backend-url`
4. Deploy

## Key Configuration

### Environment Variables Needed:

**Amplify (Frontend)**:
- `REACT_APP_API_URL` - Your Flask backend URL

**Elastic Beanstalk (Backend)**:
- `DATABASE_URL` - RDS MySQL connection string
- `CLAUDE_API_KEY` - Your Anthropic API key
- `FLASK_ENV=production`
- `CORS_ORIGINS=*` (or specific Amplify domain)

## Important Notes

1. **CORS**: Backend now allows all origins by default. For production, set `CORS_ORIGINS` to your specific Amplify domain.

2. **React Router**: The `_redirects` file ensures all routes work correctly in Amplify.

3. **API URL**: Frontend uses `REACT_APP_API_URL` environment variable. If not set in production, it will try to use relative URLs.

4. **Security**: Make sure RDS security group allows connections from Elastic Beanstalk security group.

## Testing

After deployment:
1. Test backend: `curl https://your-backend.elasticbeanstalk.com/health`
2. Test frontend: Visit Amplify URL and try creating an interview
3. Check browser console for any CORS or API errors

## Next Steps

1. Deploy backend to Elastic Beanstalk
2. Get backend URL
3. Deploy frontend to Amplify with backend URL
4. Test end-to-end
5. Configure custom domain (optional)
