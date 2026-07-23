import re
import json
from collections import defaultdict
from datetime import datetime, timedelta

def detect_ssh_brute_force(log_data: str) -> str:
    """
    Parses a Linux auth.log string to detect SSH brute-force attacks.
    Returns a JSON object mapping malicious IPs to their total failed attempts.
    """
    # Error Resilience: Gracefully handle empty or invalid inputs
    if not log_data or not isinstance(log_data, str):
        return "{}"
    
    failed_attempts = defaultdict(list)
    
    # Regex to extract standard syslog timestamps and the IP from a failed SSH login
    pattern = re.compile(
        r'^(?P<month>[A-Z][a-z]{2})\s+(?P<day>\d+)\s+(?P<time>\d{2}:\d{2}:\d{2}).*?Failed password for .*? from (?P<ip>\d+\.\d+\.\d+\.\d+)'
    )
    
    for line in log_data.strip().split('\n'):
        match = pattern.search(line)
        if match:
            month = match.group('month')
            day = match.group('day')
            time_str = match.group('time')
            ip = match.group('ip')
            
            # Use a leap year (e.g., 2024) to handle Feb 29 gracefully if it appears in logs
            date_str = f"2024 {month} {day} {time_str}"
            try:
                # Parse timestamp
                dt = datetime.strptime(date_str, "%Y %b %d %H:%M:%S")
                failed_attempts[ip].append(dt)
            except ValueError:
                # Error Resilience: Skip malformed date lines without crashing
                continue
                
    malicious_ips = {}
    
    for ip, timestamps in failed_attempts.items():
        # Quick filter: only process IPs that have at least 5 total attempts
        if len(timestamps) >= 5:
            timestamps.sort()
            
            # Sliding window check: 5 attempts within a 1-minute window
            is_brute_force = False
            for i in range(len(timestamps) - 4):
                if timestamps[i+4] - timestamps[i] <= timedelta(minutes=1):
                    is_brute_force = True
                    break
                    
            if is_brute_force:
                malicious_ips[ip] = len(timestamps)
                
    # Strict Formatting: Ensure output is a valid JSON object
    return json.dumps(malicious_ips, indent=2)

# ==========================================
# Example Usage:
# ==========================================
if __name__ == "__main__":
    sample_log = """
Jan 14 10:22:30 server sshd[101]: Failed password for root from 192.168.1.50 port 22 ssh2
Jan 14 10:22:35 server sshd[102]: Failed password for admin from 192.168.1.50 port 22 ssh2
Jan 14 10:22:40 server sshd[103]: Failed password for root from 192.168.1.50 port 22 ssh2
Jan 14 10:22:45 server sshd[104]: Failed password for user from 192.168.1.50 port 22 ssh2
Jan 14 10:22:50 server sshd[105]: Failed password for root from 192.168.1.50 port 22 ssh2
Jan 14 10:22:55 server sshd[106]: Failed password for root from 192.168.1.50 port 22 ssh2
Jan 14 10:30:00 server sshd[200]: Failed password for root from 203.0.113.12 port 22 ssh2
"""
    print(detect_ssh_brute_force(sample_log))