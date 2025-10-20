# Network Security Toolkit

A comprehensive educational toolkit for learning network security concepts and ethical security testing.

## ⚠️ Legal Notice

**This toolkit is for EDUCATIONAL PURPOSES ONLY. Only use on networks you own or have explicit permission to test. Unauthorized use is illegal and unethical.**

## 🚀 Quick Start

### Installation

```bash
# Install required dependencies
pip install -r requirements.txt

# Make scripts executable
chmod +x network_security_toolkit.py
chmod +x advanced_network_tools.py
```

### Basic Usage

```bash
# Port scan a target (replace with your own IP)
python3 network_security_toolkit.py 192.168.1.1 -p 1-1000

# Advanced monitoring
python3 advanced_network_tools.py --arp-monitor --dns-monitor
```

## 📁 Toolkit Components

### 1. Network Security Toolkit (`network_security_toolkit.py`)
- **Port Scanner**: Scan for open ports on target systems
- **Vulnerability Scanner**: Check for common security issues
- **Network Monitor**: Monitor network traffic
- **Security Tester**: Test password strength and common vulnerabilities

### 2. Advanced Network Tools (`advanced_network_tools.py`)
- **ARP Spoofing Detector**: Detect ARP poisoning attacks
- **DNS Spoofing Detector**: Monitor for DNS hijacking
- **Wireless Security Tester**: Scan and analyze WiFi networks
- **Cryptography Tester**: Test encryption algorithms
- **Social Engineering Tester**: Analyze phishing attempts

## 🔧 Features

### Port Scanning
- Multi-threaded port scanning
- Common port detection
- Service identification
- Custom port ranges

### Vulnerability Assessment
- HTTP security header analysis
- SSL/TLS configuration checking
- Common vulnerability detection
- Security report generation

### Network Monitoring
- Real-time traffic analysis
- Packet capture and analysis
- Protocol identification
- Traffic pattern detection

### Security Testing
- Password strength analysis
- Encryption algorithm testing
- Social engineering awareness
- Phishing detection

## 📊 Example Output

```
[2024-01-15 10:30:45] [INFO] Starting Network Security Toolkit
[2024-01-15 10:30:45] [WARNING] Only use on networks you own or have permission to test!
[2024-01-15 10:30:46] [INFO] Scanning 192.168.1.1 on ports [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
[2024-01-15 10:30:47] [INFO] Port 22 is open on 192.168.1.1
[2024-01-15 10:30:47] [INFO] Port 80 is open on 192.168.1.1
[2024-01-15 10:30:48] [INFO] Port 443 is open on 192.168.1.1

==================================================
SCAN SUMMARY
==================================================
Target: 192.168.1.1
Open Ports: [22, 80, 443]
Vulnerabilities Found: 0
Results saved to: security_scan_results.json
```

## 🛡️ Security Features

### Detection Capabilities
- ARP spoofing detection
- DNS hijacking detection
- Port scanning detection
- Suspicious traffic patterns
- Wireless security issues

### Analysis Tools
- Packet analysis
- Protocol identification
- Traffic volume monitoring
- Security header analysis
- Encryption strength testing

## 📚 Educational Value

This toolkit helps you learn:

1. **Network Fundamentals**: Understanding TCP/IP, ports, and protocols
2. **Security Concepts**: Vulnerabilities, attacks, and defenses
3. **Ethical Hacking**: Proper methodology and legal considerations
4. **Defensive Security**: How to protect networks and systems
5. **Cryptography**: Encryption, hashing, and secure communications

## 🔒 Ethical Guidelines

### ✅ Do:
- Use only on your own networks
- Learn and understand security concepts
- Practice defensive security measures
- Report vulnerabilities responsibly
- Follow all applicable laws

### ❌ Don't:
- Use on unauthorized networks
- Perform malicious attacks
- Violate privacy or confidentiality
- Exploit vulnerabilities maliciously
- Break any laws or regulations

## 📖 Usage Examples

### Basic Port Scan
```bash
python3 network_security_toolkit.py 192.168.1.1 -p 1-1000 -v
```

### Monitor for Attacks
```bash
python3 advanced_network_tools.py --arp-monitor --dns-monitor -i eth0
```

### Test Wireless Security
```bash
python3 advanced_network_tools.py --wifi-scan
```

### Test Cryptography
```bash
python3 advanced_network_tools.py --crypto-test
```

## 🛠️ Requirements

- Python 3.7+
- scapy
- requests
- Network interface access (for monitoring)

## 📄 License

Educational Use Only - See `ethical_guidelines.md` for complete terms.

## 🤝 Contributing

Contributions are welcome! Please ensure all additions:
- Are for educational purposes only
- Include proper ethical warnings
- Follow responsible disclosure practices
- Focus on defensive security

## 📞 Support

For questions about ethical use or legal concerns:
- Review `ethical_guidelines.md`
- Consult with legal professionals
- Contact cybersecurity education organizations

---

**Remember: Use these tools responsibly to learn, protect, and improve security!**