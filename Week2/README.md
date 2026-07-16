# 🛡️ AI-Powered Security+ Quiz Agent 🎯

An intelligent, locally-hosted quiz generator designed specifically for CompTIA Security+ (SY0-701) exam preparation. This tool leverages the power of local LLMs to generate highly accurate, dynamic multiple-choice questions, ensuring complete data privacy and an endless supply of practice material.

## ✨ Features

*   **🧠 Local AI Generation:** Powered by Ollama and the `llama3` model, meaning your data never leaves your machine.
*   **🎯 Dynamic Topic Selection:** Focus your study sessions by generating questions based on specific SY0-701 exam domains.
*   **💻 Interactive UI:** Built with Python's Gradio framework, featuring a modern, dark-mode cybersecurity aesthetic with intuitive question cards.
*   **⚡ Instant Feedback:** Get immediate grading and detailed explanations for every answer to accelerate your learning.

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:
*   **Python 3.x**
*   **Ollama** (for running the local `llama3` model)

## 🚀 Installation & Setup

Follow these step-by-step instructions to get the quiz agent running on your local machine:

**1. Clone the repository:**
```bash
git clone https://github.com/yourusername/security-plus-quiz-agent.git
cd security-plus-quiz-agent
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Pull the local AI model:**
```bash
ollama pull llama3
```

**4. Run the application:**
```bash
python QuizAgent.py
```

Once running, open the provided local URL in your web browser to start practicing!
