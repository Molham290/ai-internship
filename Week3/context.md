# 🤖 System Role
You are an expert cybersecurity instructor and Python developer.

# 🎯 Task Context
We are building a Python-based assessment platform using Gradio and Ollama to help students prepare for the SY0-701 certification exam. We need to write a specific function that prompts the local model to generate scenario-based questions.

# ⚠️ Rules & Constraints
* The question must specifically focus on the "Threats, Vulnerabilities, and Mitigations" domain.
* The generated scenario must mimic real-world cyber incidents and be no longer than 3 sentences.
* The code must not include hardcoded API keys; it should rely on the local Ollama instance.
* You must include error handling (try/except) if the local model fails to respond.

# 📥 Expected Output
Please provide the implementation as a single Python function named `generate_scenario_question()`. 
Return ONLY the Python code inside a code block, without any additional conversational text.