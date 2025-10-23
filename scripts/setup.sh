#!/bin/bash
# Setup script for Amazon Order Automation with Stagehand AI
# Author: qm-somesh
# Date: 2025-10-23

echo "=================================================="
echo "Amazon Order Automation - Setup Script"
echo "Powered by Stagehand AI"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Check if Node.js is installed (required for Stagehand)
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed. Please install Node.js 16+ for Stagehand AI."
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✓ Found Node.js $NODE_VERSION"

# Create virtual environment
echo ""
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "✓ Python dependencies installed"

# Install Stagehand via npm
echo ""
echo "Installing Stagehand AI..."
npm install @browserbasehq/stagehand

echo "✓ Stagehand AI installed"

# Install wkhtmltopdf for PDF generation
echo ""
echo "Checking for wkhtmltopdf (required for PDF generation)..."
if ! command -v wkhtmltopdf &> /dev/null; then
    echo "WARNING: wkhtmltopdf not found. Please install it manually:"
    echo "  - Ubuntu/Debian: sudo apt-get install wkhtmltopdf"
    echo "  - macOS: brew install wkhtmltopdf"
    echo "  - Windows: Download from https://wkhtmltopdf.org/downloads.html"
else
    echo "✓ wkhtmltopdf is installed"
fi

# Create output directories
echo ""
echo "Creating output directories..."
mkdir -p output
mkdir -p screenshots

echo "✓ Output directories created"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "IMPORTANT: Please edit .env file and add your Amazon credentials:"
    echo "  - AMAZON_EMAIL"
    echo "  - AMAZON_PASSWORD"
else
    echo ""
    echo "✓ .env file already exists"
fi

# Summary
echo ""
echo "=================================================="
echo "Setup Complete! 🎉"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Amazon credentials"
echo "2. Run the automation:"
echo "   python src/amazon_automation.py"
echo ""
echo "For more information, see README.md"
echo ""
