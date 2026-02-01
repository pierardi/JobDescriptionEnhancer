# AWS Amplify Deployment Guide

## Quick Deploy Steps

### 1. Connect Repository to Amplify

1. Go to [AWS Amplify Console](https://console.aws.amazon.com/amplify)
2. Click **"New app"** → **"Host web app"**
3. Select **"GitHub"** and authorize
4. Select repository: **`pierardi/JobDescriptionEnhancer`**
5. Select branch: **`main`**
6. Click **"Next"**

### 2. Configure Build Settings

Amplify will auto-detect the `amplify.yml` file. Verify:
- **Build specification**: `amplify.yml` (should be auto-detected)
- **App root**: Leave empty (root of repo)
- Click **"Next"**

### 3. Set Environment Variables

**IMPORTANT**: You must set this environment variable:

- **Key**: `REACT_APP_API_URL`
- **Value**: Your Flask backend URL (e.g., `https://your-backend.elasticbeanstalk.com`)

**To get your backend URL:**
- If using Elastic Beanstalk: Run `eb status` and copy the CNAME
- If using ECS/EC2: Use your load balancer or instance URL

**Additional environment variables (optional):**
- `NODE_ENV`: `production` (usually set automatically)

### 4. Configure Redirects (Critical for React Router)

After the first deployment:

1. Go to **App settings** → **Rewrites and redirects**
2. Add a new rule:
   - **Source address**: `/<*>`
   - **Target address**: `/index.html`
   - **Type**: `200 (Rewrite)`
3. Click **"Save"**

**Note**: The `_redirects` file in `frontend/public/` should handle this automatically, but it's good to verify.

### 5. Deploy

1. Click **"Save and deploy"**
2. Wait for build to complete (~3-5 minutes)
3. Your app will be available at: `https://main.xxxxx.amplifyapp.com`

## Environment Variables Reference

### Required for Frontend:
```
REACT_APP_API_URL=https://your-backend-url.com
```

### Backend Environment Variables (Set in Elastic Beanstalk/ECS):
```
DATABASE_URL=mysql+pymysql://dbadmin:PASSWORD@staging.cvnqlfgghza5.us-west-2.rds.amazonaws.com:3306/jdenhancer?charset=utf8mb4
CLAUDE_API_KEY=your-anthropic-api-key
FLASK_ENV=production
CLAUDE_MODEL=claude-opus-4-1
CORS_ORIGINS=*
```

## File Structure for Amplify

```
JDEnhancer/
├── amplify.yml              # Amplify build configuration
├── frontend/
│   ├── public/
│   │   ├── _redirects      # React Router redirects
│   │   └── index.html
│   ├── src/
│   │   └── api.js          # Uses REACT_APP_API_URL
│   └── package.json
└── ... (backend files not needed for Amplify)
```

## Build Process

Amplify will:
1. Checkout your code from GitHub
2. Run `cd frontend && npm ci` (install dependencies)
3. Run `npm run build` (build React app)
4. Deploy `frontend/build/` to CloudFront CDN

## Troubleshooting

### Build Fails

**Error: "Cannot find module"**
- Check that `frontend/package.json` exists
- Verify `amplify.yml` has correct paths

**Error: "npm ci failed"**
- Check Node.js version (Amplify uses Node 18 by default)
- Verify `package-lock.json` is committed

### Frontend Can't Connect to Backend

**CORS Errors:**
- Verify backend has CORS enabled (already configured in `app.py`)
- Check `CORS_ORIGINS` environment variable in backend

**404 Errors:**
- Verify `REACT_APP_API_URL` is set correctly in Amplify
- Check backend URL is accessible: `curl https://your-backend-url/health`

### React Router Not Working

- Verify `_redirects` file exists in `frontend/public/`
- Check Amplify redirects configuration (App settings → Rewrites and redirects)
- Ensure rule: `/<*>` → `/index.html` (200 Rewrite)

## Custom Domain (Optional)

1. Go to **App settings** → **Domain management**
2. Click **"Add domain"**
3. Enter your domain name
4. Follow DNS configuration instructions
5. SSL certificate is automatically provisioned

## Continuous Deployment

Amplify automatically deploys when you push to the connected branch:
- Push to `main` → Deploys to production
- Create a branch → Creates a preview deployment

## Monitoring

- **Build logs**: Available in Amplify Console
- **Access logs**: App settings → Access logs
- **Error tracking**: Consider integrating with CloudWatch or Sentry

## Next Steps After Deployment

1. ✅ Test the deployed frontend
2. ✅ Verify API calls work
3. ✅ Test creating an interview
4. ✅ Set up custom domain (optional)
5. ✅ Configure monitoring/alerts
6. ✅ Set up CI/CD for automatic deployments

## Quick Checklist

- [ ] Repository connected to Amplify
- [ ] `REACT_APP_API_URL` environment variable set
- [ ] Backend deployed and accessible
- [ ] Redirects configured for React Router
- [ ] Build completes successfully
- [ ] Frontend accessible at Amplify URL
- [ ] API calls working (test health endpoint)
- [ ] End-to-end test (create interview)
