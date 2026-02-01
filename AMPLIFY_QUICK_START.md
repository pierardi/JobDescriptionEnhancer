# Quick Start: Deploy to AWS Amplify

## Prerequisites
- AWS Account
- GitHub repository connected (already done: https://github.com/pierardi/JobDescriptionEnhancer.git)
- RDS MySQL database set up (already done)

## Step 1: Deploy Flask Backend (5 minutes)

### Using AWS Elastic Beanstalk (Easiest)

1. **Install EB CLI**:
   ```bash
   pip install awsebcli
   ```

2. **Initialize**:
   ```bash
   cd c:\Users\peter\OneDrive\dev\TechScreen\JDEnhancer
   eb init -p python-3.11 jdenhancer-app --region us-west-2
   ```

3. **Create environment**:
   ```bash
   eb create jdenhancer-env
   ```

4. **Set environment variables** (replace PASSWORD with your actual password):
   ```bash
   eb setenv DATABASE_URL="mysql+pymysql://dbadmin:PASSWORD@staging.cvnqlfgghza5.us-west-2.rds.amazonaws.com:3306/jdenhancer?charset=utf8mb4" CLAUDE_API_KEY="your-anthropic-api-key" FLASK_ENV=production CLAUDE_MODEL=claude-opus-4-1 CORS_ORIGINS="*"
   ```

5. **Deploy**:
   ```bash
   eb deploy
   ```

6. **Get backend URL**:
   ```bash
   eb status
   ```
   Copy the CNAME URL (e.g., `jdenhancer-env.us-west-2.elasticbeanstalk.com`)

## Step 2: Deploy React Frontend to Amplify (5 minutes)

1. **Go to AWS Amplify Console**:
   - Visit: https://console.aws.amazon.com/amplify
   - Click "New app" → "Host web app"

2. **Connect Repository**:
   - Select "GitHub"
   - Authorize and select: `pierardi/JobDescriptionEnhancer`
   - Branch: `main`

3. **Configure Build**:
   - Amplify will auto-detect `amplify.yml`
   - Click "Next"

4. **Set Environment Variables**:
   - Click "Advanced settings"
   - Add environment variable:
     - Key: `REACT_APP_API_URL`
     - Value: `https://YOUR-BACKEND-URL.elasticbeanstalk.com`
     - Replace `YOUR-BACKEND-URL` with the URL from Step 1

5. **Deploy**:
   - Click "Save and deploy"
   - Wait for build to complete (~5 minutes)

6. **Configure Redirects** (Important for React Router):
   - Go to: App settings → Rewrites and redirects
   - Add rule:
     - Source: `/<*>`
     - Target: `/index.html`
     - Type: `200 (Rewrite)`
   - Save

## Step 3: Test

1. **Test Backend**:
   ```bash
   curl https://YOUR-BACKEND-URL.elasticbeanstalk.com/health
   ```
   Should return: `{"status":"healthy","environment":"production"}`

2. **Test Frontend**:
   - Visit your Amplify app URL
   - Try creating an interview
   - Check browser console (F12) for any errors

## Troubleshooting

### Frontend can't connect to backend
- Verify `REACT_APP_API_URL` is set correctly in Amplify
- Check backend URL is accessible (try in browser)
- Verify CORS is enabled (backend should allow `*` origins)

### Build fails
- Check Amplify build logs
- Verify `amplify.yml` is in root directory
- Ensure `frontend/package.json` exists

### Backend errors
- Check Elastic Beanstalk logs: `eb logs`
- Verify environment variables: `eb printenv`
- Check RDS security group allows EB security group

## Your URLs

After deployment, you'll have:
- **Frontend**: `https://main.xxxxx.amplifyapp.com` (from Amplify)
- **Backend**: `https://jdenhancer-env.us-west-2.elasticbeanstalk.com` (from EB)

## Next Steps

1. Set up custom domain (optional)
2. Configure SSL certificates
3. Set up monitoring and alerts
4. Configure CI/CD for automatic deployments
