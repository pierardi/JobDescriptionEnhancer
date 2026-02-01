# AWS Amplify Setup Guide for JDEnhancer

This guide will help you deploy the React frontend to AWS Amplify and set up the Flask backend separately.

## Architecture Overview

- **Frontend (React)**: Deployed on AWS Amplify
- **Backend (Flask)**: Deployed separately (AWS Elastic Beanstalk, ECS, or EC2)
- **Database**: RDS MySQL (already configured)

## Step 1: Deploy Flask Backend

You have several options for deploying the Flask backend:

### Option A: AWS Elastic Beanstalk (Recommended for simplicity)

1. **Install EB CLI** (if not already installed):
   ```bash
   pip install awsebcli
   ```

2. **Initialize Elastic Beanstalk**:
   ```bash
   cd /path/to/JDEnhancer
   eb init -p python-3.11 jdenhancer-app --region us-west-2
   ```

3. **Create environment**:
   ```bash
   eb create jdenhancer-env
   ```

4. **Set environment variables**:
   ```bash
   eb setenv DATABASE_URL="mysql+pymysql://dbadmin:PASSWORD@staging.cvnqlfgghza5.us-west-2.rds.amazonaws.com:3306/jdenhancer?charset=utf8mb4" \
            CLAUDE_API_KEY="your-anthropic-api-key" \
            FLASK_ENV=production \
            CLAUDE_MODEL=claude-opus-4-1
   ```

5. **Deploy**:
   ```bash
   eb deploy
   ```

6. **Get the backend URL**:
   ```bash
   eb status
   ```
   Note the CNAME URL (e.g., `jdenhancer-env.elasticbeanstalk.com`)

### Option B: AWS ECS with Docker

1. **Create Dockerfile** (see `Dockerfile` in repo)
2. **Build and push to ECR**
3. **Create ECS service**
4. **Set up Application Load Balancer**

### Option C: EC2 Instance

1. Launch EC2 instance
2. Install Python, dependencies
3. Set up systemd service
4. Configure security groups

## Step 2: Set Up AWS Amplify for Frontend

### 2.1 Connect Repository

1. Go to [AWS Amplify Console](https://console.aws.amazon.com/amplify)
2. Click "New app" → "Host web app"
3. Connect your GitHub repository: `https://github.com/pierardi/JobDescriptionEnhancer.git`
4. Select the branch (usually `main`)

### 2.2 Configure Build Settings

Amplify should auto-detect the `amplify.yml` file. If not, use these settings:

**Build settings:**
- Build image: `Amazon Linux 2`
- Build specification: `amplify.yml`

### 2.3 Set Environment Variables

In Amplify Console → App settings → Environment variables, add:

```
REACT_APP_API_URL=https://your-backend-url.elasticbeanstalk.com
```

Replace `your-backend-url.elasticbeanstalk.com` with your actual backend URL from Step 1.

**Important**: The frontend will use this URL to make API calls to your Flask backend.

### 2.4 Configure Redirects

In Amplify Console → App settings → Rewrites and redirects, add:

```
Source address: /<*>
Target address: /index.html
Type: 200 (Rewrite)
```

This ensures React Router works correctly.

### 2.5 Deploy

1. Click "Save and deploy"
2. Amplify will:
   - Install dependencies
   - Build the React app
   - Deploy to CloudFront CDN

## Step 3: Configure CORS for Flask Backend

The Flask backend needs to allow requests from your Amplify domain.

### Update Flask app to allow CORS:

1. **Install flask-cors**:
   ```bash
   pip install flask-cors
   ```

2. **Update app.py** to include CORS:
   ```python
   from flask_cors import CORS
   
   def create_app(config_name=None):
       app = Flask(__name__)
       # ... existing code ...
       
       # Enable CORS for Amplify domain
       CORS(app, resources={
           r"/api/*": {
               "origins": [
                   "https://*.amplifyapp.com",  # Amplify default domain
                   "https://your-custom-domain.com"  # Your custom domain if any
               ],
               "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
               "allow_headers": ["Content-Type", "X-User-ID", "X-User-Role"]
           }
       })
   ```

3. **Update requirements.txt**:
   ```
   flask-cors==4.0.0
   ```

## Step 4: Security Group Configuration

Ensure your RDS MySQL security group allows connections from:
- Your Elastic Beanstalk/ECS/EC2 security group
- Your local IP (for testing)

## Step 5: Custom Domain (Optional)

1. In Amplify Console → Domain management
2. Add your custom domain
3. Follow DNS configuration instructions

## Step 6: Testing

1. **Test Backend**:
   ```bash
   curl https://your-backend-url.elasticbeanstalk.com/health
   ```

2. **Test Frontend**:
   - Visit your Amplify app URL
   - Try creating an interview
   - Check browser console for errors

## Troubleshooting

### Frontend can't connect to backend
- Check `REACT_APP_API_URL` environment variable in Amplify
- Verify CORS is configured in Flask backend
- Check browser console for CORS errors

### Build fails in Amplify
- Check build logs in Amplify Console
- Verify `amplify.yml` is in root directory
- Ensure `frontend/package.json` exists

### Backend connection issues
- Verify RDS security group allows connections
- Check environment variables are set correctly
- Review Elastic Beanstalk logs: `eb logs`

## Environment Variables Summary

### Amplify (Frontend)
- `REACT_APP_API_URL`: Your Flask backend URL

### Elastic Beanstalk/ECS (Backend)
- `DATABASE_URL`: RDS MySQL connection string
- `CLAUDE_API_KEY`: Your Anthropic API key
- `FLASK_ENV`: `production`
- `CLAUDE_MODEL`: `claude-opus-4-1`
- `CLAUDE_MAX_TOKENS`: `4000`
- `ENABLE_QUESTION_CACHE`: `True`
- `CACHE_SIMILARITY_THRESHOLD`: `0.85`
- `ASYNC_PROCESSING`: `True`
- `REQUEST_TIMEOUT`: `300`
- `SQLALCHEMY_ECHO`: `False`

## Next Steps

1. Deploy Flask backend to Elastic Beanstalk
2. Get backend URL
3. Set up Amplify with backend URL
4. Test end-to-end
5. Configure custom domain (optional)
