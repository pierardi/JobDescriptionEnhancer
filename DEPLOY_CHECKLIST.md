# AWS Amplify Deployment Checklist

## Pre-Deployment

### Backend Setup (Do this first!)
- [ ] Deploy Flask backend to Elastic Beanstalk/ECS/EC2
- [ ] Get backend URL (e.g., `https://jdenhancer-env.elasticbeanstalk.com`)
- [ ] Test backend health: `curl https://your-backend-url/health`
- [ ] Verify CORS is enabled (already configured in `app.py`)

### Repository Setup
- [ ] Code is pushed to GitHub: `pierardi/JobDescriptionEnhancer`
- [ ] `amplify.yml` is in root directory ✅
- [ ] `frontend/public/_redirects` exists ✅
- [ ] All changes committed and pushed

## Amplify Deployment Steps

### Step 1: Connect Repository
- [ ] Go to AWS Amplify Console
- [ ] Click "New app" → "Host web app"
- [ ] Connect GitHub repository: `pierardi/JobDescriptionEnhancer`
- [ ] Select branch: `main`

### Step 2: Configure Build
- [ ] Verify `amplify.yml` is auto-detected
- [ ] Click "Next"

### Step 3: Set Environment Variables
- [ ] Add `REACT_APP_API_URL` = `https://your-backend-url`
- [ ] Click "Save and deploy"

### Step 4: Configure Redirects (After first deploy)
- [ ] Go to App settings → Rewrites and redirects
- [ ] Add rule: `/<*>` → `/index.html` (200 Rewrite)
- [ ] Save

### Step 5: Verify Deployment
- [ ] Build completes successfully
- [ ] Frontend accessible at Amplify URL
- [ ] Test health check from frontend
- [ ] Test creating an interview

## Post-Deployment

- [ ] Test all features work
- [ ] Check browser console for errors
- [ ] Verify API calls are successful
- [ ] Set up custom domain (optional)
- [ ] Configure monitoring

## Quick Commands

### Get Backend URL (if using Elastic Beanstalk)
```bash
eb status
```

### Test Backend
```bash
curl https://your-backend-url/health
```

### View Amplify Build Logs
- Go to Amplify Console → Build history

### View Backend Logs (Elastic Beanstalk)
```bash
eb logs
```
