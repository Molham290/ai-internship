# 🛡️ Blue Team Log Parser Agent

A lightweight, local AI-assisted security tool designed to parse Linux authentication logs (`auth.log`) and detect potential SSH brute-force attacks in real-time.

## 🎯 Features
* **Automated Log Parsing:** Extracts raw syslog entries and scans for failed authentication attempts.
* **Brute-Force Detection:** Flags IP addresses exceeding a configurable threshold of failed attempts.
* **Structured Output:** Produces clean JSON reports for seamless integration into SOC alert pipelines.
* **Privacy-First:** Designed to run locally with zero external API dependencies or active network requests.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Environment:** Ollama / Local LLM Runner
* **Formatting:** Markdown Spec Standard

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/blue-team-log-parser.git](https://github.com/YOUR_USERNAME/blue-team-log-parser.git)
   cd blue-team-log-parser