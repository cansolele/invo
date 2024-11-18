#!/bin/bash

# INVO - AI-Powered Penetration Testing Tool

if [ "$#" -lt 1 ]; then
    echo "INVO - AI-Powered Penetration Testing Tool"
    echo "Usage: ./invo <domain> [options]"
    echo ""
    echo "Options:"
    echo "  -r        Reconnaissance mode"
    echo "  -v        Verbose output"
    echo "  -Ru       Use Russian language"
    echo ""
    echo "Example: ./invo example.com -r -Ru"
    exit 1
fi

# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if virtual environment exists
if [ ! -d "$DIR/venv" ]; then
    echo "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source "$DIR/venv/bin/activate"

# Run the script
cd "$DIR"  # Change to script directory
python3 invo.py "$@"

# Check exit status
if [ $? -ne 0 ]; then
    echo "Scan failed. Please check the logs for details."
    deactivate
    exit 1
fi

# Deactivate virtual environment
deactivate