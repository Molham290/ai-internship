# Day 2: Prompting Fundamentals - Task Submission

**Scenario:** Sending an email to a student regarding a course schedule adjustment due to a time conflict.
**LLM Used:** Llama 3 (via Ollama local API)

---

### 1. Basic Prompt
**Prompt:** "Write an email to a student about their course"
**Output Summary:** The model hallucinated context. It wrote about midterm progress, upcoming quiz dates, and group projects, which had nothing to do with registration or schedule adjustments.

### 2. Improved Prompt
**Prompt:** "Write an email to a student telling them their course registration was adjusted due to a time conflict."
**Output Summary:** Better context. The model correctly addressed the time conflict and provided placeholders for [Original Course] and [New Course], but the structure was still a bit generic.

### 3. Detailed Prompt (RTCF applied)
**Prompt:** "You are an academic advisor at the Deanship of E-learning. Write a formal email to a student informing them that their course schedule was updated to fix a time conflict. Ask them to check the Student Information System for the new schedule."
**Output Summary:** Highly professional. The model adopted the correct persona, provided clear step-by-step instructions on how to access the Student Information System (SIS), and used the appropriate sign-off.

### 4. Creative Prompt
**Prompt:** "Write an engaging and reassuring email to a student who might be stressed about their course schedule changing suddenly. Assure them the Deanship of E-learning has resolved the conflict and their academic journey is safely on track."
**Output Summary:** Very empathetic and supportive tone ("seamless learning experience", "safely on track"). However, it was too long and overly emotional for a standard administrative notification.

### 5. With Clear Constraints Prompt
**Prompt:** "You are a system administrator at King Abdulaziz University. Write a formal email to a student regarding a course schedule adjustment. Constraints: Do not exceed 80 words. Use 2 bullet points for the next steps. End the email with a professional sign-off from the Deanship of E-learning."
**Output Summary:** Extremely concise and direct. The model perfectly respected the word limit, used exact bullet points for the next steps (Log in to SIS / Contact us), and applied the specific signature.

---

### 🏆 Comparison

**Which prompt gave the best result?**
Prompt 5 (With clear constraints) was the most effective for this specific scenario, closely followed by Prompt 3 (Detailed).

**Why?**
In an administrative environment like managing university course registrations, efficiency and clarity are the top priorities. 
* The **Basic** prompt proved that without direction, LLMs will blindly guess the context and hallucinate irrelevant details. 
* The **Creative** prompt generated a wall of text that students would likely skip reading.
* **Prompt 5** was the best because applying strict constraints (word count limit + bullet points) forced the model to cut the "fluff." It delivered a highly scannable, direct, and professional system notification that perfectly matches real-world operations.,