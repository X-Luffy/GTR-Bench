#!/bin/bash
# GTR-Bench installation script

set -e

echo "Installing GTR-Bench..."

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python version: $python_version"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "Error: Python 3.8 or higher is required"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Install package in development mode
echo "Installing GTR-Bench in development mode..."
pip install -e .

# Create necessary directories
echo "Creating directories..."
mkdir -p data/{raw,processed,annotations,splits,samples}
mkdir -p experiments/{runs,logs,checkpoints}
mkdir -p results/{outputs,analysis,reports,leaderboard}

echo "Installation complete!"
echo "To activate the environment, run: source venv/bin/activate"