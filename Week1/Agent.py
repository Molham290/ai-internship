import ollama
import json
from fpdf import FPDF


system_prompt = """
You are an expert AI assistant specialized in summarizing text.
You MUST return your response STRICTLY as a JSON object. Do not include any conversational text.
The JSON object must contain exactly two keys:
1. "summary": The summarized version of the text.
2. "format": The requested output format, which must be either "pdf" or "txt". Extract this from the user's prompt.

Example of expected output:
{"summary": "This is the summarized text.", "format": "pdf"}
"""

print("=== AI Summarizer & File Generator ===")

user_text = input("Enter the text you want to summarize:\n> ")
user_format = input("How do you want the output? (e.g., 'Make it a PDF' or 'Save as TXT'):\n> ")

combined_prompt = f"Text to summarize: {user_text}\nRequested format: {user_format}"

print("\nThinking and generating the summary... Please wait.")


response = ollama.chat(
    model='llama3',
    messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': combined_prompt}
    ],
    format='json' 
)


try:
   
    result = json.loads(response['message']['content'])
    
    summary_text = result.get('summary', 'No summary generated.')
    file_format = result.get('format', 'txt').lower()
    
    print(f"\n[AI Decision] The model decided to output as: {file_format.upper()}")
    
    
    if 'pdf' in file_format:
        pdf = FPDF(format='A4') 
        pdf.add_page()
        pdf.set_font("helvetica", size=12)
        
        pdf.multi_cell(0, 10, txt=summary_text) 
        pdf.output("summary_output.pdf")
        print(" Success! 'summary_output.pdf' has been created in your folder.")
        
    else:
        with open("summarize.txt", "w", encoding="utf-8") as f:
            f.write(summary_text)
        print(" Success! 'summarize.txt' has been created in your folder.")

except Exception as e:
    print(" Error processing the output:", e)
    print("Raw output from model was:", response['message']['content'])
    # the way to use the Agent: first docker exec -it ai-server bash ,then go to cd Week1 ,then python3 Agent.py , you can put the text you want to summarize, then tell tha agent summrize this text in 'txt' file or 'pdf'
    