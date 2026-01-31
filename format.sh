#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Install formatting tools
pip install black isort

echo "Running isort..."
isort .

echo "Running black..."
black .

echo "Format complete!"
