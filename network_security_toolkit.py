#!/usr/bin/env python3
"""
Network Security Toolkit - Educational Purpose Only
==================================================

This toolkit contains various network security tools for educational and 
ethical testing purposes only. Always ensure you have proper authorization 
before testing any network or system.

Author: Security Researcher
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
    """Advanced port scanner with multiple scanning techniques"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        self.open_ports = []
        self.scan_results = {}
        
    def scan_port(self, target, port, timeout=1):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            sock.close()
            
            if result == 0:
                self.open_ports.append(port)
                service = self.get_service_name(port)
                self.toolkit.log(f"Port {port} ({service}) is open on {target}")
                return True
        except Exception as e:
            if self.toolkit.verbose:
                self.toolkit.log(f"Error scanning port {port}: {e}", "ERROR")
        return False
    
    def get_service_name(self, port):
        """Get common service name for port"""
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 993: "IMAPS",
            995: "POP3S", 3389: "RDP", 5432: "PostgreSQL", 3306: "MySQL",
            1433: "MSSQL", 6379: "Redis", 27017: "MongoDB"
        }
        return services.get(port, "Unknown")
    
    def tcp_scan(self, target, ports, max_threads=100):
        """Perform TCP port scan"""
        self.toolkit.log(f"Starting TCP scan on {target}")
        self.open_ports = []
        
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [executor.submit(self.scan_port, target, port) for port in ports]
            
        self.scan_results[target] = {
            'open_ports': self.open_ports,
            'scan_type': 'TCP',
            'timestamp': datetime.now().isoformat()
        }
        
        return self.open_ports
    
    def udp_scan(self, target, ports, timeout=2):
        """Perform UDP port scan"""
        self.toolkit.log(f"Starting UDP scan on {target}")
        open_udp_ports = []
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(timeout)
                sock.sendto(b'', (target, port))
                data, addr = sock.recvfrom(1024)
                open_udp_ports.append(port)
                self.toolkit.log(f"UDP Port {port} is open on {target}")
            except:
                pass
            finally:
                sock.close()
        
        return open_udp_ports

class VulnerabilityScanner:
    """Basic vulnerability scanner for common services"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        self.vulnerabilities = []
        
    def check_http_vulnerabilities(self, target, port=80):
        """Check for common HTTP vulnerabilities"""
        self.toolkit.log(f"Checking HTTP vulnerabilities on {target}:{port}")
        
        try:
            url = f"http://{target}:{port}"
            response = requests.get(url, timeout=10, allow_redirects=False)
            
            vulns = []
            
            # Check for security headers
            security_headers = [
                'X-Frame-Options', 'X-Content-Type-Options', 
                'X-XSS-Protection', 'Strict-Transport-Security'
            ]
            
            missing_headers = []
            for header in security_headers:
                if header not in response.headers:
                    missing_headers.append(header)
            
            if missing_headers:
                vulns.append({
                    'type': 'Missing Security Headers',
                    'severity': 'Medium',
                    'details': f"Missing headers: {', '.join(missing_headers)}"
                })
            
            # Check server version disclosure
            if 'Server' in response.headers:
                vulns.append({
                    'type': 'Server Version Disclosure',
                    'severity': 'Low',
                    'details': f"Server: {response.headers['Server']}"
                })
            
            # Check for common vulnerable paths
            vulnerable_paths = [
                '/admin', '/phpmyadmin', '/wp-admin', '/.git',
                '/backup', '/test', '/dev', '/api'
            ]
            
            for path in vulnerable_paths:
                try:
                    test_url = f"{url}{path}"
                    test_response = requests.get(test_url, timeout=5)
                    if test_response.status_code == 200:
                        vulns.append({
                            'type': 'Exposed Directory',
                            'severity': 'Medium',
                            'details': f"Exposed path: {path}"
                        })
                except:
                    pass
            
            self.vulnerabilities.extend(vulns)
            return vulns
            
        except Exception as e:
            self.toolkit.log(f"Error checking HTTP vulnerabilities: {e}", "ERROR")
            return []
    
    def check_ssh_vulnerabilities(self, target, port=22):
        """Check SSH configuration"""
        self.toolkit.log(f"Checking SSH vulnerabilities on {target}:{port}")
        
        try:
            # This is a simplified check - in practice, you'd use specialized tools
            vulns = []
            
            # Check if SSH is accessible
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((target, port))
            sock.close()
            
            if result == 0:
                vulns.append({
                    'type': 'SSH Service Detected',
                    'severity': 'Info',
                    'details': f"SSH service running on {target}:{port}"
                })
            
            return vulns
            
        except Exception as e:
            self.toolkit.log(f"Error checking SSH: {e}", "ERROR")
            return []

class NetworkMonitor:
    """Network traffic monitor and analyzer"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        self.packets_captured = 0
        self.suspicious_activities = []
        
    def packet_callback(self, packet):
        """Callback function for packet capture"""
        self.packets_captured += 1
        
        if self.toolkit.verbose:
            self.toolkit.log(f"Captured packet #{self.packets_captured}")
        
        # Analyze packet for suspicious activities
        if packet.haslayer(IP):
            self.analyze_ip_packet(packet)
    
    def analyze_ip_packet(self, packet):
        """Analyze IP packet for suspicious patterns"""
        ip_layer = packet[IP]
        
        # Check for unusual traffic patterns
        if ip_layer.proto == 1:  # ICMP
            if packet.haslayer(ICMP):
                icmp = packet[ICMP]
                if icmp.type == 8:  # Echo request
                    self.suspicious_activities.append({
                        'type': 'ICMP Echo Request',
                        'source': ip_layer.src,
                        'destination': ip_layer.dst,
                        'timestamp': datetime.now().isoformat()
                    })
    
    def start_monitoring(self, interface="eth0", count=100):
        """Start network monitoring"""
        self.toolkit.log(f"Starting network monitoring on {interface}")
        
        try:
            sniff(iface=interface, prn=self.packet_callback, count=count)
            self.toolkit.log(f"Captured {self.packets_captured} packets")
        except Exception as e:
            self.toolkit.log(f"Error during monitoring: {e}", "ERROR")

class SecurityTools:
    """Collection of various security testing tools"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
    
    def ping_sweep(self, network):
        """Perform ping sweep on network range"""
        self.toolkit.log(f"Starting ping sweep on {network}")
        active_hosts = []
        
        try:
            network_obj = ipaddress.ip_network(network, strict=False)
            
            def ping_host(ip):
                try:
                    result = subprocess.run(
                        ['ping', '-c', '1', '-W', '1', str(ip)],
                        capture_output=True, timeout=2
                    )
                    if result.returncode == 0:
                        active_hosts.append(str(ip))
                        self.toolkit.log(f"Host {ip} is alive")
                except:
                    pass
            
            with ThreadPoolExecutor(max_workers=50) as executor:
                executor.map(ping_host, network_obj.hosts())
            
            return active_hosts
            
        except Exception as e:
            self.toolkit.log(f"Error during ping sweep: {e}", "ERROR")
            return []
    
    def dns_enumeration(self, domain):
        """Perform DNS enumeration"""
        self.toolkit.log(f"Starting DNS enumeration for {domain}")
        
        dns_records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
        
        for record_type in record_types:
            try:
                result = subprocess.run(
                    ['nslookup', '-type=' + record_type, domain],
                    capture_output=True, text=True, timeout=10
                )
                dns_records[record_type] = result.stdout
            except Exception as e:
                self.toolkit.log(f"Error querying {record_type} record: {e}", "ERROR")
        
        return dns_records
    
    def whois_lookup(self, target):
        """Perform WHOIS lookup"""
        self.toolkit.log(f"Performing WHOIS lookup for {target}")
        
        try:
            result = subprocess.run(
                ['whois', target],
                capture_output=True, text=True, timeout=30
            )
            return result.stdout
        except Exception as e:
            self.toolkit.log(f"Error during WHOIS lookup: {e}", "ERROR")
            return ""

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description="Network Security Toolkit - Educational Use Only")
    parser.add_argument("target", help="Target IP address or domain")
    parser.add_argument("-p", "--ports", help="Port range (e.g., 1-1000)", default="1-1000")
    parser.add_argument("-t", "--threads", type=int, help="Number of threads", default=100)
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--scan-type", choices=["tcp", "udp", "both"], default="tcp", help="Scan type")
    parser.add_argument("--vuln-scan", action="store_true", help="Perform vulnerability scan")
    parser.add_argument("--monitor", action="store_true", help="Start network monitoring")
    parser.add_argument("--ping-sweep", help="Perform ping sweep on network (e.g., 192.168.1.0/24)")
    parser.add_argument("--dns-enum", help="Perform DNS enumeration on domain")
    parser.add_argument("--whois", action="store_true", help="Perform WHOIS lookup")
    
    args = parser.parse_args()
    
    # Initialize toolkit
    toolkit = NetworkSecurityToolkit()
    toolkit.verbose = args.verbose
    
    # Parse port range
    if '-' in args.ports:
        start_port, end_port = map(int, args.ports.split('-'))
        ports = list(range(start_port, end_port + 1))
    else:
        ports = [int(args.ports)]
    
    print("=" * 60)
    print("NETWORK SECURITY TOOLKIT - EDUCATIONAL USE ONLY")
    print("=" * 60)
    print("WARNING: Only use this toolkit on systems you own or have")
    print("explicit permission to test. Unauthorized access is illegal!")
    print("=" * 60)
    
    # Port scanning
    if args.scan_type in ["tcp", "both"]:
        scanner = PortScanner(toolkit)
        open_ports = scanner.tcp_scan(args.target, ports, args.threads)
        toolkit.results.append({
            'target': args.target,
            'scan_type': 'TCP',
            'open_ports': open_ports,
            'timestamp': datetime.now().isoformat()
        })
    
    if args.scan_type in ["udp", "both"]:
        scanner = PortScanner(toolkit)
        open_udp_ports = scanner.udp_scan(args.target, ports[:50])  # Limit UDP scan
        toolkit.results.append({
            'target': args.target,
            'scan_type': 'UDP',
            'open_ports': open_udp_ports,
            'timestamp': datetime.now().isoformat()
        })
    
    # Vulnerability scanning
    if args.vuln_scan:
        vuln_scanner = VulnerabilityScanner(toolkit)
        http_vulns = vuln_scanner.check_http_vulnerabilities(args.target)
        ssh_vulns = vuln_scanner.check_ssh_vulnerabilities(args.target)
        
        all_vulns = http_vulns + ssh_vulns
        if all_vulns:
            toolkit.results.append({
                'target': args.target,
                'vulnerabilities': all_vulns,
                'timestamp': datetime.now().isoformat()
            })
    
    # Network monitoring
    if args.monitor:
        monitor = NetworkMonitor(toolkit)
        monitor.start_monitoring()
    
    # Ping sweep
    if args.ping_sweep:
        tools = SecurityTools(toolkit)
        active_hosts = tools.ping_sweep(args.ping_sweep)
        toolkit.results.append({
            'network': args.ping_sweep,
            'active_hosts': active_hosts,
            'timestamp': datetime.now().isoformat()
        })
    
    # DNS enumeration
    if args.dns_enum:
        tools = SecurityTools(toolkit)
        dns_results = tools.dns_enumeration(args.dns_enum)
        toolkit.results.append({
            'domain': args.dns_enum,
            'dns_records': dns_results,
            'timestamp': datetime.now().isoformat()
        })
    
    # WHOIS lookup
    if args.whois:
        tools = SecurityTools(toolkit)
        whois_result = tools.whois_lookup(args.target)
        toolkit.results.append({
            'target': args.target,
            'whois_data': whois_result,
            'timestamp': datetime.now().isoformat()
        })
    
    # Save results
    if toolkit.results:
        toolkit.save_results()
        print(f"\nScan completed. Results saved to security_scan_results.json")
    else:
        print("No results to save.")

if __name__ == "__main__":
    main()