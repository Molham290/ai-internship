import os
from google import genai


os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6I4XHzDk_YW4KVWlDsqerTb429IlvM5DojP3dl9xZv1qw"


client = genai.Client()


interaction = client.interactions.create(
    model="gemini-3.5-flash", 
    input=" give me the best use of the AI "
)


print(interaction.output_text)