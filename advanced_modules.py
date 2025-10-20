#!/usr/bin/env python3
"""
Advanced Network Security Modules
=================================

Additional advanced modules for the Network Security Education Toolkit.
These modules demonstrate more sophisticated security testing concepts.

IMPORTANT: FOR EDUCATIONAL PURPOSES ONLY
Use only on networks you own or have explicit permission to test.
"""

import socket
import struct
import random
import time
import threading
import hashlib
import itertools
import string
from datetime import datetime

class AdvancedNetworkScanner:
    """Advanced network scanning techniques"""
    
    def __init__(self):
        self.timeout = 2
    
    def syn_scan(self, host, port):
        """
        Simulate SYN scan technique (educational demonstration)
        Note: Actual SYN scanning requires raw sockets and root privileges
        """
        print(f"[INFO] SYN scan simulation for {host}:{port}")
        
        try:
            # Create a socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            # Attempt connection (simulating SYN packet)
            start_time = time.time()
            result = sock.connect_ex((host, port))
            response_time = (time.time() - start_time) * 1000
            
            sock.close()
            
            if result == 0:
                return "open", response_time
            else:
                return "closed", response_time
                
        except Exception as e:
            return "filtered", 0
    
    def udp_scan(self, host, port):
        """UDP port scanning"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            
            # Send UDP packet
            sock.sendto(b"test", (host, port))
            
            try:
                # Try to receive response
                data, addr = sock.recvfrom(1024)
                sock.close()
                return "open"
            except socket.timeout:
                sock.close()
                return "open|filtered"
                
        except Exception as e:
            return "closed"
    
    def os_fingerprinting(self, host):
        """
        Basic OS fingerprinting based on network behavior
        This is a simplified educational version
        """
        print(f"\nPerforming OS fingerprinting on {host}")
        print("-" * 40)
        
        fingerprints = {}
        
        # Test different TCP behaviors
        test_ports = [22, 80, 443, 135, 139]
        
        for port in test_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                
                start_time = time.time()
                result = sock.connect_ex((host, port))
                response_time = time.time() - start_time
                
                if result == 0:
                    fingerprints[port] = {
                        'status': 'open',
                        'response_time': response_time
                    }
                    
                    # Try to get banner
                    try:
                        banner = sock.recv(1024).decode('utf-8', errors='ignore')
                        fingerprints[port]['banner'] = banner[:100]
                    except:
                        pass
                
                sock.close()
                
            except Exception as e:
                fingerprints[port] = {'status': 'filtered', 'error': str(e)}
        
        # Analyze fingerprints
        self.analyze_os_fingerprint(host, fingerprints)
        
        return fingerprints
    
    def analyze_os_fingerprint(self, host, fingerprints):
        """Analyze OS fingerprint results"""
        print(f"\nOS Fingerprint Analysis for {host}:")
        print("=" * 35)
        
        # Look for Windows indicators
        windows_indicators = 0
        linux_indicators = 0
        
        if 135 in fingerprints and fingerprints[135]['status'] == 'open':
            windows_indicators += 2
            print("[+] Port 135 (RPC) open - Windows indicator")
        
        if 139 in fingerprints and fingerprints[139]['status'] == 'open':
            windows_indicators += 1
            print("[+] Port 139 (NetBIOS) open - Windows indicator")
        
        if 22 in fingerprints and fingerprints[22]['status'] == 'open':
            linux_indicators += 2
            print("[+] Port 22 (SSH) open - Unix/Linux indicator")
        
        # Check banners for OS information
        for port, data in fingerprints.items():
            if 'banner' in data:
                banner = data['banner'].lower()
                if 'ubuntu' in banner or 'debian' in banner or 'centos' in banner:
                    linux_indicators += 2
                    print(f"[+] Linux distribution detected in banner (port {port})")
                elif 'windows' in banner or 'microsoft' in banner:
                    windows_indicators += 2
                    print(f"[+] Windows detected in banner (port {port})")
        
        # Make educated guess
        if windows_indicators > linux_indicators:
            print(f"\n[*] Likely OS: Windows (confidence: {windows_indicators}/10)")
        elif linux_indicators > windows_indicators:
            print(f"\n[*] Likely OS: Linux/Unix (confidence: {linux_indicators}/10)")
        else:
            print("\n[*] OS detection inconclusive")

class WebVulnerabilityScanner:
    """Web application vulnerability scanner"""
    
    def __init__(self):
        self.timeout = 5
        self.user_agent = "Educational-Security-Scanner/1.0"
    
    def check_http_methods(self, url):
        """Check allowed HTTP methods"""
        import urllib.request
        import urllib.error
        
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'TRACE', 'PATCH']
        allowed_methods = []
        
        print(f"\nTesting HTTP methods for {url}")
        print("-" * 30)
        
        for method in methods:
            try:
                req = urllib.request.Request(url, method=method)
                req.add_header('User-Agent', self.user_agent)
                
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    if response.getcode() < 400:
                        allowed_methods.append(method)
                        print(f"[+] {method} - Allowed")
                    else:
                        print(f"[-] {method} - Not allowed ({response.getcode()})")
                        
            except urllib.error.HTTPError as e:
                if e.code == 405:  # Method Not Allowed
                    print(f"[-] {method} - Not allowed (405)")
                else:
                    print(f"[-] {method} - Error ({e.code})")
            except Exception as e:
                print(f"[-] {method} - Error: {str(e)[:50]}")
        
        # Check for dangerous methods
        dangerous_methods = ['PUT', 'DELETE', 'TRACE']
        for method in dangerous_methods:
            if method in allowed_methods:
                print(f"[!] WARNING: Dangerous method {method} is allowed!")
        
        return allowed_methods
    
    def check_common_files(self, base_url):
        """Check for common sensitive files"""
        import urllib.request
        import urllib.error
        
        common_files = [
            'robots.txt', 'sitemap.xml', '.htaccess', 'web.config',
            'admin/', 'administrator/', 'login/', 'wp-admin/',
            'phpmyadmin/', 'backup/', 'config/', 'test/',
            '.git/', '.svn/', 'README.md', 'CHANGELOG.md'
        ]
        
        print(f"\nChecking for common files/directories on {base_url}")
        print("-" * 50)
        
        found_files = []
        
        for file_path in common_files:
            url = base_url.rstrip('/') + '/' + file_path
            
            try:
                req = urllib.request.Request(url)
                req.add_header('User-Agent', self.user_agent)
                
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    if response.getcode() == 200:
                        size = len(response.read())
                        found_files.append((file_path, size))
                        print(f"[+] Found: {file_path} ({size} bytes)")
                    
            except urllib.error.HTTPError as e:
                if e.code == 403:
                    print(f"[!] Forbidden: {file_path} (may exist)")
                # Silently ignore 404s
            except Exception:
                pass  # Connection errors, timeouts, etc.
        
        return found_files
    
    def check_sql_injection(self, url):
        """Basic SQL injection detection (educational)"""
        import urllib.request
        import urllib.parse
        
        print(f"\nTesting for SQL injection vulnerabilities")
        print("(This is a basic educational demonstration)")
        print("-" * 45)
        
        # Common SQL injection payloads
        payloads = [
            "'", "''", "1'", "1' OR '1'='1", "1' OR '1'='1' --",
            "1' OR '1'='1' /*", "'; DROP TABLE users; --",
            "1 OR 1=1", "1 OR 1=1 --", "admin'--", "admin' #"
        ]
        
        # Test GET parameters
        if '?' in url:
            base_url, query_string = url.split('?', 1)
            params = urllib.parse.parse_qs(query_string)
            
            for param_name in params:
                print(f"\nTesting parameter: {param_name}")
                
                for payload in payloads[:3]:  # Test only first 3 for demo
                    test_params = params.copy()
                    test_params[param_name] = [payload]
                    
                    test_query = urllib.parse.urlencode(test_params, doseq=True)
                    test_url = f"{base_url}?{test_query}"
                    
                    try:
                        req = urllib.request.Request(test_url)
                        req.add_header('User-Agent', self.user_agent)
                        
                        with urllib.request.urlopen(req, timeout=self.timeout) as response:
                            content = response.read().decode('utf-8', errors='ignore')
                            
                            # Look for SQL error messages
                            sql_errors = [
                                'sql syntax', 'mysql_fetch', 'ora-', 'postgresql',
                                'sqlite_', 'sqlstate', 'syntax error'
                            ]
                            
                            for error in sql_errors:
                                if error in content.lower():
                                    print(f"[!] Potential SQL injection: {payload}")
                                    print(f"    Error pattern found: {error}")
                                    break
                    
                    except Exception:
                        pass  # Ignore connection errors
        
        print("\n[*] SQL injection test completed")
        print("    Note: This is a basic test. Use specialized tools for thorough testing.")

class CryptographyTester:
    """Cryptography and hash testing utilities"""
    
    def __init__(self):
        self.common_hashes = {
            32: 'MD5',
            40: 'SHA1',
            64: 'SHA256',
            128: 'SHA512'
        }
    
    def identify_hash(self, hash_string):
        """Identify hash type based on length and format"""
        hash_clean = hash_string.strip().lower()
        length = len(hash_clean)
        
        # Check if it's hexadecimal
        if all(c in '0123456789abcdef' for c in hash_clean):
            hash_type = self.common_hashes.get(length, 'Unknown')
            return hash_type, length
        
        return 'Unknown format', length
    
    def hash_cracker(self, target_hash, wordlist, hash_type='md5'):
        """Simple hash cracking demonstration"""
        print(f"\nAttempting to crack {hash_type.upper()} hash: {target_hash}")
        print("=" * 50)
        
        hash_functions = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512
        }
        
        if hash_type.lower() not in hash_functions:
            print(f"Unsupported hash type: {hash_type}")
            return False
        
        hash_func = hash_functions[hash_type.lower()]
        target_hash = target_hash.lower().strip()
        
        attempts = 0
        for word in wordlist:
            attempts += 1
            word_hash = hash_func(word.encode()).hexdigest()
            
            print(f"Attempt {attempts:4d}: {word:15s} -> {word_hash}")
            
            if word_hash == target_hash:
                print(f"\n[+] Hash cracked!")
                print(f"    Original text: {word}")
                print(f"    Attempts: {attempts}")
                return True
            
            # Add small delay for demonstration
            time.sleep(0.05)
        
        print(f"\n[-] Hash not cracked after {attempts} attempts")
        return False
    
    def generate_rainbow_table(self, charset, max_length, hash_type='md5'):
        """Generate a small rainbow table for demonstration"""
        print(f"\nGenerating rainbow table ({hash_type.upper()}, max length: {max_length})")
        print("=" * 60)
        
        hash_functions = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256
        }
        
        if hash_type.lower() not in hash_functions:
            print(f"Unsupported hash type: {hash_type}")
            return {}
        
        hash_func = hash_functions[hash_type.lower()]
        rainbow_table = {}
        
        total_combinations = 0
        for length in range(1, max_length + 1):
            total_combinations += len(charset) ** length
        
        print(f"Total combinations to generate: {total_combinations}")
        
        if total_combinations > 10000:
            print("Warning: This would generate a very large table!")
            proceed = input("Continue? (y/N): ")
            if proceed.lower() != 'y':
                return {}
        
        generated = 0
        for length in range(1, max_length + 1):
            for combination in itertools.product(charset, repeat=length):
                plaintext = ''.join(combination)
                hash_value = hash_func(plaintext.encode()).hexdigest()
                rainbow_table[hash_value] = plaintext
                
                generated += 1
                if generated % 100 == 0:
                    print(f"Generated {generated}/{total_combinations} entries...")
        
        print(f"\nRainbow table generated: {len(rainbow_table)} entries")
        return rainbow_table

class SocialEngineeringAwareness:
    """Social engineering awareness and education"""
    
    def __init__(self):
        self.phishing_indicators = [
            "Urgent action required",
            "Verify your account",
            "Click here immediately",
            "Your account will be suspended",
            "Congratulations, you've won",
            "Free money/prizes",
            "Act now or lose out",
            "Confidential/Secret information"
        ]
    
    def analyze_phishing_email(self, email_content):
        """Analyze email content for phishing indicators"""
        print("\nPhishing Email Analysis")
        print("=" * 30)
        
        score = 0
        indicators_found = []
        
        email_lower = email_content.lower()
        
        # Check for common phishing phrases
        for indicator in self.phishing_indicators:
            if indicator.lower() in email_lower:
                score += 1
                indicators_found.append(indicator)
        
        # Check for suspicious patterns
        if '@' in email_content and 'http' in email_content:
            # Look for mismatched domains
            import re
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_content)
            if urls:
                print(f"URLs found: {len(urls)}")
                for url in urls[:3]:  # Show first 3 URLs
                    print(f"  - {url}")
        
        # Risk assessment
        if score == 0:
            risk_level = "Low"
        elif score <= 2:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        print(f"\nRisk Level: {risk_level}")
        print(f"Phishing Score: {score}/10")
        
        if indicators_found:
            print("\nPhishing indicators found:")
            for indicator in indicators_found:
                print(f"  - {indicator}")
        
        return risk_level, score, indicators_found
    
    def password_policy_checker(self, password_policy):
        """Check password policy strength"""
        print("\nPassword Policy Analysis")
        print("=" * 30)
        
        score = 0
        recommendations = []
        
        # Check minimum length
        if 'min_length' in password_policy:
            min_len = password_policy['min_length']
            if min_len >= 12:
                score += 2
                print(f"[+] Minimum length: {min_len} (Good)")
            elif min_len >= 8:
                score += 1
                print(f"[+] Minimum length: {min_len} (Acceptable)")
            else:
                print(f"[-] Minimum length: {min_len} (Too short)")
                recommendations.append("Increase minimum length to at least 8 characters")
        
        # Check complexity requirements
        complexity_checks = [
            ('require_uppercase', 'Uppercase letters required'),
            ('require_lowercase', 'Lowercase letters required'),
            ('require_numbers', 'Numbers required'),
            ('require_special', 'Special characters required')
        ]
        
        for check, description in complexity_checks:
            if password_policy.get(check, False):
                score += 1
                print(f"[+] {description}")
            else:
                recommendations.append(f"Require {description.lower()}")
        
        # Check other policies
        if password_policy.get('password_history', 0) > 0:
            score += 1
            print(f"[+] Password history: {password_policy['password_history']}")
        else:
            recommendations.append("Implement password history")
        
        if password_policy.get('max_age_days', 0) > 0:
            age = password_policy['max_age_days']
            if 30 <= age <= 90:
                score += 1
                print(f"[+] Password expiration: {age} days")
            else:
                print(f"[!] Password expiration: {age} days (consider 30-90 days)")
        
        print(f"\nPolicy Strength Score: {score}/8")
        
        if recommendations:
            print("\nRecommendations:")
            for rec in recommendations:
                print(f"  - {rec}")
        
        return score, recommendations

def demo_advanced_modules():
    """Demonstrate the advanced modules"""
    print("Advanced Network Security Modules Demo")
    print("=" * 40)
    
    # Network scanning demo
    print("\n1. Advanced Network Scanning")
    scanner = AdvancedNetworkScanner()
    # scanner.os_fingerprinting("127.0.0.1")  # Uncomment to test
    
    # Cryptography demo
    print("\n2. Cryptography Testing")
    crypto = CryptographyTester()
    
    # Example hash identification
    test_hash = "5d41402abc4b2a76b9719d911017c592"  # MD5 of "hello"
    hash_type, length = crypto.identify_hash(test_hash)
    print(f"Hash: {test_hash}")
    print(f"Identified as: {hash_type} ({length} characters)")
    
    # Social engineering awareness demo
    print("\n3. Social Engineering Awareness")
    se_awareness = SocialEngineeringAwareness()
    
    sample_email = """
    URGENT: Your account will be suspended!
    Click here immediately to verify your account.
    Act now or lose access forever!
    """
    
    risk, score, indicators = se_awareness.analyze_phishing_email(sample_email)
    
    print("\n" + "="*40)
    print("Demo completed!")

if __name__ == "__main__":
    demo_advanced_modules()