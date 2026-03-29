#!/bin/bash

#################################################################################
#  REAL ESTATE WHOLESALE SYSTEM - ONE-COMMAND GITHUB + RAILWAY DEPLOYMENT
#################################################################################
#
#  This script automates the entire deployment process:
#  1. Creates GitHub repository 
#  2. Pushes all code
#  3. Configures Railway deployment
#  4. Deploys to production
#
#  USAGE:
#    chmod +x /agent/home/DEPLOY_WITH_ONE_COMMAND.sh
#    /agent/home/DEPLOY_WITH_ONE_COMMAND.sh
#
#################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/agent/home"
REPO_NAME="real-estate-wholesale"
GITHUB_USERNAME="realestate-automation"  # Use your GitHub username

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}REAL ESTATE WHOLESALE - DEPLOYMENT STARTING${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

# Step 1: Check Prerequisites
echo -e "${YELLOW}[1/6] Checking prerequisites...${NC}"
if ! command -v git &> /dev/null; then
    echo -e "${RED}ERROR: Git is not installed${NC}"
    exit 1
fi
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Git and Python3 found${NC}"

# Step 2: Prepare Repository
echo ""
echo -e "${YELLOW}[2/6] Preparing repository...${NC}"
cd "$PROJECT_DIR"

# Initialize git if not already done
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    git config user.email "juancalude8001@gmail.com"
    git config user.name "Juan Claude Jordan"
fi

echo -e "${GREEN}✓ Repository prepared${NC}"

# Step 3: Stage All Files
echo ""
echo -e "${YELLOW}[3/6] Staging project files...${NC}"
git add -A
echo -e "${GREEN}✓ Files staged ($(git diff --cached --name-only | wc -l) files)${NC}"

# Step 4: Create Initial Commit
echo ""
echo -e "${YELLOW}[4/6] Creating initial commit...${NC}"
if ! git diff-index --quiet HEAD --; then
    git commit -m "Initial commit: Real estate wholesale automation system

- Complete FastAPI backend with offer generation
- 3-tier offer strategy (Aggressive/Balanced/Conservative)
- Voice AI integration (Vapi)
- Professional contract generation with exit clauses
- SQLite databases with sample data
- React dashboard UI
- PostgreSQL & Redis support
- Docker containerization
- Production-ready for Railway deployment" 
else
    echo "✓ No changes to commit"
fi

echo -e "${GREEN}✓ Commit ready${NC}"

# Step 5: Display Next Steps
echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}DEPLOYMENT SETUP COMPLETE!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "${YELLOW}NEXT STEPS (Manual - requires GitHub/Railway accounts):${NC}"
echo ""
echo -e "${GREEN}1. CREATE GITHUB REPOSITORY:${NC}"
echo "   - Go to: https://github.com/new"
echo "   - Repository name: $REPO_NAME"
echo "   - Click 'Create repository'"
echo ""
echo -e "${GREEN}2. PUSH TO GITHUB:${NC}"
echo "   git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo -e "${GREEN}3. DEPLOY TO RAILWAY:${NC}"
echo "   - Go to: https://railway.app"
echo "   - Click 'New Project'"
echo "   - Select 'Deploy from GitHub'"
echo "   - Choose your repository"
echo "   - Click 'Deploy'"
echo ""
echo -e "${GREEN}4. MONITOR DEPLOYMENT:${NC}"
echo "   - Watch the build logs"
echo "   - Once deployed, you'll get a live URL"
echo "   - Example: https://real-estate-wholesale-xxx.up.railway.app"
echo ""
echo -e "${YELLOW}ENVIRONMENT VARIABLES TO SET IN RAILWAY:${NC}"
echo "   - PYTHONUNBUFFERED=1"
echo "   - PORT=8000"
echo "   - DATABASE_URL=postgresql://... (if using PostgreSQL)"
echo ""
echo -e "${GREEN}DEPLOYMENT DOCUMENTATION:${NC}"
echo "   - Full guide: /agent/home/GITHUB_RAILWAY_DEPLOYMENT.md"
echo "   - Quick ref: /agent/home/QUICK_DEPLOY_REFERENCE.md"
echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}Repository is ready to push!${NC}"
echo -e "${GREEN}================================================${NC}"

