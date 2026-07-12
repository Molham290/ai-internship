import gradio as gr
import json
import ollama

MAX_QUESTIONS = 10

def generate_quiz(num_questions, topic):
    if not topic.strip():
        return [gr.update(visible=False)] * MAX_QUESTIONS + [None] * MAX_QUESTIONS + ["Please enter a topic."]

    prompt = f"""You are a cybersecurity expert. Create a Security+ certification quiz with exactly {num_questions} multiple-choice questions about '{topic}'.
Respond ONLY with a valid JSON array. Do not include markdown formatting like ```json.
The JSON format MUST be exactly:
[
    {{
        "question": "The question text?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_answer": "Option A",
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
                updates.append(gr.update(
                    visible=True, 
                    choices=q.get("options", []), 
                    label=f"Q{i+1}: {q.get('question', '')}", 
                    value=None
                ))
                updates.append(q)
            else:
                updates.append(gr.update(visible=False))
                updates.append(None)
                
        status = f"✅ Generated {len(quiz_data)} questions about '{topic}'. Select your answers and click Submit!"
        return updates + [status]

    except json.JSONDecodeError:
        err_msg = f"❌ Error: Llama3 did not return valid JSON. Please try again.\n\nRaw response:\n{raw_text}"
        return [gr.update(visible=False)] * MAX_QUESTIONS + [None] * MAX_QUESTIONS + [err_msg]
    except Exception as e:
        err_msg = f"❌ Error connecting to Ollama: {str(e)}\n\nPlease ensure Ollama is running locally and the 'llama3' model is pulled (`ollama run llama3`)."
        return [gr.update(visible=False)] * MAX_QUESTIONS + [None] * MAX_QUESTIONS + [err_msg]

def grade_quiz(*args):
    radios = args[:MAX_QUESTIONS]
    states = args[MAX_QUESTIONS:]
    
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
        return "No quiz generated yet."
        
    final_score = f"# 🎯 Final Score: {score} / {total}\n\n---\n\n" + "\n---\n".join(results_md)
    return final_score

# Gradio Interface
with gr.Blocks(theme=gr.themes.Soft(), title="Security+ Quick Quiz") as demo:
    gr.Markdown(
        """
        # 🛡️ Security+ Quick Quiz Generator
        Generate custom multiple-choice questions for the CompTIA Security+ exam using local AI (Llama3).
        """
    )
    
    with gr.Row():
        with gr.Column(scale=2):
            topic_input = gr.Textbox(
                label="Quiz Topic", 
                placeholder="e.g., Cryptography, Network Firewalls, Malware types...",
                lines=1
            )
        with gr.Column(scale=1):
            num_questions_input = gr.Slider(
                minimum=1, maximum=10, step=1, value=5, 
                label="Number of Questions"
            )
            
    generate_btn = gr.Button("🚀 Generate Quiz", variant="primary")
    status_output = gr.Markdown()
    
    # Dynamically create radio buttons and state holders (hidden by default)
    radio_components = []
    state_components = []
    
    with gr.Column() as quiz_container:
        for i in range(MAX_QUESTIONS):
            r = gr.Radio(visible=False)
            s = gr.State()
            radio_components.append(r)
            state_components.append(s)
            
    submit_btn = gr.Button("✅ Submit Answers", variant="secondary")
    results_output = gr.Markdown()
    
    # Wire up Generation
    gen_outputs = []
    for i in range(MAX_QUESTIONS):
        gen_outputs.append(radio_components[i])
        gen_outputs.append(state_components[i])
    gen_outputs.append(status_output)
    
    generate_btn.click(
        fn=generate_quiz,
        inputs=[num_questions_input, topic_input],
        outputs=gen_outputs
    )
    
    # Wire up Grading
    submit_btn.click(
        fn=grade_quiz,
        inputs=radio_components + state_components,
        outputs=results_output
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)