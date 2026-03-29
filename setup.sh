#!/bin/bash

# Real Estate Wholesale System - Setup Script
# Run this script to set up the entire system

set -e

echo "=================================="
echo "Real Estate Wholesale System Setup"
echo "=================================="
echo ""

# Check prerequisites
echo "✓ Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required. Please install Python 3.9+."
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "❌ Git is required. Please install Git."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo "✓ Git found: $(git --version)"
echo ""

# Create virtual environment
echo "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create .env file
echo "Creating .env configuration..."
if [ ! -f ".env" ]; then
    cat > .env << EOF
# Real Estate Wholesale System Configuration

# Database
DATABASE_URL=sqlite:///real_estate.db
# For PostgreSQL: postgresql://user:password@localhost/real_estate_db

# Server
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=development

# Vapi Voice AI
VAPI_API_KEY=your_vapi_key_here
VAPI_PHONE_NUMBERS=+1571491642,+1424857934

# Email/SMS
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Twilio SMS
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# AWS S3 (for document storage)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_S3_BUCKET=your_bucket_name
AWS_REGION=us-east-1

# Logging
LOG_LEVEL=INFO

# Security
SECRET_KEY=your_secret_key_here_change_in_production
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

EOF
    echo "✓ .env file created"
    echo "⚠️  Edit .env file with your API keys and credentials"
else
    echo "✓ .env file already exists"
fi
echo ""

# Initialize databases
echo "Initializing databases..."
if [ ! -f "real_estate.db" ]; then
    echo "Creating real_estate.db..."
    python3 -c "
import sqlite3
conn = sqlite3.connect('real_estate.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS deals (
    id INTEGER PRIMARY KEY,
    address TEXT,
    city TEXT,
    state TEXT,
    county TEXT,
    zip_code TEXT,
    property_type TEXT,
    list_price REAL,
    estimated_arv REAL,
    repair_cost REAL,
    holding_cost REAL,
    closing_cost REAL,
    profit_potential REAL,
    deal_score REAL,
    status TEXT
)''')
conn.commit()
conn.close()
"
    echo "✓ real_estate.db initialized"
fi

if [ ! -f "call_outcomes.db" ]; then
    echo "Creating call_outcomes.db..."
    python3 -c "
import sqlite3
conn = sqlite3.connect('call_outcomes.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS calls (
    id INTEGER PRIMARY KEY,
    phone_number TEXT,
    call_date TIMESTAMP,
    duration INTEGER,
    outcome TEXT,
    notes TEXT
)''')
conn.commit()
conn.close()
"
    echo "✓ call_outcomes.db initialized"
fi

if [ ! -f "deal_tracker.db" ]; then
    echo "Creating deal_tracker.db..."
    python3 -c "
import sqlite3
conn = sqlite3.connect('deal_tracker.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS offers (
    id INTEGER PRIMARY KEY,
    deal_id INTEGER,
    offer_price REAL,
    offer_tier TEXT,
    status TEXT,
    created_at TIMESTAMP,
    approved_at TIMESTAMP
)''')
conn.commit()
conn.close()
"
    echo "✓ deal_tracker.db initialized"
fi
echo ""

# Setup complete
echo "=================================="
echo "✓ Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Edit .env file with your API keys:"
echo "   nano .env"
echo ""
echo "2. Start the backend API:"
echo "   python3 dashboard_backend.py"
echo ""
echo "3. Open dashboard in your browser:"
echo "   http://localhost:8000/dashboard"
echo ""
echo "4. For Docker deployment:"
echo "   docker-compose up"
echo ""
echo "5. To deploy to Railway:"
echo "   Follow GITHUB_RAILWAY_DEPLOYMENT.md"
echo ""
echo "Documentation:"
echo "  - START_HERE.md"
echo "  - GITHUB_RAILWAY_DEPLOYMENT.md"
echo "  - OFFER_AND_CONTRACT_SYSTEM.md"
echo ""
