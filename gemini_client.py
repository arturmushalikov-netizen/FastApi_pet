from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key = GENAI_API_KEY)

def get_answer_from_gemini(prompt: str):
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )
    return interaction.output_text

if __name__ == "__main__":
    prompt = "What is the capital of France?"
    answer = get_answer_from_gemini(prompt)
    print(answer)
