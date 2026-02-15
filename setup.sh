#!/bin/bash

# AI Lead Generation System - Automated Setup Script
# This script helps you set up the project quickly

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🚀 AI Lead Generation System - Setup Script              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "📋 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.9 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"
echo ""

# Navigate to backend directory
cd backend || exit 1

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo -e "${GREEN}✅ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env file with your API keys!${NC}"
else
    echo -e "${YELLOW}⚠️  .env file already exists${NC}"
fi
echo ""

# Check for credentials.json
if [ ! -f "credentials.json" ]; then
    echo -e "${YELLOW}⚠️  credentials.json not found${NC}"
    echo "   Please download your Google service account JSON and rename it to credentials.json"
else
    echo -e "${GREEN}✅ credentials.json found${NC}"
fi
echo ""

# Summary
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  📋 Setup Summary                                          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}✅ Virtual environment created and activated${NC}"
echo -e "${GREEN}✅ Dependencies installed${NC}"
echo -e "${GREEN}✅ .env file created${NC}"
echo ""

# Next steps
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  📝 Next Steps                                             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "1. Edit the .env file with your API keys:"
echo "   - OPENAI_API_KEY (from https://platform.openai.com/api-keys)"
echo "   - SERPER_API_KEY (from https://serper.dev/)"
echo "   - GOOGLE_SHEET_ID (from your Google Sheet URL)"
echo ""
echo "2. Add your credentials.json file:"
echo "   - Download from Google Cloud Console"
echo "   - Place in backend/ directory"
echo ""
echo "3. Run the application:"
echo "   python main.py"
echo ""
echo "4. Open the frontend:"
echo "   Open frontend/index.html in your browser"
echo ""
echo -e "${GREEN}🎉 Setup complete! Follow the steps above to start using the system.${NC}"
