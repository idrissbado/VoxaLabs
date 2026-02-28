#!/bin/bash

# VoxaLab AI - Quick Start Setup Script
# Sets up VoxaLab AI for local development

echo ""
echo "VoxaLab AI - Setup"
echo ""

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.10 or later from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "OK - Python $PYTHON_VERSION installed"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js not found. Please install Node.js 16 or later from https://nodejs.org"
    exit 1
fi

NODE_VERSION=$(node -v)
echo "OK - Node.js $NODE_VERSION installed"

# Check Git (optional)
if ! command -v git &> /dev/null; then
    echo "NOTE: Git not found (optional). Some features may not work without Git."
else
    echo "OK - Git is installed"
fi

echo ""
echo "Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env configuration file..."
    cp .env.example .env 2>/dev/null || echo "MISTRAL_API_KEY=your-api-key-here" > .env
    echo "NOTE: Please edit backend/.env and add your Mistral API key"
fi

echo "OK - Backend setup complete"
cd ..

# Setup Frontend
echo ""
echo "Setting up Frontend..."
cd frontend

# Install dependencies
echo "Installing npm dependencies..."
npm install -q --legacy-peer-deps 2>/dev/null || npm install -q

echo "OK - Frontend setup complete"
cd ..

echo ""
echo "Setup Complete"
echo ""
echo "Next Steps:"
echo ""
echo "1. Edit backend/.env with your Mistral API key:"
echo "   MISTRAL_API_KEY=sk-your-key-here"
echo ""
echo "2. Start the backend in Terminal 1:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "3. Start the frontend in Terminal 2:"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "Documentation:"
echo "   README.md - Project overview"
echo "   DEPLOY.md - Deployment guide"
echo ""
echo "Get your Mistral API key from:"
echo "   https://console.mistral.ai"
echo ""
