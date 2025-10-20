#!/usr/bin/env python3
"""
Network Security Toolkit - Educational Purpose Only
==================================================

This toolkit is designed for educational purposes and ethical security testing.
Only use on networks you own or have explicit permission to test.

Author: Security Education
License: Educational Use Only
"""

import socket
import threading
import subprocess
import sys
import time
import json
import argparse
from datetime import datetime
from scapy.all import *
import requests
from concurrent.futures import ThreadPoolExecutor
import ipaddress

class NetworkSecurityToolkit:
    def __init__(self):
        self.results = []
        self.verbose = False
        
    def log(self, message, level="INFO"):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def save_results(self, filename="security_scan_results.json"):
        """Save scan results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        self.log(f"Results saved to {filename}")

class PortScanner:
    """Port scanning utility for network reconnaissance"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        
    def scan_port(self, target, port, timeout=1):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            sock.close()
            
            if result == 0:
                return port, "open"
            else:
                return port, "closed"
        except Exception as e:
            return port, f"error: {str(e)}"
    
    def scan_ports(self, target, ports, max_threads=100):
        """Scan multiple ports on a target"""
        self.toolkit.log(f"Scanning {target} on ports {ports}")
        open_ports = []
        
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [executor.submit(self.scan_port, target, port) for port in ports]
            
            for future in futures:
                port, status = future.result()
                if status == "open":
                    open_ports.append(port)
                    self.toolkit.log(f"Port {port} is open on {target}")
        
        return open_ports

class VulnerabilityScanner:
    """Basic vulnerability scanner"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        self.vulnerabilities = []
        
    def check_http_security(self, target, port=80):
        """Check basic HTTP security headers"""
        try:
            url = f"http://{target}:{port}"
            response = requests.get(url, timeout=5, allow_redirects=True)
            
            security_headers = {
                'X-Frame-Options': 'Missing',
                'X-Content-Type-Options': 'Missing',
                'X-XSS-Protection': 'Missing',
                'Strict-Transport-Security': 'Missing',
                'Content-Security-Policy': 'Missing'
            }
            
            for header in security_headers:
                if header in response.headers:
                    security_headers[header] = response.headers[header]
            
            return security_headers
        except Exception as e:
            self.toolkit.log(f"HTTP security check failed: {str(e)}", "ERROR")
            return {}
    
    def check_ssl_configuration(self, target, port=443):
        """Check SSL/TLS configuration"""
        try:
            import ssl
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((target, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=target) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    
                    return {
                        'certificate': cert,
                        'cipher': cipher,
                        'protocol': ssock.version()
                    }
        except Exception as e:
            self.toolkit.log(f"SSL check failed: {str(e)}", "ERROR")
            return {}

class NetworkMonitor:
    """Network traffic monitoring utility"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        self.captured_packets = []
        
    def packet_handler(self, packet):
        """Handle captured packets"""
        if packet.haslayer(IP):
            packet_info = {
                'timestamp': datetime.now().isoformat(),
                'src_ip': packet[IP].src,
                'dst_ip': packet[IP].dst,
                'protocol': packet[IP].proto,
                'size': len(packet)
            }
            
            if packet.haslayer(TCP):
                packet_info['src_port'] = packet[TCP].sport
                packet_info['dst_port'] = packet[TCP].dport
                packet_info['flags'] = packet[TCP].flags
            elif packet.haslayer(UDP):
                packet_info['src_port'] = packet[UDP].sport
                packet_info['dst_port'] = packet[UDP].dport
            
            self.captured_packets.append(packet_info)
            self.toolkit.log(f"Captured packet: {packet_info}")
    
    def start_monitoring(self, interface="eth0", count=100):
        """Start network monitoring"""
        self.toolkit.log(f"Starting network monitoring on {interface}")
        try:
            sniff(iface=interface, prn=self.packet_handler, count=count)
        except Exception as e:
            self.toolkit.log(f"Monitoring failed: {str(e)}", "ERROR")

class SecurityTester:
    """Security testing utilities"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        
    def test_password_strength(self, password):
        """Test password strength"""
        score = 0
        feedback = []
        
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Password should be at least 8 characters")
            
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Password should contain uppercase letters")
            
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Password should contain lowercase letters")
            
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Password should contain numbers")
            
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
        else:
            feedback.append("Password should contain special characters")
        
        return {
            'score': score,
            'max_score': 5,
            'feedback': feedback,
            'strength': 'Weak' if score < 3 else 'Medium' if score < 5 else 'Strong'
        }
    
    def check_common_vulnerabilities(self, target):
        """Check for common vulnerabilities"""
        vulnerabilities = []
        
        # Check for common open ports that might indicate vulnerabilities
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
        scanner = PortScanner(self.toolkit)
        open_ports = scanner.scan_ports(target, common_ports)
        
        if 21 in open_ports:
            vulnerabilities.append("FTP service detected - check for anonymous access")
        if 23 in open_ports:
            vulnerabilities.append("Telnet service detected - insecure protocol")
        if 25 in open_ports:
            vulnerabilities.append("SMTP service detected - check for open relay")
            
        return vulnerabilities

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Network Security Toolkit - Educational Purpose Only")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", help="Ports to scan (e.g., 1-1000 or 80,443,22)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-o", "--output", help="Output file for results")
    
    args = parser.parse_args()
    
    # Initialize toolkit
    toolkit = NetworkSecurityToolkit()
    toolkit.verbose = args.verbose
    
    # Parse ports
    if args.ports:
        if '-' in args.ports:
            start, end = map(int, args.ports.split('-'))
            ports = list(range(start, end + 1))
        else:
            ports = [int(p) for p in args.ports.split(',')]
    else:
        ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
    
    toolkit.log("Starting Network Security Toolkit")
    toolkit.log("WARNING: Only use on networks you own or have permission to test!")
    
    # Port scanning
    scanner = PortScanner(toolkit)
    open_ports = scanner.scan_ports(args.target, ports)
    
    # Vulnerability scanning
    vuln_scanner = VulnerabilityScanner(toolkit)
    http_security = vuln_scanner.check_http_security(args.target)
    ssl_config = vuln_scanner.check_ssl_configuration(args.target)
    
    # Security testing
    security_tester = SecurityTester(toolkit)
    vulnerabilities = security_tester.check_common_vulnerabilities(args.target)
    
    # Compile results
    results = {
        'target': args.target,
        'scan_time': datetime.now().isoformat(),
        'open_ports': open_ports,
        'http_security': http_security,
        'ssl_configuration': ssl_config,
        'vulnerabilities': vulnerabilities
    }
    
    toolkit.results = results
    
    # Save results
    output_file = args.output or "security_scan_results.json"
    toolkit.save_results(output_file)
    
    # Print summary
    print("\n" + "="*50)
    print("SCAN SUMMARY")
    print("="*50)
    print(f"Target: {args.target}")
    print(f"Open Ports: {open_ports}")
    print(f"Vulnerabilities Found: {len(vulnerabilities)}")
    for vuln in vulnerabilities:
        print(f"  - {vuln}")
    print(f"Results saved to: {output_file}")

if __name__ == "__main__":
    main()