#!/bin/bash

echo "Setting up Invo Penetration Testing Tool..."

# Get absolute path to the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Install system dependencies
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-venv nmap

# Clean up old files
echo "Cleaning up old files..."
sudo rm -rf venv
sudo find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Create virtual environment with user permissions
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip in virtual environment
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python packages in virtual environment
echo "Installing Python packages..."
pip install langchain-core
pip install langchain-community
pip install langchain-ollama
pip install pyyaml
pip install requests

# Create necessary directories
echo "Creating directories..."
mkdir -p {reports,logs}
chmod 755 {reports,logs}

# Setup sudo rule for nmap
echo "Setting up sudo rules..."
sudo rm -f /etc/sudoers.d/invo
echo "# Allow running nmap without password for invo tool" | sudo tee /etc/sudoers.d/invo
echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/nmap *" | sudo tee -a /etc/sudoers.d/invo
sudo chmod 0440 /etc/sudoers.d/invo

# Make the main script executable
chmod +x invo.sh

# Installation complete
echo "Setup complete!"
echo "Run the tool with: ./invo <domain> [options]"
echo "For help use: ./invo --help"

# Deactivate virtual environment
deactivate