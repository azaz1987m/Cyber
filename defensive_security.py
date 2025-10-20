#!/usr/bin/env python3
"""
Defensive Security Tools - Network Protection
=============================================

Tools for protecting networks and detecting threats.
This is the defensive side of network security.

Author: Security Education
License: Educational Use Only
"""

import socket
import threading
import time
import json
import subprocess
import psutil
from datetime import datetime, timedelta
from scapy.all import *
import requests
import hashlib
import re

class NetworkDefender:
    """Main defensive security class"""
    
    def __init__(self):
        self.alerts = []
        self.blocked_ips = set()
        self.monitoring = False
        self.stats = {
            'packets_analyzed': 0,
            'threats_detected': 0,
            'ips_blocked': 0,
            'start_time': datetime.now()
        }
    
    def log_alert(self, message, severity="INFO", source_ip=None):
        """Log security alerts"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'message': message,
            'source_ip': source_ip
        }
        self.alerts.append(alert)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [{severity}] {message}")

class FirewallManager:
    """Basic firewall management and monitoring"""
    
    def __init__(self, defender):
        self.defender = defender
        self.rules = []
        self.blocked_connections = []
    
    def add_firewall_rule(self, rule_type, source_ip, port=None, action="DROP"):
        """Add a firewall rule"""
        rule = {
            'type': rule_type,
            'source_ip': source_ip,
            'port': port,
            'action': action,
            'created': datetime.now().isoformat()
        }
        self.rules.append(rule)
        self.defender.log_alert(f"Added firewall rule: {rule_type} {source_ip} {port} -> {action}")
    
    def block_ip(self, ip_address, reason="Suspicious activity"):
        """Block an IP address"""
        self.defender.blocked_ips.add(ip_address)
        self.add_firewall_rule("BLOCK", ip_address, action="DROP")
        self.defender.log_alert(f"Blocked IP {ip_address}: {reason}", "WARNING", ip_address)
        self.defender.stats['ips_blocked'] += 1
    
    def check_connection(self, source_ip, dest_port):
        """Check if connection should be allowed"""
        for rule in self.rules:
            if rule['source_ip'] == source_ip and rule['port'] == dest_port:
                if rule['action'] == "DROP":
                    return False
        return True

class IntrusionDetectionSystem:
    """Basic Intrusion Detection System"""
    
    def __init__(self, defender):
        self.defender = defender
        self.attack_patterns = {
            'port_scan': {'threshold': 10, 'window': 60, 'counts': {}},
            'syn_flood': {'threshold': 50, 'window': 10, 'counts': {}},
            'brute_force': {'threshold': 5, 'window': 300, 'counts': {}}
        }
        self.connection_attempts = {}
    
    def analyze_packet(self, packet):
        """Analyze packet for attack patterns"""
        self.defender.stats['packets_analyzed'] += 1
        
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            current_time = time.time()
            
            # Port scan detection
            if packet.haslayer(TCP):
                tcp = packet[TCP]
                if tcp.flags == 2:  # SYN flag
                    self.detect_port_scan(src_ip, current_time)
                    self.detect_syn_flood(src_ip, current_time)
            
            # Brute force detection (simplified)
            if packet.haslayer(TCP) and packet[TCP].dport == 22:  # SSH
                self.detect_brute_force(src_ip, current_time)
    
    def detect_port_scan(self, src_ip, timestamp):
        """Detect port scanning attempts"""
        pattern = self.attack_patterns['port_scan']
        
        if src_ip not in pattern['counts']:
            pattern['counts'][src_ip] = []
        
        # Clean old entries
        pattern['counts'][src_ip] = [
            t for t in pattern['counts'][src_ip] 
            if timestamp - t < pattern['window']
        ]
        
        pattern['counts'][src_ip].append(timestamp)
        
        if len(pattern['counts'][src_ip]) > pattern['threshold']:
            self.defender.log_alert(f"Port scan detected from {src_ip}", "WARNING", src_ip)
            self.defender.stats['threats_detected'] += 1
            return True
        return False
    
    def detect_syn_flood(self, src_ip, timestamp):
        """Detect SYN flood attacks"""
        pattern = self.attack_patterns['syn_flood']
        
        if src_ip not in pattern['counts']:
            pattern['counts'][src_ip] = []
        
        # Clean old entries
        pattern['counts'][src_ip] = [
            t for t in pattern['counts'][src_ip] 
            if timestamp - t < pattern['window']
        ]
        
        pattern['counts'][src_ip].append(timestamp)
        
        if len(pattern['counts'][src_ip]) > pattern['threshold']:
            self.defender.log_alert(f"SYN flood detected from {src_ip}", "CRITICAL", src_ip)
            self.defender.stats['threats_detected'] += 1
            return True
        return False
    
    def detect_brute_force(self, src_ip, timestamp):
        """Detect brute force attacks"""
        pattern = self.attack_patterns['brute_force']
        
        if src_ip not in pattern['counts']:
            pattern['counts'][src_ip] = []
        
        # Clean old entries
        pattern['counts'][src_ip] = [
            t for t in pattern['counts'][src_ip] 
            if timestamp - t < pattern['window']
        ]
        
        pattern['counts'][src_ip].append(timestamp)
        
        if len(pattern['counts'][src_ip]) > pattern['threshold']:
            self.defender.log_alert(f"Brute force attack detected from {src_ip}", "WARNING", src_ip)
            self.defender.stats['threats_detected'] += 1
            return True
        return False

class MalwareDetector:
    """Basic malware and threat detection"""
    
    def __init__(self, defender):
        self.defender = defender
        self.malicious_ips = set()
        self.suspicious_domains = set()
        self.load_threat_intelligence()
    
    def load_threat_intelligence(self):
        """Load known malicious IPs and domains"""
        # In a real implementation, this would load from threat feeds
        self.malicious_ips = {
            '192.168.1.100',  # Example malicious IP
            '10.0.0.50'       # Example malicious IP
        }
        
        self.suspicious_domains = {
            'malicious-site.com',
            'phishing-example.org'
        }
    
    def check_ip_reputation(self, ip_address):
        """Check if IP is known malicious"""
        if ip_address in self.malicious_ips:
            self.defender.log_alert(f"Malicious IP detected: {ip_address}", "CRITICAL", ip_address)
            return True
        return False
    
    def check_domain_reputation(self, domain):
        """Check if domain is suspicious"""
        if domain in self.suspicious_domains:
            self.defender.log_alert(f"Suspicious domain detected: {domain}", "WARNING")
            return True
        return False
    
    def analyze_dns_query(self, packet):
        """Analyze DNS queries for threats"""
        if packet.haslayer(DNS) and packet[DNS].qr == 0:  # DNS query
            dns = packet[DNS]
            if dns.qd:
                domain = dns.qd.qname.decode('utf-8').rstrip('.')
                self.check_domain_reputation(domain)

class SystemMonitor:
    """Monitor system resources and processes"""
    
    def __init__(self, defender):
        self.defender = defender
        self.baseline_cpu = 0
        self.baseline_memory = 0
        self.baseline_network = 0
        self.establish_baseline()
    
    def establish_baseline(self):
        """Establish baseline system metrics"""
        self.baseline_cpu = psutil.cpu_percent(interval=1)
        self.baseline_memory = psutil.virtual_memory().percent
        self.baseline_network = self.get_network_usage()
        self.defender.log_alert(f"Baseline established - CPU: {self.baseline_cpu}%, Memory: {self.baseline_memory}%")
    
    def get_network_usage(self):
        """Get current network usage"""
        net_io = psutil.net_io_counters()
        return net_io.bytes_sent + net_io.bytes_recv
    
    def check_anomalies(self):
        """Check for system anomalies"""
        current_cpu = psutil.cpu_percent(interval=1)
        current_memory = psutil.virtual_memory().percent
        current_network = self.get_network_usage()
        
        # Check for high CPU usage
        if current_cpu > self.baseline_cpu * 2:
            self.defender.log_alert(f"High CPU usage detected: {current_cpu}%", "WARNING")
        
        # Check for high memory usage
        if current_memory > self.baseline_memory * 1.5:
            self.defender.log_alert(f"High memory usage detected: {current_memory}%", "WARNING")
        
        # Check for unusual network activity
        if current_network > self.baseline_network * 3:
            self.defender.log_alert("Unusual network activity detected", "WARNING")
    
    def check_suspicious_processes(self):
        """Check for suspicious running processes"""
        suspicious_keywords = ['nc', 'netcat', 'nmap', 'masscan', 'zmap']
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                proc_info = proc.info
                if proc_info['name'] and any(keyword in proc_info['name'].lower() for keyword in suspicious_keywords):
                    self.defender.log_alert(f"Suspicious process detected: {proc_info['name']} (PID: {proc_info['pid']})", "WARNING")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

class SecurityReporter:
    """Generate security reports and statistics"""
    
    def __init__(self, defender):
        self.defender = defender
    
    def generate_report(self):
        """Generate comprehensive security report"""
        uptime = datetime.now() - self.defender.stats['start_time']
        
        report = {
            'report_time': datetime.now().isoformat(),
            'uptime_seconds': uptime.total_seconds(),
            'statistics': self.defender.stats,
            'alerts': self.defender.alerts[-50:],  # Last 50 alerts
            'blocked_ips': list(self.defender.blocked_ips),
            'threat_level': self.calculate_threat_level()
        }
        
        return report
    
    def calculate_threat_level(self):
        """Calculate current threat level"""
        recent_alerts = [alert for alert in self.defender.alerts 
                        if datetime.fromisoformat(alert['timestamp']) > datetime.now() - timedelta(hours=1)]
        
        critical_count = len([alert for alert in recent_alerts if alert['severity'] == 'CRITICAL'])
        warning_count = len([alert for alert in recent_alerts if alert['severity'] == 'WARNING'])
        
        if critical_count > 5:
            return "HIGH"
        elif critical_count > 2 or warning_count > 10:
            return "MEDIUM"
        elif warning_count > 5:
            return "LOW"
        else:
            return "NORMAL"
    
    def save_report(self, filename="security_report.json"):
        """Save security report to file"""
        report = self.generate_report()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        self.defender.log_alert(f"Security report saved to {filename}")

def main():
    """Main defensive security monitoring"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Defensive Security Tools")
    parser.add_argument("-i", "--interface", default="eth0", help="Network interface to monitor")
    parser.add_argument("-r", "--report", action="store_true", help="Generate security report")
    parser.add_argument("-m", "--monitor", action="store_true", help="Start monitoring mode")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Initialize defensive system
    defender = NetworkDefender()
    firewall = FirewallManager(defender)
    ids = IntrusionDetectionSystem(defender)
    malware_detector = MalwareDetector(defender)
    system_monitor = SystemMonitor(defender)
    reporter = SecurityReporter(defender)
    
    defender.log_alert("Defensive Security System Started")
    defender.log_alert("WARNING: This is for educational purposes only!")
    
    if args.monitor:
        defender.monitoring = True
        defender.log_alert(f"Starting monitoring on interface {args.interface}")
        
        def packet_handler(packet):
            if defender.monitoring:
                # Check for malicious IPs
                if packet.haslayer(IP):
                    src_ip = packet[IP].src
                    if malware_detector.check_ip_reputation(src_ip):
                        firewall.block_ip(src_ip, "Known malicious IP")
                
                # Analyze for attacks
                ids.analyze_packet(packet)
                
                # Analyze DNS queries
                malware_detector.analyze_dns_query(packet)
        
        def system_monitor_loop():
            while defender.monitoring:
                system_monitor.check_anomalies()
                system_monitor.check_suspicious_processes()
                time.sleep(30)  # Check every 30 seconds
        
        # Start system monitoring in background
        monitor_thread = threading.Thread(target=system_monitor_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        try:
            sniff(iface=args.interface, prn=packet_handler)
        except KeyboardInterrupt:
            defender.monitoring = False
            defender.log_alert("Monitoring stopped by user")
        except Exception as e:
            defender.log_alert(f"Monitoring error: {str(e)}", "ERROR")
    
    if args.report:
        reporter.save_report()
        report = reporter.generate_report()
        print("\n" + "="*50)
        print("SECURITY REPORT")
        print("="*50)
        print(f"Threat Level: {report['threat_level']}")
        print(f"Packets Analyzed: {report['statistics']['packets_analyzed']}")
        print(f"Threats Detected: {report['statistics']['threats_detected']}")
        print(f"IPs Blocked: {report['statistics']['ips_blocked']}")
        print(f"Recent Alerts: {len(report['alerts'])}")
        print("="*50)

if __name__ == "__main__":
    main()