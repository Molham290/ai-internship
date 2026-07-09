import ollama


messages = [
    {
        'role': 'system',
        'content': 'You are a senior tech expert. Provide very concise, practical answers.'
    }
]

print("=== Context Window OPEN (Ollama). Type 'exit' to close ===")


while True:
    
    user_input = input("\nAsk Q: ")
    
    
    if user_input.lower() == 'exit':
        print("Closing window...")
        break

    
    messages.append({'role': 'user', 'content': user_input})

    
    response = ollama.chat(
        model='llama3',
        messages=messages,
        options={
            'temperature': 0.6,
            'top_p': 1.0,
            'top_k': 100,
            'num_ctx': 1024,
            'num_thread': 4,            
        }
    )

   
    ai_response = response['message']['content']
    
    
    print("\n The A:", ai_response)

    
    messages.append({'role': 'assistant', 'content': ai_response})