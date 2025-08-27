import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("⚠️ OPENAI_API_KEY not found. Please set it in .env")

openai.api_key = api_key

def call_llm(prompt, model="gpt-4o-mini"):
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


def get_embedding(text, model="text-embedding-3-small"):
    response = openai.embeddings.create(
        model=model,
        input=text
    )
    return response.data[0].embedding
