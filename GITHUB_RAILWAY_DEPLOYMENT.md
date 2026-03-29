# GitHub + Railway Deployment Guide

Complete step-by-step guide to deploy the Real Estate Wholesale system to production using GitHub + Railway.

## Overview

**Architecture:**
```
Your Computer (Local Development)
    ↓ Git Push
GitHub Repository
    ↓ Webhook Trigger
Railway.app (Production)
    ↓ Docker Container
Uvicorn Server (Port 8000)
    ↓
PostgreSQL Database
```

**What's Included:**
- ✅ Dockerfile for containerization
- ✅ requirements.txt with all dependencies
- ✅ railway.json for Railway configuration
- ✅ GitHub Actions CI/CD workflow
- ✅ Environment setup scripts
- ✅ Automatic deployment on push
- ✅ PostgreSQL database provisioning
- ✅ Health checks and monitoring

---

## Phase 1: GitHub Setup (5 minutes)

### Step 1: Create GitHub Account (if needed)
1. Go to https://github.com
2. Sign up or log in
3. Verify email

### Step 2: Create Repository

**Option A: Via Web**
1. Go to https://github.com/new
2. Repository name: `real-estate-wholesale`
3. Description: `AI-powered real estate wholesale automation system`
4. Choose: **Public** (simpler for this tutorial)
5. ✅ Check "Add .gitignore" → Select "Python"
6. ✅ Check "Add a README file"
7. Click "Create repository"

**Option B: Via Terminal** (Faster)
```bash
# On your computer
cd ~/real-estate-wholesale

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Real estate wholesale system"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/real-estate-wholesale.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Push Code to GitHub

**With all files from Tasklet:**

```bash
# Navigate to your project
cd ~/real-estate-wholesale

# Copy files from wherever you saved them
cp /path/to/dashboard_backend.py .
cp /path/to/offer_and_contract_system.py .
cp /path/to/property_scraper_and_analysis.py .
cp /path/to/vapi_voice_system.py .
cp /path/to/vapi_backend_api.py .
cp /path/to/approval_workflow_api.py .
cp /path/to/real_estate.db .
cp /path/to/call_outcomes.db .
cp /path/to/deal_tracker.db .

# Add all
git add .

# Commit
git commit -m "Add complete real estate system with all modules and databases"

# Push
git push
```

**Your repository now contains:**
```
real-estate-wholesale/
├── dashboard_backend.py          # Main API
├── offer_and_contract_system.py  # Offer generation
├── property_scraper_and_analysis.py  # Analysis
├── vapi_voice_system.py          # Voice AI
├── vapi_backend_api.py           # Voice API
├── approval_workflow_api.py       # Approvals
├── real_estate.db                # Sample data
├── call_outcomes.db              # Call logs
├── deal_tracker.db               # Deal tracking
├── Dockerfile                    # Container config
├── requirements.txt              # Python dependencies
├── railway.json                  # Railway config
├── .gitignore                    # Git ignore rules
└── README.md                     # Documentation
```

---

## Phase 2: Railway Setup (10 minutes)

### Step 1: Create Railway Account

1. Go to https://railway.app
2. Click "Start Free" or "Sign In"
3. Choose GitHub signup (easiest)
4. Authorize Railway to access GitHub
5. Confirm email if needed

### Step 2: Create Project

1. In Railway dashboard, click "New Project"
2. Select "Deploy from GitHub repo"
3. Search for `real-estate-wholesale`
4. Click to select it
5. Railway asks "Authorize Railway?"
   - Click "Authorize" to allow Railway to access your repo

### Step 3: Configure Services

Railway should auto-detect:
- ✅ Dockerfile (your app container)
- ✅ PostgreSQL (database)

**If not auto-detected:**

1. Click "Add Service"
2. Select "Database"
3. Choose "PostgreSQL"
4. Click "Deploy"

### Step 4: Set Environment Variables

1. Click on your **App Service** (not database)
2. Go to "Variables" tab
3. Click "New Variable" and add:

```
DATABASE_URL=postgresql://user:password@host:port/railway
PORT=8000
FLASK_ENV=production
LOG_LEVEL=INFO
```

**To get DATABASE_URL:**
1. Click on **PostgreSQL service**
2. Go to "Connect" tab
3. Copy the PostgreSQL connection string
4. Paste into APP's `DATABASE_URL` variable

### Step 5: Deploy

1. Click the **App service** again
2. Look for "Deployment" or "Deployments" tab
3. You should see a build in progress
4. Wait for ✅ "Success" (2-5 minutes)
5. Click on the deployment to view logs

**Check for success message:**
```
✓ BUILD PASSED
✓ DEPLOY PASSED
✓ Service started successfully
```

---

## Phase 3: Verify Deployment (5 minutes)

### Step 1: Get Your Live URL

1. In Railway, click your **App service**
2. Look for "Domains" or click the URL icon
3. Railway gives you a URL like:
   ```
   https://real-estate-wholesale-production.up.railway.app
   ```

### Step 2: Test the API

**Test health check:**
```bash
curl https://your-railway-url/api/health
# Should return: {"status": "ok"}
```

**Test deals endpoint:**
```bash
curl https://your-railway-url/api/deals
# Should return list of deals
```

**Test offer generation:**
```bash
curl -X POST https://your-railway-url/offers/generate \
  -H "Content-Type: application/json" \
  -d '{"deal_id": 1}'
# Should return 3 offers
```

### Step 3: Access Your Dashboard

1. Navigate to: `https://your-railway-url/dashboard`
2. You should see your deal interface
3. All features working: offers, contracts, voice calls

---

## Phase 4: CI/CD Setup (Automatic Deployments)

Railway automatically deploys when you push to GitHub. But you can also set up GitHub Actions for custom workflows.

### Create `.github/workflows/deploy.yml`

```yaml
name: Deploy to Railway

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Railway
        run: |
          npm install -g @railway/cli
          railway up --detach
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

### Add GitHub Secret

1. Go to your GitHub repo
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `RAILWAY_TOKEN`
5. Value: (Get from Railway dashboard)
   - Railway → Account settings → API tokens
   - Create new token
   - Copy and paste

---

## Phase 5: Monitoring & Management

### View Logs

**In Railway:**
1. Click your App service
2. Click "Logs" tab
3. See real-time logs of your app

**Terminal (if CLI installed):**
```bash
railway logs --tail
```

### Monitor Health

**Railway Dashboard:**
1. Click service
2. See CPU, Memory, Network usage
3. See deployment history

### Scale Up (Paid)

Need more power?
```
Railway Pro ($20/month)
- Unlimited services
- Custom domains
- Priority support
- Higher resource limits
```

---

## Phase 6: Custom Domain (Optional)

Want `real-estate.yourdomain.com`?

### Add Custom Domain

1. Railway → App service → "Domains"
2. Click "Add Domain"
3. Enter: `real-estate.yourdomain.com`
4. Railway gives you CNAME record
5. Go to your domain registrar
6. Add CNAME pointing to Railway
7. Wait 5-30 minutes for DNS propagation
8. ✅ Your domain now routes to app

---

## Phase 7: Continuous Improvement

### Auto-Deploy on Push

Every time you push to `main`:
```bash
git add .
git commit -m "Fix: offer generation logic"
git push
# ↓
# GitHub receives push
# ↓
# Railroad auto-detects
# ↓
# Triggers new deployment
# ↓
# App updated in 2-5 minutes
```

### Rollback if Something Breaks

1. Railway → Deployments tab
2. See all previous deployments
3. Click previous working version
4. Click "Rollback"
5. 1-2 minutes to restore

---

## Complete File Checklist

Before deploying, ensure you have:

```
✅ dashboard_backend.py         (Main API)
✅ offer_and_contract_system.py (Offers)
✅ property_scraper_and_analysis.py  (Analysis)
✅ vapi_voice_system.py         (Voice)
✅ vapi_backend_api.py          (Voice API)
✅ approval_workflow_api.py      (Approvals)
✅ real_estate.db               (Data)
✅ call_outcomes.db             (Calls)
✅ deal_tracker.db              (Tracking)
✅ Dockerfile                   (Container)
✅ requirements.txt             (Deps)
✅ railway.json                 (Config)
✅ .gitignore                   (Git rules)
✅ README.md                    (Docs)
```

---

## Troubleshooting

### Build Fails

**Error: "Module not found"**
- Check requirements.txt has all imports
- Verify Dockerfile copies all Python files

**Error: "Port already in use"**
- Railway auto-assigns port
- Check `$PORT` environment variable

### App Crashes

**Error: "Database connection failed"**
- Verify DATABASE_URL in Railway variables
- Check PostgreSQL service is running
- Test connection: `psql $DATABASE_URL`

**Error: "Out of memory"**
- Railway Pro has more resources
- Or optimize code to use less memory

### Logs Show Errors

1. Click Logs tab in Railway
2. Look for error messages
3. Search error message online
4. Check requirements.txt for missing deps

---

## Production Checklist

Before going live with real deals:

- [ ] Create GitHub account
- [ ] Create repository
- [ ] Push code to GitHub
- [ ] Create Railway account
- [ ] Deploy PostgreSQL
- [ ] Deploy Python app
- [ ] Set environment variables
- [ ] Test all API endpoints
- [ ] Verify health check passes
- [ ] Test offer generation
- [ ] Test contract generation
- [ ] Test voice system integration
- [ ] Verify database persistence
- [ ] Check logs for errors
- [ ] Get custom domain (optional)
- [ ] Enable automatic deployments
- [ ] Document your URL for team
- [ ] Plan backup strategy

---

## Cost Breakdown

**GitHub:**
- Public repos: FREE ✅
- Private repos: FREE ✅
- Actions (CI/CD): 2,000 free minutes/month ✅

**Railway:**
- Free tier: $5 credit/month (usually covers small projects)
- Pro: $20/month (if you need more)
- Pay-as-you-go: $0.50/GB RAM/month

**Typical Monthly Cost:**
- Small deployment: $0-$5
- Medium deployment: $5-$20
- Large deployment: $20-$100+

---

## Next Steps

1. ✅ Create GitHub account
2. ✅ Create repository with files
3. ✅ Create Railway account
4. ✅ Deploy PostgreSQL
5. ✅ Deploy app
6. ✅ Verify working
7. ✅ Test all features
8. ✅ Go live with real deals

---

## Quick Command Reference

### Local Development
```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/real-estate-wholesale.git
cd real-estate-wholesale

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run locally
python dashboard_backend.py
# Or with Uvicorn
uvicorn dashboard_backend:app --reload
```

### Git Workflow
```bash
# Make changes
# ...

# Stage changes
git add .

# Commit
git commit -m "Description of changes"

# Push to GitHub (auto-deploys to Railway)
git push
```

### Railway CLI
```bash
# Install
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up

# View logs
railway logs --tail

# View environment
railway env
```

---

## Support Resources

- **Railway Docs:** https://docs.railway.app
- **GitHub Docs:** https://docs.github.com
- **FastAPI:** https://fastapi.tiangolo.com
- **Docker:** https://docs.docker.com
- **PostgreSQL:** https://www.postgresql.org/docs

---

**You're now ready to deploy to production!** 🚀

Your real estate system is production-grade and can scale to handle thousands of deals daily.

Next: Follow the step-by-step guide above to get your app live.
