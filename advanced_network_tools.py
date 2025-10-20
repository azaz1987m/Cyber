#!/usr/bin/env python3
"""
Advanced Network Security Tools - Educational Purpose Only
==========================================================

Advanced network security utilities for educational and ethical testing purposes.
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
import hashlib
import base64
import re

class AdvancedNetworkTools:
    def __init__(self):
        self.results = []
        self.verbose = False
        
    def log(self, message, level="INFO"):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

class ARPSpoofDetector:
    """Detect ARP spoofing attacks"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        self.arp_table = {}
        
    def monitor_arp_traffic(self, interface="eth0"):
        """Monitor ARP traffic for spoofing"""
        self.toolkit.log(f"Monitoring ARP traffic on {interface}")
        
        def arp_handler(packet):
            if packet.haslayer(ARP):
                arp = packet[ARP]
                ip = arp.psrc
                mac = arp.hwsrc
                
                if ip in self.arp_table:
                    if self.arp_table[ip] != mac:
                        self.toolkit.log(f"ARP SPOOFING DETECTED! IP {ip} changed from {self.arp_table[ip]} to {mac}", "WARNING")
                else:
                    self.arp_table[ip] = mac
                    self.toolkit.log(f"New ARP entry: {ip} -> {mac}")
        
        try:
            sniff(iface=interface, prn=arp_handler, filter="arp")
        except Exception as e:
            self.toolkit.log(f"ARP monitoring failed: {str(e)}", "ERROR")

class DNSSpoofDetector:
    """Detect DNS spoofing attacks"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        self.dns_cache = {}
        
    def monitor_dns_traffic(self, interface="eth0"):
        """Monitor DNS traffic for spoofing"""
        self.toolkit.log(f"Monitoring DNS traffic on {interface}")
        
        def dns_handler(packet):
            if packet.haslayer(DNS) and packet[DNS].qr == 1:  # DNS response
                dns = packet[DNS]
                if dns.an:
                    for answer in dns.an:
                        if answer.type == 1:  # A record
                            domain = answer.rrname.decode('utf-8').rstrip('.')
                            ip = answer.rdata
                            
                            if domain in self.dns_cache:
                                if self.dns_cache[domain] != ip:
                                    self.toolkit.log(f"DNS SPOOFING DETECTED! {domain} changed from {self.dns_cache[domain]} to {ip}", "WARNING")
                            else:
                                self.dns_cache[domain] = ip
                                self.toolkit.log(f"New DNS entry: {domain} -> {ip}")
        
        try:
            sniff(iface=interface, prn=dns_handler, filter="udp port 53")
        except Exception as e:
            self.toolkit.log(f"DNS monitoring failed: {str(e)}", "ERROR")

class NetworkIntrusionDetector:
    """Basic network intrusion detection system"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        self.suspicious_activities = []
        self.attack_patterns = {
            'port_scan': r'(\d+\.\d+\.\d+\.\d+).*?(\d+\.\d+\.\d+\.\d+).*?(\d+)',
            'syn_flood': r'SYN.*?(\d+\.\d+\.\d+\.\d+)',
            'brute_force': r'(\d+\.\d+\.\d+\.\d+).*?Failed password'
        }
        
    def analyze_traffic(self, packet):
        """Analyze network traffic for suspicious patterns"""
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            
            # Check for port scanning patterns
            if packet.haslayer(TCP):
                tcp = packet[TCP]
                if tcp.flags == 2:  # SYN flag
                    self.check_syn_scan(src_ip, dst_ip, tcp.dport)
            
            # Check for unusual traffic patterns
            self.check_traffic_volume(src_ip)
            
    def check_syn_scan(self, src_ip, dst_ip, port):
        """Check for SYN scan patterns"""
        # This is a simplified check - in reality, you'd track over time
        self.toolkit.log(f"SYN packet from {src_ip} to {dst_ip}:{port}")
        
    def check_traffic_volume(self, src_ip):
        """Check for unusual traffic volume"""
        # Simplified volume check
        current_time = time.time()
        # In a real implementation, you'd track traffic over time windows
        pass

class WirelessSecurityTester:
    """Wireless network security testing utilities"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        
    def scan_wireless_networks(self):
        """Scan for wireless networks"""
        self.toolkit.log("Scanning for wireless networks...")
        try:
            # This would require additional tools like airodump-ng
            result = subprocess.run(['iwlist', 'scan'], capture_output=True, text=True)
            if result.returncode == 0:
                self.toolkit.log("Wireless scan completed")
                return result.stdout
            else:
                self.toolkit.log("Wireless scan failed - ensure you have proper tools installed", "ERROR")
                return None
        except FileNotFoundError:
            self.toolkit.log("iwlist not found - install wireless-tools", "ERROR")
            return None
    
    def check_wifi_security(self, network_info):
        """Check wireless network security"""
        security_issues = []
        
        if "WEP" in network_info:
            security_issues.append("WEP encryption detected - highly vulnerable")
        if "WPA" in network_info and "WPA2" not in network_info:
            security_issues.append("WPA encryption detected - consider upgrading to WPA2/WPA3")
        if "Open" in network_info:
            security_issues.append("Open network detected - no encryption")
            
        return security_issues

class CryptographyTester:
    """Cryptography and encryption testing utilities"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        
    def test_encryption_strength(self, algorithm, key_size):
        """Test encryption algorithm strength"""
        strength_ratings = {
            'AES': {128: 'Good', 192: 'Better', 256: 'Excellent'},
            'RSA': {1024: 'Weak', 2048: 'Good', 3072: 'Better', 4096: 'Excellent'},
            'DES': {56: 'Very Weak'},
            '3DES': {168: 'Weak'}
        }
        
        if algorithm in strength_ratings:
            if key_size in strength_ratings[algorithm]:
                return strength_ratings[algorithm][key_size]
            else:
                return "Unknown key size"
        else:
            return "Unknown algorithm"
    
    def generate_secure_password(self, length=16):
        """Generate a secure password"""
        import secrets
        import string
        
        characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
    
    def hash_password(self, password, algorithm='sha256'):
        """Hash a password using specified algorithm"""
        if algorithm == 'sha256':
            return hashlib.sha256(password.encode()).hexdigest()
        elif algorithm == 'sha512':
            return hashlib.sha512(password.encode()).hexdigest()
        elif algorithm == 'md5':
            return hashlib.md5(password.encode()).hexdigest()
        else:
            return None

class SocialEngineeringTester:
    """Social engineering awareness and testing utilities"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        
    def check_email_security(self, email_content):
        """Check email for potential security issues"""
        issues = []
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'urgent.*password',
            r'click.*here.*immediately',
            r'verify.*account.*now',
            r'limited.*time.*offer',
            r'act.*now.*or.*lose'
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, email_content, re.IGNORECASE):
                issues.append(f"Suspicious pattern detected: {pattern}")
        
        # Check for suspicious links
        link_pattern = r'https?://[^\s]+'
        links = re.findall(link_pattern, email_content)
        for link in links:
            if any(domain in link for domain in ['bit.ly', 'tinyurl.com', 'goo.gl']):
                issues.append(f"Shortened URL detected: {link}")
        
        return issues
    
    def test_phishing_resistance(self, url):
        """Test URL for potential phishing indicators"""
        issues = []
        
        # Check for suspicious domains
        suspicious_domains = ['bit.ly', 'tinyurl.com', 'goo.gl']
        for domain in suspicious_domains:
            if domain in url:
                issues.append(f"Shortened URL service detected: {domain}")
        
        # Check for IP addresses in URLs
        ip_pattern = r'\d+\.\d+\.\d+\.\d+'
        if re.search(ip_pattern, url):
            issues.append("IP address in URL detected")
        
        return issues

def main():
    """Main function for advanced tools"""
    parser = argparse.ArgumentParser(description="Advanced Network Security Tools - Educational Purpose Only")
    parser.add_argument("--arp-monitor", action="store_true", help="Monitor for ARP spoofing")
    parser.add_argument("--dns-monitor", action="store_true", help="Monitor for DNS spoofing")
    parser.add_argument("--wifi-scan", action="store_true", help="Scan wireless networks")
    parser.add_argument("--crypto-test", action="store_true", help="Test cryptography")
    parser.add_argument("--social-test", action="store_true", help="Test social engineering")
    parser.add_argument("-i", "--interface", default="eth0", help="Network interface")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    toolkit = AdvancedNetworkTools()
    toolkit.verbose = args.verbose
    
    toolkit.log("Starting Advanced Network Security Tools")
    toolkit.log("WARNING: Only use on networks you own or have permission to test!")
    
    if args.arp_monitor:
        arp_detector = ARPSpoofDetector(toolkit)
        arp_detector.monitor_arp_traffic(args.interface)
    
    if args.dns_monitor:
        dns_detector = DNSSpoofDetector(toolkit)
        dns_detector.monitor_dns_traffic(args.interface)
    
    if args.wifi_scan:
        wifi_tester = WirelessSecurityTester(toolkit)
        networks = wifi_tester.scan_wireless_networks()
        if networks:
            security_issues = wifi_tester.check_wifi_security(networks)
            for issue in security_issues:
                toolkit.log(f"Security issue: {issue}", "WARNING")
    
    if args.crypto_test:
        crypto_tester = CryptographyTester(toolkit)
        toolkit.log("Testing encryption algorithms...")
        toolkit.log(f"AES-256: {crypto_tester.test_encryption_strength('AES', 256)}")
        toolkit.log(f"RSA-2048: {crypto_tester.test_encryption_strength('RSA', 2048)}")
        
        secure_password = crypto_tester.generate_secure_password()
        toolkit.log(f"Generated secure password: {secure_password}")
        toolkit.log(f"SHA-256 hash: {crypto_tester.hash_password(secure_password)}")
    
    if args.social_test:
        social_tester = SocialEngineeringTester(toolkit)
        toolkit.log("Testing social engineering awareness...")
        
        # Test email content
        test_email = "URGENT: Click here immediately to verify your account or it will be suspended!"
        issues = social_tester.check_email_security(test_email)
        for issue in issues:
            toolkit.log(f"Email security issue: {issue}", "WARNING")
        
        # Test URL
        test_url = "https://bit.ly/suspicious-link"
        url_issues = social_tester.test_phishing_resistance(test_url)
        for issue in url_issues:
            toolkit.log(f"URL security issue: {issue}", "WARNING")

if __name__ == "__main__":
    main()