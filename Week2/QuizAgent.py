import os
import json
import time
import gradio as gr
import ollama

MAX_QUESTIONS = 10

def generate_quiz(num_questions, topic, difficulty):
    if not topic.strip():
        return [gr.update(visible=False), gr.update(), None] * MAX_QUESTIONS + ["Please enter a topic.", gr.update(visible=False), None]

    prompt = f"You are a cybersecurity expert. Create a Security+ certification quiz with exactly {num_questions} multiple-choice questions about '{topic}'."
    
    if difficulty == "Hard":
        prompt += " Make the questions highly technical and difficult."
    elif difficulty == "Scenario-Based":
        prompt += " Write the questions as real-world cybersecurity incident scenarios."
        
    prompt += """
Respond ONLY with a valid JSON array. Do not include markdown formatting like ```json.
The JSON format MUST be exactly:
[
    {{
        "question": "The question text?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_answer": "The exact string text of the correct option, do NOT write 'Option A' or 'Option B'.",
        "explanation": "Explanation of why this is the correct answer."
    }}
]"""

    try:
        # Using the ollama Python library as requested
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        
        raw_text = response['message']['content'].strip()
        
        # Clean up potential markdown formatting from the model
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        quiz_data = json.loads(raw_text.strip())
        
        # Ensure we don't exceed MAX_QUESTIONS
        quiz_data = quiz_data[:MAX_QUESTIONS]
        
        updates = []
        for i in range(MAX_QUESTIONS):
            if i < len(quiz_data):
                q = quiz_data[i]
                updates.append(gr.update(visible=True)) # Group
                updates.append(gr.update(
                    choices=q.get("options", []), 
                    label=f"Q{i+1}: {q.get('question', '')}", 
                    value=None
                )) # Radio
                updates.append(q) # State
            else:
                updates.append(gr.update(visible=False))
                updates.append(gr.update())
                updates.append(None)
                
        status = f"✅ Generated {len(quiz_data)} questions about '{topic}'. Select your answers and click Submit!"
        return updates + [status, gr.update(visible=True), time.time()]

    except json.JSONDecodeError:
        err_msg = f"❌ Error: Llama3 did not return valid JSON. Please try again.\n\nRaw response:\n{raw_text}"
        return [gr.update(visible=False), gr.update(), None] * MAX_QUESTIONS + [err_msg, gr.update(visible=False), None]
    except ollama.ResponseError as e:
        err_msg = f"❌ Ollama Model Error: {e.error}\n\nPlease ensure the 'llama3' model is pulled by running `ollama pull llama3` in your terminal."
        return [gr.update(visible=False), gr.update(), None] * MAX_QUESTIONS + [err_msg, gr.update(visible=False), None]
    except Exception as e:
        err_msg = f"❌ Connection Error: Could not connect to the local Ollama service.\n\nDetails: {str(e)}\n\nSteps to fix:\n1. Ensure Ollama is installed and running locally.\n2. Verify the Ollama server is active (default URL: http://localhost:11434).\n3. Try running `ollama run llama3` in your terminal."
        return [gr.update(visible=False), gr.update(), None] * MAX_QUESTIONS + [err_msg, gr.update(visible=False), None]

def grade_quiz(*args):
    radios = args[:MAX_QUESTIONS]
    states = args[MAX_QUESTIONS:2*MAX_QUESTIONS]
    start_time = args[-1]
    
    score = 0
    total = 0
    results_md = []
    
    for user_answer, q_data in zip(radios, states):
        if q_data is not None:
            total += 1
            correct_answer = q_data.get("correct_answer", "")
            explanation = q_data.get("explanation", "No explanation provided.")
            
            if user_answer == correct_answer:
                score += 1
                results_md.append(f"### Q{total}: ✅ Correct!\n**Your Answer:** {user_answer}\n\n*Explanation:* {explanation}\n")
            else:
                user_answer_display = user_answer if user_answer else "No answer provided"
                results_md.append(f"### Q{total}: ❌ Incorrect.\n**Your Answer:** {user_answer_display}  \n**Correct Answer:** {correct_answer}\n\n*Explanation:* {explanation}\n")
                
    if total == 0:
        return "No quiz generated yet.", gr.update(visible=False)
        
    time_str = ""
    if start_time:
        elapsed = time.time() - start_time
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)
        time_str = f"⏱️ **Time Taken:** {mins}m {secs}s\n\n"
        
    final_score = f"# 🎯 Final Score: {score} / {total}\n\n{time_str}---\n\n" + "\n---\n".join(results_md)
    
    with open("quiz_results.md", "w", encoding="utf-8") as f:
        f.write(final_score)
        
    return final_score, gr.update(value="quiz_results.md", visible=True)

# Gradio Interface
custom_css = """
.container { max-width: 1000px; margin: auto; padding-top: 3rem; padding-bottom: 3rem; }
.header-text { text-align: center; margin-bottom: 3rem; }
.header-text h1 { 
    color: #06b6d4; 
    font-weight: 900; 
    font-size: 2.8rem; 
    margin-bottom: 0.5rem; 
    text-transform: uppercase; 
    letter-spacing: 0.05em;
    text-shadow: 0 0 15px rgba(6, 182, 212, 0.5);
}
.header-text p { color: #94a3b8; font-size: 1.15rem; letter-spacing: 0.02em; }
.panel-custom { padding: 2rem !important; border-radius: 1rem !important; }

/* Question Card Styles */
.question-card {
    background-color: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    padding: 24px !important;
    margin-bottom: 24px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
}

.question-radio {
    border: none !important;
    background: transparent !important;
}

.question-radio > label > span {
    font-size: 1.35rem !important;
    font-weight: 800 !important;
    color: #e2e8f0 !important;
    margin-bottom: 16px !important;
    display: block !important;
    line-height: 1.4 !important;
}

.question-radio .wrap {
    display: flex !important;
    flex-direction: column !important;
    gap: 12px !important;
}

.question-radio .wrap label {
    background: #0f172a !important;
    padding: 14px 18px !important;
    border-radius: 8px !important;
    border: 1px solid #334155 !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

.question-radio .wrap label:hover {
    border-color: #06b6d4 !important;
    background: #164e63 !important;
}

/* Premium Button Styles */
button.premium-btn {
    background: #0891b2 !important; /* solid cybersecurity cyan */
    border: none !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    font-weight: bold !important;
    font-size: 1.15rem !important;
    box-shadow: 0 0 15px rgba(8, 145, 178, 0.4) !important;
    transition: all 0.3s ease !important;
}

button.premium-btn:hover {
    background: #06b6d4 !important; /* brighter glow */
    transform: scale(1.02) !important;
    box-shadow: 0 0 25px rgba(6, 182, 212, 0.7) !important;
    filter: brightness(1.1) !important;
}
"""

with gr.Blocks(theme=gr.themes.Monochrome(primary_hue="cyan", neutral_hue="slate"), title="Security+ Quiz Agent", css=custom_css) as demo:
    with gr.Column(elem_classes="container"):
        gr.HTML(
            """
            <div class="header-text">
                <h1>🛡️ Security+ Quiz Agent</h1>
                <p>Premium AI-powered assessment generation for CompTIA Security+ SY0-701</p>
            </div>
            """
        )
        
        with gr.Row():
            with gr.Column(scale=1, variant="panel", elem_classes="panel-custom"):
                gr.Markdown("### ⚙️ Configuration")
                topic_input = gr.Dropdown(
                    choices=[
                        "General Security Concepts",
                        "Threats, Vulnerabilities, and Mitigations",
                        "Security Architecture",
                        "Security Operations",
                        "Security Program Management and Oversight"
                    ],
                    value="General Security Concepts",
                    label="SY0-701 Domain",
                    interactive=True
                )
                difficulty_input = gr.Dropdown(
                    choices=["Standard", "Hard", "Scenario-Based"],
                    value="Standard",
                    label="Difficulty Level",
                    interactive=True
                )
                num_questions_input = gr.Slider(
                    minimum=1, maximum=10, step=1, value=5, 
                    label="Number of Questions"
                )
                generate_btn = gr.Button("🚀 Generate Assessment", variant="primary", size="lg", elem_classes="premium-btn")
                status_output = gr.Markdown()
                
            with gr.Column(scale=2, variant="panel", elem_classes="panel-custom"):
                gr.Markdown("### 📝 Assessment Area")
                
                # Dynamically create radio buttons and state holders (hidden by default)
                group_components = []
                radio_components = []
                state_components = []
                
                for i in range(MAX_QUESTIONS):
                    with gr.Group(visible=False, elem_classes="question-card") as g:
                        r = gr.Radio(visible=True, label="", elem_classes="question-radio")
                    s = gr.State()
                    group_components.append(g)
                    radio_components.append(r)
                    state_components.append(s)
                    
                submit_btn = gr.Button("✅ Submit Answers", variant="primary", size="lg", visible=False, elem_classes="premium-btn")
                results_output = gr.Markdown()
                download_btn = gr.DownloadButton("📥 Download Results", visible=False, elem_classes="premium-btn")
                start_time_state = gr.State()
    
    # Wire up Generation
    gen_outputs = []
    for i in range(MAX_QUESTIONS):
        gen_outputs.append(group_components[i])
        gen_outputs.append(radio_components[i])
        gen_outputs.append(state_components[i])
    gen_outputs.append(status_output)
    gen_outputs.append(submit_btn)
    gen_outputs.append(start_time_state)
    
    generate_btn.click(
        fn=generate_quiz,
        inputs=[num_questions_input, topic_input, difficulty_input],
        outputs=gen_outputs
    )
    
    # Wire up Grading
    submit_btn.click(
        fn=grade_quiz,
        inputs=radio_components + state_components + [start_time_state],
        outputs=[results_output, download_btn]
    )

if __name__ == "__main__":
    demo.launch()


