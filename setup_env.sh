#!/bin/bash

# Check if requirements.txt exists
if [ ! -f requirements.txt ]; then
    echo "Error: requirements.txt not found in the current directory."
    exit 1
fi

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Setup complete. To activate the virtual environment, use: source venv/bin/activate"
