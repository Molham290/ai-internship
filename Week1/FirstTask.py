import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input="what is the best model in ai.",
    system_instruction="You are a senior tech expert. Provide very concise, practical answers.",
    
    
    generation_config={
        "temperature": 0.2,
        "max_output_tokens": 1000
    }
)

print(interaction.output_text)