#!/usr/bin/env python3
"""
Network Security Education Toolkit
==================================

A comprehensive educational program for learning network security concepts,
ethical hacking, and penetration testing fundamentals.

IMPORTANT LEGAL NOTICE:
This toolkit is for EDUCATIONAL PURPOSES ONLY. Use only on networks you own
or have explicit written permission to test. Unauthorized network scanning
or penetration testing is illegal in most jurisdictions.

Author: Educational Security Toolkit
License: MIT (Educational Use Only)
"""

import socket
import threading
import time
import subprocess
import sys
import argparse
import ipaddress
from datetime import datetime
import json
import os

class NetworkSecurityToolkit:
    """Main class for the Network Security Education Toolkit"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.banner = """
╔══════════════════════════════════════════════════════════════╗
║                Network Security Education Toolkit            ║
║                        Version 1.0.0                        ║
║                                                              ║
║  WARNING: FOR EDUCATIONAL PURPOSES ONLY                     ║
║  Use only on networks you own or have permission to test    ║
╚══════════════════════════════════════════════════════════════╝
        """
    
    def display_banner(self):
        """Display the toolkit banner"""
        print(self.banner)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 62)
    
    def show_menu(self):
        """Display the main menu"""
        menu = """
Available Modules:
1. Network Discovery & Scanning
2. Port Scanning & Service Detection
3. Vulnerability Assessment
4. Network Monitoring
5. Security Testing Utilities
6. Educational Resources
7. Legal & Ethical Guidelines
8. Exit

Select an option (1-8): """
        return input(menu)
    
    def run(self):
        """Main program loop"""
        self.display_banner()
        
        while True:
            try:
                choice = self.show_menu()
                
                if choice == '1':
                    NetworkScanner().run()
                elif choice == '2':
                    PortScanner().run()
                elif choice == '3':
                    VulnerabilityAssessment().run()
                elif choice == '4':
                    NetworkMonitor().run()
                elif choice == '5':
                    SecurityTester().run()
                elif choice == '6':
                    EducationalResources().display()
                elif choice == '7':
                    EthicalGuidelines().display()
                elif choice == '8':
                    print("\nThank you for using the Network Security Education Toolkit!")
                    print("Remember: Always use these tools ethically and legally.")
                    break
                else:
                    print("\nInvalid choice. Please select 1-8.")
                    
            except KeyboardInterrupt:
                print("\n\nProgram interrupted by user.")
                break
            except Exception as e:
                print(f"\nError: {e}")

class NetworkScanner:
    """Network discovery and scanning utilities"""
    
    def __init__(self):
        self.timeout = 1
    
    def ping_host(self, host):
        """Ping a single host to check if it's alive"""
        try:
            # Use system ping command
            result = subprocess.run(['ping', '-c', '1', '-W', '1', host], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def scan_network(self, network):
        """Scan a network range for live hosts"""
        print(f"\nScanning network: {network}")
        print("=" * 40)
        
        try:
            net = ipaddress.IPv4Network(network, strict=False)
            live_hosts = []
            
            for host in net.hosts():
                host_str = str(host)
                if self.ping_host(host_str):
                    print(f"[+] Host {host_str} is alive")
                    live_hosts.append(host_str)
                else:
                    print(f"[-] Host {host_str} is down", end='\r')
            
            print(f"\n\nScan complete. Found {len(live_hosts)} live hosts.")
            return live_hosts
            
        except Exception as e:
            print(f"Error scanning network: {e}")
            return []
    
    def get_local_network(self):
        """Get the local network range"""
        try:
            # Get default gateway
            result = subprocess.run(['ip', 'route', 'show', 'default'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                gateway = result.stdout.split()[2]
                # Assume /24 network
                network_parts = gateway.split('.')
                network = f"{'.'.join(network_parts[:3])}.0/24"
                return network
        except:
            pass
        return "192.168.1.0/24"  # Default fallback
    
    def run(self):
        """Run the network scanner module"""
        print("\n" + "="*50)
        print("         NETWORK DISCOVERY MODULE")
        print("="*50)
        
        print("\nOptions:")
        print("1. Scan local network")
        print("2. Scan custom network range")
        print("3. Ping single host")
        print("4. Back to main menu")
        
        choice = input("\nSelect option (1-4): ")
        
        if choice == '1':
            network = self.get_local_network()
            print(f"Detected local network: {network}")
            confirm = input("Proceed with scan? (y/N): ")
            if confirm.lower() == 'y':
                self.scan_network(network)
        
        elif choice == '2':
            network = input("Enter network range (e.g., 192.168.1.0/24): ")
            try:
                ipaddress.IPv4Network(network, strict=False)
                confirm = input(f"Scan {network}? (y/N): ")
                if confirm.lower() == 'y':
                    self.scan_network(network)
            except:
                print("Invalid network format!")
        
        elif choice == '3':
            host = input("Enter host IP or hostname: ")
            if self.ping_host(host):
                print(f"[+] {host} is alive")
            else:
                print(f"[-] {host} is not responding")
        
        input("\nPress Enter to continue...")

class PortScanner:
    """Port scanning and service detection utilities"""
    
    def __init__(self):
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 
                           443, 993, 995, 1723, 3306, 3389, 5900, 8080]
        self.timeout = 1
    
    def scan_port(self, host, port):
        """Scan a single port on a host"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def get_service_name(self, port):
        """Get common service name for a port"""
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 111: "RPC", 135: "RPC", 139: "NetBIOS",
            143: "IMAP", 443: "HTTPS", 993: "IMAPS", 995: "POP3S",
            1723: "PPTP", 3306: "MySQL", 3389: "RDP", 5900: "VNC", 8080: "HTTP-Alt"
        }
        return services.get(port, "Unknown")
    
    def scan_host_ports(self, host, ports=None):
        """Scan multiple ports on a host"""
        if ports is None:
            ports = self.common_ports
        
        print(f"\nScanning {host} for open ports...")
        print("-" * 40)
        
        open_ports = []
        for port in ports:
            if self.scan_port(host, port):
                service = self.get_service_name(port)
                print(f"[+] Port {port:5d} - {service:10s} - OPEN")
                open_ports.append((port, service))
            else:
                print(f"[-] Port {port:5d} - CLOSED", end='\r')
        
        print(f"\n\nScan complete. Found {len(open_ports)} open ports.")
        return open_ports
    
    def banner_grab(self, host, port):
        """Attempt to grab service banner"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((host, port))
            
            # Send HTTP request for web services
            if port in [80, 8080]:
                sock.send(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            return banner.strip()
        except:
            return None
    
    def run(self):
        """Run the port scanner module"""
        print("\n" + "="*50)
        print("           PORT SCANNER MODULE")
        print("="*50)
        
        print("\nOptions:")
        print("1. Scan common ports")
        print("2. Scan custom port range")
        print("3. Scan specific ports")
        print("4. Banner grabbing")
        print("5. Back to main menu")
        
        choice = input("\nSelect option (1-5): ")
        
        if choice in ['1', '2', '3']:
            host = input("Enter target host: ")
            
            if choice == '1':
                self.scan_host_ports(host)
            
            elif choice == '2':
                try:
                    start = int(input("Start port: "))
                    end = int(input("End port: "))
                    ports = list(range(start, end + 1))
                    self.scan_host_ports(host, ports)
                except ValueError:
                    print("Invalid port numbers!")
            
            elif choice == '3':
                port_input = input("Enter ports (comma-separated): ")
                try:
                    ports = [int(p.strip()) for p in port_input.split(',')]
                    self.scan_host_ports(host, ports)
                except ValueError:
                    print("Invalid port format!")
        
        elif choice == '4':
            host = input("Enter target host: ")
            port = int(input("Enter port: "))
            banner = self.banner_grab(host, port)
            if banner:
                print(f"\nBanner from {host}:{port}:")
                print("-" * 30)
                print(banner)
            else:
                print("No banner received or connection failed.")
        
        input("\nPress Enter to continue...")

class VulnerabilityAssessment:
    """Basic vulnerability assessment utilities"""
    
    def __init__(self):
        self.vulnerabilities = []
    
    def check_default_credentials(self, host, port, service):
        """Check for default credentials (educational simulation)"""
        default_creds = {
            'ssh': [('admin', 'admin'), ('root', 'root'), ('admin', 'password')],
            'ftp': [('anonymous', ''), ('admin', 'admin'), ('ftp', 'ftp')],
            'telnet': [('admin', 'admin'), ('root', 'root')],
            'http': [('admin', 'admin'), ('admin', 'password')]
        }
        
        service_lower = service.lower()
        if any(s in service_lower for s in default_creds.keys()):
            print(f"[!] {host}:{port} ({service}) - Check for default credentials")
            return True
        return False
    
    def check_outdated_services(self, host, port, service, banner=None):
        """Check for potentially outdated services"""
        vulnerable_patterns = [
            'apache/2.2', 'nginx/1.0', 'openssh_5', 'microsoft-iis/6.0',
            'vsftpd 2.3.4', 'proftpd 1.3.3'
        ]
        
        if banner:
            banner_lower = banner.lower()
            for pattern in vulnerable_patterns:
                if pattern in banner_lower:
                    print(f"[!] {host}:{port} - Potentially vulnerable service: {pattern}")
                    return True
        
        # Check for commonly vulnerable services
        if service.lower() in ['telnet', 'ftp', 'rlogin']:
            print(f"[!] {host}:{port} - Insecure service detected: {service}")
            return True
        
        return False
    
    def check_ssl_configuration(self, host, port):
        """Basic SSL/TLS configuration check"""
        if port in [443, 993, 995]:
            try:
                import ssl
                context = ssl.create_default_context()
                with socket.create_connection((host, port), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=host) as ssock:
                        cert = ssock.getpeercert()
                        print(f"[+] {host}:{port} - SSL certificate found")
                        if cert:
                            print(f"    Subject: {cert.get('subject', 'Unknown')}")
                            print(f"    Issuer: {cert.get('issuer', 'Unknown')}")
                        return True
            except Exception as e:
                print(f"[!] {host}:{port} - SSL connection failed: {e}")
                return False
        return False
    
    def run_assessment(self, host, open_ports):
        """Run vulnerability assessment on a host"""
        print(f"\nRunning vulnerability assessment on {host}")
        print("=" * 50)
        
        vulnerabilities_found = 0
        
        for port, service in open_ports:
            # Check for default credentials
            if self.check_default_credentials(host, port, service):
                vulnerabilities_found += 1
            
            # Check for outdated services
            if self.check_outdated_services(host, port, service):
                vulnerabilities_found += 1
            
            # Check SSL configuration
            if self.check_ssl_configuration(host, port):
                pass  # SSL check is informational
        
        print(f"\nAssessment complete. Found {vulnerabilities_found} potential issues.")
        return vulnerabilities_found
    
    def run(self):
        """Run the vulnerability assessment module"""
        print("\n" + "="*50)
        print("      VULNERABILITY ASSESSMENT MODULE")
        print("="*50)
        
        print("\nThis module performs basic vulnerability checks.")
        print("For comprehensive testing, use dedicated tools like:")
        print("- Nessus, OpenVAS, Nmap NSE scripts")
        
        host = input("\nEnter target host: ")
        
        # First scan for open ports
        scanner = PortScanner()
        open_ports = scanner.scan_host_ports(host)
        
        if open_ports:
            proceed = input("\nProceed with vulnerability assessment? (y/N): ")
            if proceed.lower() == 'y':
                self.run_assessment(host, open_ports)
        else:
            print("No open ports found. Cannot perform assessment.")
        
        input("\nPress Enter to continue...")

class NetworkMonitor:
    """Network monitoring and traffic analysis utilities"""
    
    def __init__(self):
        self.monitoring = False
    
    def monitor_connections(self, duration=30):
        """Monitor network connections (simplified)"""
        print(f"\nMonitoring network connections for {duration} seconds...")
        print("Press Ctrl+C to stop early")
        print("-" * 50)
        
        try:
            start_time = time.time()
            while time.time() - start_time < duration:
                # Use netstat to show connections
                result = subprocess.run(['netstat', '-tuln'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    listening_ports = []
                    for line in lines:
                        if 'LISTEN' in line:
                            parts = line.split()
                            if len(parts) >= 4:
                                listening_ports.append(parts[3])
                    
                    print(f"\rListening ports: {len(listening_ports)}", end='')
                
                time.sleep(2)
        
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")
    
    def show_network_interfaces(self):
        """Display network interfaces"""
        try:
            result = subprocess.run(['ip', 'addr', 'show'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("\nNetwork Interfaces:")
                print("=" * 30)
                print(result.stdout)
        except:
            print("Could not retrieve network interfaces.")
    
    def show_routing_table(self):
        """Display routing table"""
        try:
            result = subprocess.run(['ip', 'route', 'show'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("\nRouting Table:")
                print("=" * 20)
                print(result.stdout)
        except:
            print("Could not retrieve routing table.")
    
    def run(self):
        """Run the network monitor module"""
        print("\n" + "="*50)
        print("        NETWORK MONITORING MODULE")
        print("="*50)
        
        print("\nOptions:")
        print("1. Monitor network connections")
        print("2. Show network interfaces")
        print("3. Show routing table")
        print("4. Back to main menu")
        
        choice = input("\nSelect option (1-4): ")
        
        if choice == '1':
            try:
                duration = int(input("Monitor duration in seconds (default 30): ") or "30")
                self.monitor_connections(duration)
            except ValueError:
                print("Invalid duration!")
        
        elif choice == '2':
            self.show_network_interfaces()
        
        elif choice == '3':
            self.show_routing_table()
        
        input("\nPress Enter to continue...")

class SecurityTester:
    """Security testing utilities"""
    
    def __init__(self):
        pass
    
    def test_password_strength(self, password):
        """Test password strength"""
        score = 0
        feedback = []
        
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Use at least 8 characters")
        
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Include uppercase letters")
        
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Include lowercase letters")
        
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Include numbers")
        
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
        else:
            feedback.append("Include special characters")
        
        strength_levels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
        strength = strength_levels[min(score, 4)]
        
        return strength, score, feedback
    
    def generate_wordlist(self, base_word, variations=True):
        """Generate a simple wordlist for testing"""
        wordlist = [base_word]
        
        if variations:
            # Common variations
            wordlist.extend([
                base_word + "123",
                base_word + "1",
                base_word + "!",
                base_word.capitalize(),
                base_word.upper(),
                base_word + "2023",
                base_word + "2024",
                "123" + base_word,
                base_word[::-1]  # Reversed
            ])
        
        return wordlist
    
    def simulate_brute_force(self, target_password, wordlist):
        """Simulate a brute force attack (educational)"""
        print("\nSimulating brute force attack...")
        print("(This is a simulation for educational purposes)")
        print("-" * 40)
        
        attempts = 0
        for password in wordlist:
            attempts += 1
            print(f"Attempt {attempts}: {password}")
            time.sleep(0.1)  # Simulate delay
            
            if password == target_password:
                print(f"\n[+] Password found: {password}")
                print(f"Attempts required: {attempts}")
                return True
        
        print(f"\n[-] Password not found after {attempts} attempts")
        return False
    
    def run(self):
        """Run the security tester module"""
        print("\n" + "="*50)
        print("        SECURITY TESTING MODULE")
        print("="*50)
        
        print("\nOptions:")
        print("1. Password strength tester")
        print("2. Generate wordlist")
        print("3. Simulate brute force attack")
        print("4. Back to main menu")
        
        choice = input("\nSelect option (1-4): ")
        
        if choice == '1':
            password = input("Enter password to test: ")
            strength, score, feedback = self.test_password_strength(password)
            print(f"\nPassword Strength: {strength} ({score}/5)")
            if feedback:
                print("Recommendations:")
                for item in feedback:
                    print(f"  - {item}")
        
        elif choice == '2':
            base_word = input("Enter base word: ")
            wordlist = self.generate_wordlist(base_word)
            print(f"\nGenerated wordlist ({len(wordlist)} entries):")
            for word in wordlist:
                print(f"  {word}")
        
        elif choice == '3':
            print("This is an educational simulation only!")
            target = input("Enter target password: ")
            base_word = input("Enter base word for wordlist: ")
            wordlist = self.generate_wordlist(base_word)
            self.simulate_brute_force(target, wordlist)
        
        input("\nPress Enter to continue...")

class EducationalResources:
    """Educational resources and learning materials"""
    
    def display(self):
        """Display educational resources"""
        print("\n" + "="*60)
        print("              EDUCATIONAL RESOURCES")
        print("="*60)
        
        resources = """
NETWORK SECURITY FUNDAMENTALS:

1. OSI Model & TCP/IP Stack
   - Understanding network layers
   - Protocols: HTTP/HTTPS, FTP, SSH, DNS, DHCP
   - Packet analysis and network troubleshooting

2. Common Network Attacks:
   - Man-in-the-Middle (MITM)
   - Denial of Service (DoS/DDoS)
   - ARP Spoofing
   - DNS Poisoning
   - Session Hijacking

3. Network Security Tools:
   - Nmap: Network discovery and port scanning
   - Wireshark: Packet capture and analysis
   - Metasploit: Penetration testing framework
   - Burp Suite: Web application security testing
   - Nessus/OpenVAS: Vulnerability scanners

4. Defensive Measures:
   - Firewalls and IDS/IPS
   - Network segmentation
   - VPNs and encryption
   - Access control and authentication
   - Security monitoring and logging

5. Ethical Hacking Methodology:
   - Reconnaissance and information gathering
   - Scanning and enumeration
   - Vulnerability assessment
   - Exploitation (authorized environments only)
   - Post-exploitation and reporting

LEARNING RESOURCES:

Books:
- "The Web Application Hacker's Handbook" by Stuttard & Pinto
- "Network Security Essentials" by William Stallings
- "Hacking: The Art of Exploitation" by Jon Erickson

Online Platforms:
- TryHackMe (tryhackme.com)
- Hack The Box (hackthebox.eu)
- OverTheWire (overthewire.org)
- SANS Cyber Ranges

Certifications:
- CEH (Certified Ethical Hacker)
- OSCP (Offensive Security Certified Professional)
- CISSP (Certified Information Systems Security Professional)
- Security+ (CompTIA Security+)

PRACTICE ENVIRONMENTS:
- VirtualBox/VMware with Kali Linux
- Metasploitable (intentionally vulnerable Linux)
- DVWA (Damn Vulnerable Web Application)
- WebGoat (OWASP)
        """
        
        print(resources)
        input("\nPress Enter to continue...")

class EthicalGuidelines:
    """Ethical guidelines and legal considerations"""
    
    def display(self):
        """Display ethical guidelines"""
        print("\n" + "="*60)
        print("           ETHICAL GUIDELINES & LEGAL NOTICE")
        print("="*60)
        
        guidelines = """
ETHICAL HACKING PRINCIPLES:

1. AUTHORIZATION IS MANDATORY
   - Only test systems you own or have explicit written permission to test
   - Obtain proper authorization before any security testing
   - Respect scope limitations and testing windows

2. DO NO HARM
   - Avoid causing damage to systems or data
   - Don't disrupt normal business operations
   - Use minimal necessary force in testing

3. RESPONSIBLE DISCLOSURE
   - Report vulnerabilities to system owners promptly
   - Allow reasonable time for fixes before public disclosure
   - Follow coordinated disclosure practices

4. MAINTAIN CONFIDENTIALITY
   - Protect sensitive information discovered during testing
   - Don't access or modify data beyond what's necessary for testing
   - Respect privacy and data protection laws

LEGAL CONSIDERATIONS:

⚠️  WARNING: Unauthorized network scanning, penetration testing, or 
   hacking activities are ILLEGAL in most jurisdictions and may result in:
   - Criminal charges and prosecution
   - Civil liability and lawsuits
   - Fines and imprisonment
   - Permanent criminal record

APPLICABLE LAWS (varies by jurisdiction):
- Computer Fraud and Abuse Act (CFAA) - USA
- Computer Misuse Act - UK
- Criminal Code provisions - Canada
- Cybercrime laws - EU and other countries

SAFE PRACTICE ENVIRONMENTS:
✅ Your own systems and networks
✅ Dedicated lab environments (VMs, containers)
✅ Authorized penetration testing with contracts
✅ Educational platforms (TryHackMe, Hack The Box)
✅ Bug bounty programs with clear scope

PROFESSIONAL ETHICS:
- Follow industry standards (NIST, ISO 27001)
- Maintain professional certifications
- Continue education and skill development
- Contribute positively to the security community

REMEMBER: The goal of ethical hacking is to IMPROVE security,
not to cause harm or gain unauthorized access.

"With great power comes great responsibility."
        """
        
        print(guidelines)
        input("\nPress Enter to continue...")

def main():
    """Main function to run the toolkit"""
    try:
        # Check if running as root (for some network operations)
        if os.geteuid() != 0:
            print("Note: Some features may require root privileges.")
            print("Consider running with 'sudo' for full functionality.\n")
        
        toolkit = NetworkSecurityToolkit()
        toolkit.run()
        
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Please report this issue if it persists.")

if __name__ == "__main__":
    main()