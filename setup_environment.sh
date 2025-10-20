#!/bin/bash

# Network Security Education Toolkit - Environment Setup
# This script sets up the environment for the toolkit

echo "=========================================="
echo "Network Security Education Toolkit Setup"
echo "=========================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or later."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

echo "✅ pip3 found"

# Create virtual environment (optional but recommended)
echo "Creating virtual environment..."
python3 -m venv network_security_env

echo "To activate the virtual environment, run:"
echo "source network_security_env/bin/activate"

# Check for required system tools
echo ""
echo "Checking system tools..."

tools=("ping" "netstat" "ip")
missing_tools=()

for tool in "${tools[@]}"; do
    if command -v "$tool" &> /dev/null; then
        echo "✅ $tool found"
    else
        echo "❌ $tool not found"
        missing_tools+=("$tool")
    fi
done

if [ ${#missing_tools[@]} -gt 0 ]; then
    echo ""
    echo "⚠️  Some system tools are missing. Install them with:"
    echo "Ubuntu/Debian: sudo apt-get install net-tools iproute2 iputils-ping"
    echo "CentOS/RHEL: sudo yum install net-tools iproute iputils"
    echo "Arch Linux: sudo pacman -S net-tools iproute2 iputils"
fi

# Set executable permissions
echo ""
echo "Setting executable permissions..."
chmod +x network_security_toolkit.py

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To run the toolkit:"
echo "python3 network_security_toolkit.py"
echo ""
echo "For enhanced functionality, consider running with sudo:"
echo "sudo python3 network_security_toolkit.py"
echo ""
echo "⚠️  IMPORTANT: Only use this toolkit on networks you own"
echo "   or have explicit permission to test!"
echo ""