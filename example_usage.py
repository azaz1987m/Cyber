#!/usr/bin/env python3
"""
Example Usage of Network Security Toolkit
========================================

This file demonstrates how to use the network security toolkit
for educational and authorized testing purposes.

Author: Security Researcher
License: Educational Use Only
"""

from network_security_toolkit import NetworkSecurityToolkit, PortScanner, VulnerabilityScanner
from advanced_network_tools import ARPSpoofing, PacketSniffer, NetworkStressTester
import time

def example_port_scanning():
    """Example of port scanning"""
    print("=" * 50)
    print("EXAMPLE: Port Scanning")
    print("=" * 50)
    
    # Initialize toolkit
    toolkit = NetworkSecurityToolkit()
    toolkit.verbose = True
    
    # Create port scanner
    scanner = PortScanner(toolkit)
    
    # Example: Scan common ports on localhost
    target = "127.0.0.1"  # Always use localhost for examples
    ports = [22, 80, 443, 8080, 3306, 5432]  # Common ports
    
    print(f"Scanning {target} for ports: {ports}")
    open_ports = scanner.tcp_scan(target, ports, max_threads=10)
    
    print(f"Open ports found: {open_ports}")
    return open_ports

def example_vulnerability_scanning():
    """Example of vulnerability scanning"""
    print("\n" + "=" * 50)
    print("EXAMPLE: Vulnerability Scanning")
    print("=" * 50)
    
    toolkit = NetworkSecurityToolkit()
    vuln_scanner = VulnerabilityScanner(toolkit)
    
    # Example: Check localhost for vulnerabilities
    target = "127.0.0.1"
    
    print(f"Checking vulnerabilities on {target}")
    http_vulns = vuln_scanner.check_http_vulnerabilities(target, 80)
    ssh_vulns = vuln_scanner.check_ssh_vulnerabilities(target, 22)
    
    all_vulns = http_vulns + ssh_vulns
    if all_vulns:
        print("Vulnerabilities found:")
        for vuln in all_vulns:
            print(f"  - {vuln['type']}: {vuln['details']} (Severity: {vuln['severity']})")
    else:
        print("No vulnerabilities found")
    
    return all_vulns

def example_packet_sniffing():
    """Example of packet sniffing"""
    print("\n" + "=" * 50)
    print("EXAMPLE: Packet Sniffing")
    print("=" * 50)
    
    toolkit = NetworkSecurityToolkit()
    sniffer = PacketSniffer(toolkit)
    
    print("Starting packet capture for 10 seconds...")
    print("(This will capture packets on the default interface)")
    
    # Note: This requires root privileges and may not work in all environments
    try:
        # Start sniffing with a count limit for safety
        sniffer.start_sniffing(count=50)
        
        print(f"Captured {len(sniffer.captured_packets)} packets")
        
        # Show sample packets
        for i, packet in enumerate(sniffer.captured_packets[:5]):
            print(f"Packet {i+1}: {packet['protocol']} from {packet['source']} to {packet['destination']}")
        
        # Save results
        sniffer.save_captured_packets("example_captured_packets.json")
        
    except Exception as e:
        print(f"Packet sniffing failed (may require root privileges): {e}")

def example_arp_spoofing():
    """Example of ARP spoofing (demonstration only)"""
    print("\n" + "=" * 50)
    print("EXAMPLE: ARP Spoofing (Demonstration Only)")
    print("=" * 50)
    
    print("⚠️  WARNING: ARP spoofing is for demonstration only!")
    print("This example shows how the tool works but does not execute it.")
    print("Only use ARP spoofing on systems you own or have explicit permission to test.")
    
    toolkit = NetworkSecurityToolkit()
    arp_spoofer = ARPSpoofing(toolkit)
    
    # Example configuration (not executed)
    target_ip = "192.168.1.100"  # Example target
    gateway_ip = "192.168.1.1"   # Example gateway
    
    print(f"ARP Spoofing would target: {target_ip}")
    print(f"Gateway: {gateway_ip}")
    print("To actually perform ARP spoofing:")
    print("  arp_spoofer.spoof(target_ip, gateway_ip)")
    print("  # ... perform testing ...")
    print("  arp_spoofer.stop_spoofing()")

def example_stress_testing():
    """Example of network stress testing"""
    print("\n" + "=" * 50)
    print("EXAMPLE: Network Stress Testing")
    print("=" * 50)
    
    print("⚠️  WARNING: Stress testing is for demonstration only!")
    print("Only use on systems you own or have explicit permission to test.")
    
    toolkit = NetworkSecurityToolkit()
    stress_tester = NetworkStressTester(toolkit)
    
    # Example configuration (not executed)
    target_ip = "127.0.0.1"  # Use localhost for safety
    target_port = 80
    
    print(f"Stress testing would target: {target_ip}:{target_port}")
    print("To perform stress testing:")
    print("  stress_tester.syn_flood(target_ip, target_port, count=100)")
    print("  stress_tester.icmp_flood(target_ip, count=100)")

def example_cryptography_tools():
    """Example of cryptography tools"""
    print("\n" + "=" * 50)
    print("EXAMPLE: Cryptography Tools")
    print("=" * 50)
    
    from advanced_network_tools import CryptographyTools
    
    toolkit = NetworkSecurityToolkit()
    crypto_tools = CryptographyTools(toolkit)
    
    # Example: Generate hashes
    text = "Hello, World!"
    print(f"Text: {text}")
    
    algorithms = ["md5", "sha1", "sha256", "sha512"]
    for algo in algorithms:
        hash_value = crypto_tools.generate_hash(text, algo)
        print(f"{algo.upper()}: {hash_value}")
    
    # Example: Brute force (with small wordlist)
    print("\nBrute force example (educational only):")
    target_hash = crypto_tools.generate_hash("password", "md5")
    print(f"Target hash: {target_hash}")
    
    # Create a small wordlist for demonstration
    wordlist = ["123456", "password", "admin", "test", "hello"]
    
    print("Trying common passwords...")
    result = crypto_tools.brute_force_hash(target_hash, "wordlist.txt", "md5")
    if result:
        print(f"Password found: {result}")
    else:
        print("Password not found in wordlist")

def create_sample_wordlist():
    """Create a sample wordlist for demonstration"""
    wordlist_content = """123456
password
admin
test
hello
world
user
guest
root
toor
"""
    
    with open("wordlist.txt", "w") as f:
        f.write(wordlist_content)
    
    print("Created sample wordlist: wordlist.txt")

def main():
    """Main example function"""
    print("NETWORK SECURITY TOOLKIT - EXAMPLE USAGE")
    print("=" * 60)
    print("This demonstrates various tools in the toolkit.")
    print("All examples use localhost (127.0.0.1) for safety.")
    print("=" * 60)
    
    # Create sample wordlist
    create_sample_wordlist()
    
    try:
        # Run examples
        example_port_scanning()
        example_vulnerability_scanning()
        example_packet_sniffing()
        example_arp_spoofing()
        example_stress_testing()
        example_cryptography_tools()
        
        print("\n" + "=" * 60)
        print("EXAMPLES COMPLETED")
        print("=" * 60)
        print("Remember:")
        print("- Always get permission before testing")
        print("- Use only on systems you own")
        print("- Follow ethical guidelines")
        print("- Learn responsibly")
        
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\nError during examples: {e}")
    finally:
        # Cleanup
        try:
            import os
            if os.path.exists("wordlist.txt"):
                os.remove("wordlist.txt")
                print("Cleaned up sample files.")
        except:
            pass

if __name__ == "__main__":
    main()