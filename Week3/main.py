import re
import json
from collections import Counter

def parse_ssh_bruteforce(log_lines, threshold=3):
    """
    Parses SSH log lines and detects IPs exceeding the failed password threshold.
    """
    # Regular expression to extract IP addresses from failed SSH login attempts
    failed_login_pattern = re.compile(r"Failed password for .* from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
    
    failed_ips = []
    
    for line in log_lines:
        match = failed_login_pattern.search(line)
        if match:
            failed_ips.append(match.group(1))
            
    # Count occurrences per IP
    ip_counts = Counter(failed_ips)
    
    # Filter IPs exceeding the threshold
    flagged = {ip: count for ip, count in ip_counts.items() if count >= threshold}
    
    return {
        "flagged_ips": flagged,
        "status": "SUCCESS"
    }

# ==========================================
# 🧪 Test Execution (Validation)
# ==========================================
if __name__ == "__main__":
    # Simulated auth.log entries for testing
    sample_logs = [
        "Jul 22 10:01:02 server sshd[1024]: Failed password for root from 192.168.1.50 port 22 ssh2",
        "Jul 22 10:01:05 server sshd[1025]: Failed password for admin from 192.168.1.50 port 22 ssh2",
        "Jul 22 10:01:09 server sshd[1026]: Failed password for invalid user test from 192.168.1.50 port 22 ssh2",
        "Jul 22 10:01:15 server sshd[1027]: Failed password for root from 192.168.1.50 port 22 ssh2",
        "Jul 22 10:02:01 server sshd[1030]: Accepted password for user1 from 10.0.0.5 port 22 ssh2",
        "Jul 22 10:03:12 server sshd[1040]: Failed password for root from 172.16.0.4 port 22 ssh2"
    ]

    # Execute parser
    result = parse_ssh_bruteforce(sample_logs, threshold=3)
    
    # Output formatted JSON
    print(json.dumps(result, indent=2))