# langmem/llm_client.py

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_llm(prompt: str, model: str = "gpt-4o") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an assistant that answers questions using memory context."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
