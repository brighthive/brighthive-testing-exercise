#!/bin/bash

# Start the BrightHive QA Exercise Web Application

echo "🚀 Starting BrightHive QA Exercise Web Application..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies if needed
if [ ! -f ".venv/.installed" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    touch .venv/.installed
fi

# Start the application
echo ""
echo "✅ Starting web application on http://localhost:8000"
echo "📚 Swagger UI: http://localhost:8000/docs ← AUTOMATE THIS!"
echo "🏥 Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn webapp:app --reload --port 8000
