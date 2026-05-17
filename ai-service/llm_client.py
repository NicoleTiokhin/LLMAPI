from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

def call_llm(prompt: str) -> str:
    try:
        response = client.responses.create(
            model="openai/gpt-oss-20b",  # ← from Groq docs
            input=prompt
        )

        return response.output_text

    except Exception as e:
        print("🔥 LLM ERROR:", str(e))
        raise e