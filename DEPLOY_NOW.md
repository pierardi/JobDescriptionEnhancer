# Deploy to AWS Amplify - Step by Step

## ⚠️ IMPORTANT: Deploy Backend First!

The frontend needs your backend URL. Deploy the backend first, then use that URL in Amplify.

---

## Step 1: Deploy Flask Backend to Elastic Beanstalk

### 1.1 Install EB CLI
```bash
pip install awsebcli
```

### 1.2 Initialize Elastic Beanstalk
```bash
cd c:\Users\peter\OneDrive\dev\TechScreen\JDEnhancer
eb init -p python-3.11 jdenhancer-app --region us-west-2
```
- When prompted, select "us-west-2" region
- Don't set up SSH (press Enter)

### 1.3 Create Environment
```bash
eb create jdenhancer-env
```
This will take 5-10 minutes. Wait for it to complete.

### 1.4 Set Environment Variables
**Replace YOUR_PASSWORD with your actual RDS MySQL password:**

```bash
eb setenv DATABASE_URL="mysql+pymysql://dbadmin:YOUR_PASSWORD@staging.cvnqlfgghza5.us-west-2.rds.amazonaws.com:3306/jdenhancer?charset=utf8mb4" CLAUDE_API_KEY="your-anthropic-api-key" FLASK_ENV=production CLAUDE_MODEL=claude-opus-4-1 CORS_ORIGINS="*"
```

### 1.5 Deploy
```bash
eb deploy
```

### 1.6 Get Your Backend URL
```bash
eb status
```
**Copy the CNAME URL** - it will look like:
`jdenhancer-env.us-west-2.elasticbeanstalk.com`

**Test it:**
```bash
curl https://jdenhancer-env.us-west-2.elasticbeanstalk.com/health
```
Should return: `{"status":"healthy","environment":"production"}`

---

## Step 2: Deploy Frontend to AWS Amplify

### 2.1 Go to Amplify Console
1. Visit: https://console.aws.amazon.com/amplify
2. Click **"New app"** → **"Host web app"**

### 2.2 Connect GitHub Repository
1. Select **"GitHub"**
2. Authorize AWS to access GitHub (if first time)
3. Select repository: **`pierardi/JobDescriptionEnhancer`**
4. Select branch: **`main`**
5. Click **"Next"**

### 2.3 Configure Build Settings
1. Amplify should auto-detect `amplify.yml`
2. Verify it shows: **"amplify.yml"** as build specification
3. Click **"Next"**

### 2.4 Set Environment Variable (CRITICAL!)
1. Click **"Advanced settings"** or scroll down
2. Under **"Environment variables"**, click **"Add environment variable"**
3. Add:
   - **Key**: `REACT_APP_API_URL`
   - **Value**: `https://YOUR-BACKEND-URL.elasticbeanstalk.com`
     - Replace `YOUR-BACKEND-URL` with the URL from Step 1.6
     - Example: `https://jdenhancer-env.us-west-2.elasticbeanstalk.com`
4. Click **"Save"**

### 2.5 Deploy
1. Click **"Save and deploy"**
2. Wait for build to complete (~3-5 minutes)
3. Watch the build logs - it should show:
   - Installing dependencies
   - Building React app
   - Deploying to CloudFront

### 2.6 Get Your Frontend URL
After deployment completes, you'll see:
- **App URL**: `https://main.xxxxx.amplifyapp.com`
- Click the URL to open your app!

---

## Step 3: Configure Redirects (For React Router)

After the first deployment:

1. In Amplify Console, go to your app
2. Click **"App settings"** (left sidebar)
3. Click **"Rewrites and redirects"**
4. Click **"Add rewrite/redirect"**
5. Add:
   - **Source address**: `/<*>`
   - **Target address**: `/index.html`
   - **Type**: `200 (Rewrite)`
6. Click **"Save"**

**Note:** The `_redirects` file should handle this, but verify it's working.

---

## Step 4: Test Your Deployment

### Test Backend
```bash
curl https://your-backend-url.elasticbeanstalk.com/health
```

### Test Frontend
1. Open your Amplify app URL in browser
2. Open browser console (F12)
3. Try creating an interview
4. Check for any errors in console

---

## Troubleshooting

### ❌ Build Fails in Amplify
- Check build logs in Amplify Console
- Verify `amplify.yml` is in root directory
- Ensure `frontend/package.json` exists

### ❌ Frontend Can't Connect to Backend
- Verify `REACT_APP_API_URL` is set correctly in Amplify
- Check backend URL is accessible: `curl https://your-backend-url/health`
- Verify CORS is enabled (we set `CORS_ORIGINS="*"`)

### ❌ React Router Not Working
- Verify redirects are configured (Step 3)
- Check `frontend/public/_redirects` file exists

### ❌ Backend Errors
- Check logs: `eb logs`
- Verify environment variables: `eb printenv`
- Check RDS security group allows EB connections

---

## Quick Reference

**Backend Commands:**
```bash
eb status          # Get backend URL
eb logs            # View logs
eb printenv        # View environment variables
eb deploy          # Redeploy
```

**Amplify:**
- Console: https://console.aws.amazon.com/amplify
- Build logs: Available in Amplify Console → Build history

---

## Your URLs After Deployment

- **Frontend**: `https://main.xxxxx.amplifyapp.com` (from Amplify)
- **Backend**: `https://jdenhancer-env.us-west-2.elasticbeanstalk.com` (from EB)

---

## Next Steps

1. ✅ Test the deployed app
2. ✅ Set up custom domain (optional)
3. ✅ Configure monitoring
4. ✅ Set up automatic deployments (push to main = auto deploy)
