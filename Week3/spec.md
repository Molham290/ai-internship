# 🎯 Objectives
Develop a Python function for the Blue Team AI Agent to parse Linux SSH authentication logs (`auth.log`) and detect potential SSH brute-force attacks accurately.

# 📥 Inputs
* A raw text string representing the contents of a standard Linux `auth.log` file.
* Each line in the log contains standard syslog formatting (timestamp, hostname, service, and message).

# ⚠️ Constraints
* **No Third-Party Libraries:** The script must use only built-in Python libraries (e.g., `re`, `datetime`, `collections`).
* **OpSec Strict Rule:** Do NOT perform any active network requests (e.g., no WhoIs lookups, no pinging the suspicious IPs) to avoid tipping off the attacker.
* **Detection Threshold:** A brute-force attack is defined strictly as 5 or more failed login attempts from the exact same IP address within a 1-minute window.

# 📤 Expected Outputs
Return a JSON object where the keys are the malicious IP addresses and the values are the total number of failed attempts detected. 

Example:
{
  "192.168.1.50": 7,
  "203.0.113.12": 15
}
