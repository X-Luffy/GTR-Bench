#!/bin/bash

# Human-Level Evaluation System Startup Script

echo "🎯 Starting Human-Level Evaluation System..."

# Activate conda environment
echo "🔧 Activating conda environment..."
# Note: Please modify the following path according to your actual conda environment path
# conda activate your_conda_environment_name
echo "⚠️  Please manually activate your conda environment, e.g.: conda activate your_env_name"

# Check Python environment
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed, please install Python first"
    exit 1
fi

# Check dependencies
echo "🔍 Checking project dependencies..."
python -c "import streamlit, cv2, PIL, numpy, pandas, subprocess, threading, queue; print('✅ All dependencies are installed')" || {
    echo "❌ Missing dependencies, please install packages from requirements.txt"
    exit 1
}

# Check eval directory
if [ ! -d "eval" ]; then
    echo "❌ eval directory does not exist"
    exit 1
fi

# Check eval.py file
if [ ! -f "eval/eval.py" ]; then
    echo "❌ eval/eval.py file does not exist"
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p eval/results
mkdir -p eval/results/prompt

# Start application
echo "🚀 Starting Streamlit application..."
echo "🎯 Features include:"
echo "   - Human assessment evaluation"
echo "   - Automated model evaluation"
echo "   - Result visualization and analysis"
echo "   - Real-time progress monitoring"
echo ""
echo "📝 Application will run at http://localhost:8505"
echo "🔧 To stop the application, press Ctrl+C"
echo ""

streamlit run app.py --server.port 8506 --server.address 0.0.0.0
