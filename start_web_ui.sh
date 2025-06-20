#!/bin/bash

# Advanced Image Detection & Analysis Tool
# Comprehensive Computer Vision and AI/ML Web Interface
# 
# This script starts the advanced computer vision web application
# featuring OCR text recognition, face detection, and image quality analysis

echo "🔍 Advanced Image Detection & Analysis Tool"
echo "=========================================="
echo "🚀 Starting Computer Vision Web Interface..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python $python_version detected. Python $required_version or higher is required."
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing Computer Vision and AI/ML dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads
mkdir -p results
mkdir -p logs

# Check if Tesseract is installed (for OCR)
if ! command -v tesseract &> /dev/null; then
    echo "⚠️  Warning: Tesseract OCR is not installed. OCR functionality may not work properly."
    echo "   Install Tesseract:"
    echo "   - macOS: brew install tesseract tesseract-lang"
    echo "   - Ubuntu: sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-urd"
    echo "   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki"
    echo ""
fi

# Display system information
echo "🔍 System Information:"
echo "   - Python: $(python --version)"
echo "   - OpenCV: $(python -c 'import cv2; print(cv2.__version__)')"
echo "   - NumPy: $(python -c 'import numpy; print(numpy.__version__)')"
echo "   - Flask: $(python -c 'import flask; print(flask.__version__)')"
echo ""

# Start the web application
echo "🌐 Starting Advanced Image Detection Web Interface..."
echo "   📍 URL: http://localhost:5001"
echo "   🔧 Press Ctrl+C to stop the server"
echo ""

# Set environment variables
export FLASK_ENV=development
export FLASK_DEBUG=1

# Start Flask application
python app.py

echo ""
echo "👋 Advanced Image Detection Tool stopped."
echo "   Thank you for using our Computer Vision solution!" 