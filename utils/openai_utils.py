# utils/openai_utils.py
import openai
import os
from dotenv import load_dotenv

# Load environment 
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env")
openai.api_key = api_key


def call_llm(prompt, context="", model="gpt-4o-mini", mode="default", asked_questions=None):
    """
    Calls the LLM.
    mode = "default" → collect info / ask questions (stay on-topic)
    """
    if mode == "default":
        system_prompt = (
            "You are TalentScout, an AI Hiring Assistant.\n"
            "Your ONLY job is to:\n"
            "- Collect candidate details\n"
            "- Ask technical questions based on the provided tech stack and years of experience\n"
            "- Evaluate answers ONLY in that context\n\n"
            "Stay strictly professional. If candidate goes off-topic, "
            "politely redirect to their tech stack or hiring-related details.\n"
            "Never repeat a previously asked question."
        )
    else:
        system_prompt = "You are TalentScout, an AI hiring assistant."

   
    if asked_questions:
        avoid_text = "\nPreviously asked questions (DO NOT repeat):\n" + "\n".join(asked_questions)
        prompt = prompt + avoid_text

    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context + "\n" + prompt},
        ],
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()
