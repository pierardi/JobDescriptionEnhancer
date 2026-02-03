# Hosting JDEnhancer on AWS

This guide covers hosting the **frontend** (React) and **backend** (Flask) on AWS, with a MySQL database.

## Architecture

```
┌─────────────────────┐      HTTPS       ┌──────────────────────┐      ┌─────────────┐
│   AWS Amplify       │ ───────────────▶│  Elastic Beanstalk   │─────▶│  RDS MySQL  │
│   (React frontend) │  REACT_APP_API   │  (Flask backend)     │      │  (Database) │
│   or S3 + CloudFront│      _URL        │  backend/ + app      │      └─────────────┘
└─────────────────────┘                  └──────────────────────┘
         │                                          │
         │                                          │ (optional)
         │                                          ▼
         │                                  ┌──────────────┐
         └─────────────────────────────────│ Anthropic    │
                   (browser only)           │ Claude API   │
                                            └──────────────┘
```

**Deploy order:** 1) Database (RDS) → 2) Backend (EB or ECS) → 3) Frontend (Amplify).

---

## 1. Database: RDS MySQL

Create a MySQL database for the backend.

1. In **AWS Console** → **RDS** → **Create database**.
2. Choose **MySQL 8.0** (or 5.7), **Free tier** or your preferred tier.
3. Set **DB identifier**, **master username**, **master password**. Save the password.
4. **Public access**: Yes if you want to connect from your PC for migrations; for production, usually No and access only from the VPC (EB/ECS in same VPC).
5. **VPC / Security group**: Note the security group (e.g. `rds-sg`). You will allow the backend (EB or ECS) to connect to this SG.
6. Create the DB. Wait for **Endpoint** (e.g. `xxx.region.rds.amazonaws.com`).

**Create a database and user:**

- Connect (e.g. MySQL Workbench, or EC2/bastion in same VPC) and run:

```sql
CREATE DATABASE jdenhancer CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- Optionally: CREATE USER 'appuser'@'%' IDENTIFIED BY 'your_password'; GRANT ALL ON jdenhancer.* TO 'appuser'@'%'; FLUSH PRIVILEGES;
```

**Connection string (for backend env):**

```text
mysql+pymysql://USER:PASSWORD@YOUR_RDS_ENDPOINT:3306/jdenhancer?charset=utf8mb4
```

Use this as `DATABASE_URL` in the backend (Elastic Beanstalk or ECS).

---

## 2. Backend: Elastic Beanstalk (recommended)

The backend lives in the `backend/` folder; the root `application.py` is the WSGI entry.

### 2.1 One-time setup (EB CLI)

```bash
# Install EB CLI if needed: pip install awsebcli
cd C:\Users\peter\OneDrive\dev\TechScreen\JDEnhancer

eb init -p python-3.11 jdenhancer-app --region us-east-1
# Choose your region. When asked for SSH, optional.
```

### 2.2 Create environment and deploy

```bash
eb create jdenhancer-env
# This uploads the app (backend/, application.py, .ebextensions; frontend/ is in .ebignore).
```

After creation, get the URL:

```bash
eb status
# Copy "CNAME" or the environment URL, e.g. jdenhancer-env.us-east-1.elasticbeanstalk.com
```

### 2.3 Set environment variables

In **AWS Console** → **Elastic Beanstalk** → your app → **Configuration** → **Software** → **Edit** → **Environment properties**, add:

| Name | Value |
|------|--------|
| `DATABASE_URL` | `mysql+pymysql://USER:PASSWORD@RDS_ENDPOINT:3306/jdenhancer?charset=utf8mb4` |
| `CLAUDE_API_KEY` | Your Anthropic API key |
| `FLASK_ENV` | `production` |
| `CORS_ORIGINS` | `*` (or your Amplify URL, e.g. `https://main.xxx.amplifyapp.com`) |

Or via CLI:

```bash
eb setenv DATABASE_URL="mysql+pymysql://..." CLAUDE_API_KEY="your-anthropic-api-key" FLASK_ENV=production CORS_ORIGINS="*"
```

### 2.4 Allow backend to reach RDS

- In **RDS** → your DB → **Security group** → **Inbound rules** → add rule: Type **MySQL/Aurora**, Port **3306**, Source = security group of the Elastic Beanstalk environment (or its EC2 instances).  
- If RDS has **Public access: No**, backend and RDS must be in the same VPC (default EB and RDS usually are).

### 2.5 Redeploy after changes

```bash
eb deploy
```

### 2.6 Test backend

```bash
curl https://YOUR_EB_CNAME/health
# Expect: {"status":"healthy", ...}
```

Use this **backend URL** (e.g. `https://jdenhancer-env.us-east-1.elasticbeanstalk.com`) as `REACT_APP_API_URL` in Amplify.

---

## 3. Backend alternative: ECS with Docker

If you prefer to run the backend as a container:

1. **Build and push image to ECR:**
   - AWS Console → **ECR** → Create repository (e.g. `jdenhancer-backend`).
   - Locally:
     ```bash
     aws ecr get-login-password --region REGION | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.REGION.amazonaws.com
     docker build -t jdenhancer-backend .
     docker tag jdenhancer-backend:latest ACCOUNT.dkr.ecr.REGION.amazonaws.com/jdenhancer-backend:latest
     docker push ACCOUNT.dkr.ecr.REGION.amazonaws.com/jdenhancer-backend:latest
     ```

2. **Create ECS cluster and service:**
   - Fargate, task definition with the image above.
   - Environment variables: `DATABASE_URL`, `CLAUDE_API_KEY`, `FLASK_ENV`, `CORS_ORIGINS`.
   - Expose port **5000** and put an **Application Load Balancer** in front.

3. Use the **ALB URL** (e.g. `https://xxx.us-east-1.elb.amazonaws.com`) as `REACT_APP_API_URL` for the frontend.

The project **Dockerfile** is already set up to run the backend (root `application.py` + `backend/`).

---

## 4. Frontend: AWS Amplify

The React app is in `frontend/`. Amplify uses `amplify.yml` and builds from the repo root.

### 4.1 Connect the repo

1. **AWS Console** → **Amplify** → **New app** → **Host web app**.
2. Connect **GitHub** (or your Git provider), select the **JDEnhancer** repo and branch (e.g. `main`).
3. Amplify should detect **amplify.yml**. App root = **empty** (repo root). Confirm and continue.

### 4.2 Set environment variable

In Amplify → **App settings** → **Environment variables**, add:

| Name | Value |
|------|--------|
| `REACT_APP_API_URL` | Your **backend URL** (e.g. `https://jdenhancer-env.us-east-1.elasticbeanstalk.com`) |

No trailing slash. This is used by `frontend/src/api.js` for all API calls.

### 4.3 Redirects (React Router)

The repo has `frontend/public/_redirects` with:

```text
/*    /index.html   200
```

If client-side routes still 404, in Amplify go to **App settings** → **Rewrites and redirects** and add:

- Source: `/<*>`  
- Target: `/index.html`  
- Type: **200 (Rewrite)**

### 4.4 Deploy

Save and deploy. The first build will:

- Run `cd frontend && npm ci` and `npm run build`.
- Serve `frontend/build` from Amplify’s CDN.

Your app URL will look like: `https://main.xxxxx.amplifyapp.com`.

---

## 5. Checklist and testing

- [ ] **RDS**: DB created, `jdenhancer` database exists, security group allows backend.
- [ ] **Backend (EB or ECS)**: Deployed, env vars set (`DATABASE_URL`, `CLAUDE_API_KEY`, `FLASK_ENV`, `CORS_ORIGINS`).
- [ ] **Backend health**: `curl https://YOUR_BACKEND_URL/health` returns JSON.
- [ ] **Amplify**: Repo connected, `REACT_APP_API_URL` = backend URL, redirects OK.
- [ ] **E2E**: Open Amplify URL → create an interview → confirm it hits the backend and DB.

---

## 6. Optional: custom domains and HTTPS

- **Amplify**: App settings → **Domain management** → add your domain; Amplify provisions HTTPS.
- **Elastic Beanstalk**: Add a custom domain and certificate (e.g. via Route 53 and ACM), or put CloudFront in front of the EB URL and use the CloudFront URL as `REACT_APP_API_URL`.

---

## 7. Summary

| Component | Service | Purpose |
|-----------|---------|--------|
| Frontend | **AWS Amplify** | Hosts React app, uses `REACT_APP_API_URL` to call backend |
| Backend | **Elastic Beanstalk** (or ECS) | Runs `application.py` and `backend/`, talks to RDS and Claude |
| Database | **RDS MySQL** | Stores job descriptions and interviews |
| API key | **Anthropic** | Backend only; never put in frontend |

Deploy in order: **RDS → Backend → Amplify**, and always set `REACT_APP_API_URL` in Amplify to your backend URL after the backend is live.
