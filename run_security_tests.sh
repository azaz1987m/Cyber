#!/bin/bash

# Network Security Toolkit - Test Runner
# Educational Purpose Only

echo "=========================================="
echo "Network Security Toolkit - Test Runner"
echo "=========================================="
echo "WARNING: Only use on networks you own or have permission to test!"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Make scripts executable
chmod +x network_security_toolkit.py
chmod +x advanced_network_tools.py
chmod +x defensive_security.py

echo ""
echo "Available test options:"
echo "1. Basic port scan (localhost)"
echo "2. Advanced network monitoring"
echo "3. Defensive security monitoring"
echo "4. Wireless security scan"
echo "5. Cryptography testing"
echo "6. Social engineering testing"
echo "7. Generate security report"
echo ""

read -p "Select test option (1-7): " choice

case $choice in
    1)
        echo "Running basic port scan on localhost..."
        python3 network_security_toolkit.py 127.0.0.1 -p 1-1000 -v
        ;;
    2)
        echo "Starting advanced network monitoring..."
        echo "Press Ctrl+C to stop"
        python3 advanced_network_tools.py --arp-monitor --dns-monitor
        ;;
    3)
        echo "Starting defensive security monitoring..."
        echo "Press Ctrl+C to stop"
        python3 defensive_security.py --monitor
        ;;
    4)
        echo "Scanning wireless networks..."
        python3 advanced_network_tools.py --wifi-scan
        ;;
    5)
        echo "Testing cryptography..."
        python3 advanced_network_tools.py --crypto-test
        ;;
    6)
        echo "Testing social engineering awareness..."
        python3 advanced_network_tools.py --social-test
        ;;
    7)
        echo "Generating security report..."
        python3 defensive_security.py --report
        ;;
    *)
        echo "Invalid option. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "Test completed. Check the generated files for results."
echo "Remember: Use these tools responsibly and ethically!"