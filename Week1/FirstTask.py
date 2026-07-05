import os
from google import genai
from dotenv import load_dotenv


load_dotenv()


os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")


client = genai.Client()
interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input="best use of ai."
)

print(interaction.output_text)