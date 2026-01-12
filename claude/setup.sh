#!/bin/bash

# TechScreen Interview Generator - Automated Setup Script
# This script automates the setup process

set -e  # Exit on error

echo "=================================================="
echo "TechScreen Interview Generator - Setup"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print success message
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to print info message
info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Function to print error message
error() {
    echo -e "${RED}❌ $1${NC}"
}

echo "Step 1: Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    error "Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
success "Found Python $PYTHON_VERSION"
echo ""

echo "Step 2: Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    success "Virtual environment created"
else
    info "Virtual environment already exists"
fi
echo ""

echo "Step 3: Activating virtual environment..."
source venv/bin/activate
success "Virtual environment activated"
echo ""

echo "Step 4: Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
success "Dependencies installed"
echo ""

echo "Step 5: Setting up environment variables..."
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# Flask Configuration
FLASK_ENV=development
FLASK_APP=app.py

# Database - Using SQLite for quick testing
DATABASE_URL=sqlite:///techscreen.db

# Claude API - REPLACE THIS WITH YOUR KEY!
CLAUDE_API_KEY=your-api-key-here

# Model Configuration
CLAUDE_MODEL=claude-opus-4-1
CLAUDE_MAX_TOKENS=4000

# Feature Flags
ENABLE_QUESTION_CACHE=True
ASYNC_PROCESSING=False
SQLALCHEMY_ECHO=False
EOF
    success ".env file created"
    echo ""
    error "⚠️  IMPORTANT: You MUST edit .env and add your Claude API key!"
    echo "   Get your key from: https://console.anthropic.com/"
    echo "   Then run: nano .env (or use your favorite editor)"
    echo ""
else
    info ".env file already exists"
    echo ""
fi

echo "Step 6: Initializing database..."
python3 << 'PYEOF'
from app import create_app
from models import db

try:
    app = create_app('development')
    with app.app_context():
        db.create_all()
    print("✅ Database initialized successfully!")
except Exception as e:
    print(f"❌ Database initialization failed: {e}")
    exit(1)
PYEOF
echo ""

echo "=================================================="
echo "✅ Setup Complete!"
echo "=================================================="
echo ""
echo "Next Steps:"
echo ""
echo "1. Edit .env and add your Claude API key:"
echo "   nano .env"
echo ""
echo "2. Start the server:"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "3. In another terminal, test it:"
echo "   source venv/bin/activate"
echo "   python test_client.py"
echo ""
echo "4. Or visit: http://localhost:5000/health"
echo ""
echo "📖 Read QUICK_START.md for detailed instructions"
echo "=================================================="
