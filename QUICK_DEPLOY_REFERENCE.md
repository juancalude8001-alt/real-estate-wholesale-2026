# Quick Deploy Reference Card

## 🚀 GitHub + Railway Deployment in 15 Minutes

### Step 1: GitHub Setup (5 min)

```bash
# Initialize git
cd ~/real-estate-wholesale
git init
git add .
git commit -m "Initial: Real estate wholesale system"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/real-estate-wholesale.git
git branch -M main
git push -u origin main
```

**Or use GitHub web:**
1. Go to https://github.com/new
2. Name: `real-estate-wholesale`
3. Create repository
4. Follow on-screen instructions

### Step 2: Railway Setup (5 min)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
railway init

# Deploy
railway up
```

**Or use Railway web:**
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Choose your repo
5. Deploy (auto-detects Dockerfile)

### Step 3: Test (5 min)

```bash
# Get your Railway URL
railway domains

# Test API
curl https://your-railway-url/api/health

# Check deals
curl https://your-railway-url/api/deals
```

---

## 📋 File Checklist

```
✅ dashboard_backend.py
✅ offer_and_contract_system.py
✅ property_scraper_and_analysis.py
✅ vapi_voice_system.py
✅ vapi_backend_api.py
✅ approval_workflow_api.py
✅ real_estate.db
✅ call_outcomes.db
✅ deal_tracker.db
✅ Dockerfile
✅ requirements.txt
✅ railway.json
✅ .gitignore
✅ README.md
✅ START_HERE.md
✅ GITHUB_RAILWAY_DEPLOYMENT.md
```

---

## 🔑 Key URLs

| Service | URL |
|---------|-----|
| GitHub | https://github.com |
| Railway | https://railway.app |
| Your App | `https://your-railway-url.app` |
| Dashboard | `https://your-railway-url.app/dashboard` |
| API Health | `https://your-railway-url.app/api/health` |

---

## 💻 Local Commands

```bash
# Setup
./setup.sh

# Run locally
python3 dashboard_backend.py

# With Docker
docker-compose up

# Git workflow
git add .
git commit -m "Description"
git push  # Auto-deploys to Railway

# Railway CLI
railway login
railway up
railway logs --tail
railway env
```

---

## 🆘 Common Issues

| Issue | Fix |
|-------|-----|
| Module not found | `pip install -r requirements.txt` |
| Port 8000 in use | `lsof -i :8000` then kill process |
| Database error | Check DATABASE_URL in .env |
| Docker build fails | Check all Python files copied |
| Railway deploy fails | Check Dockerfile syntax |
| Can't connect to Railway | Wait 2-5 min, refresh page |

---

## 📊 Architecture

```
Your Computer
     ↓ git push
GitHub Repository
     ↓ webhook
Railway.app
     ↓ docker pull
Container (Python + FastAPI)
     ↓
PostgreSQL Database
     ↓
Your App Live!
```

---

## ⏱️ Typical Timing

- GitHub setup: 5 min
- Railway setup: 5 min
- Pushing code: 2 min
- Building container: 3-5 min
- Database setup: 2 min
- **Total: ~15-20 minutes**

---

## 🎯 Next Steps After Deploy

1. ✅ Test API endpoints
2. ✅ View dashboard in browser
3. ✅ Generate sample offers
4. ✅ Practice approvals
5. ✅ Review contracts
6. ✅ Add your API keys
7. ✅ Make first voice call
8. ✅ Send real offers
9. ✅ Close first deal
10. ✅ Celebrate! 🎉

---

## 📞 Need Help?

- **Docs**: See `/agent/home/*.md` files
- **GitHub Issues**: Post in repo issues
- **Railway Support**: https://railway.app/support
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

**You're ready to deploy!** 🚀

```bash
git push  # Deploy to production now
```
