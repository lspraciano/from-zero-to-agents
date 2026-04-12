import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion

load_dotenv()

client: OpenAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

model: str = "gpt-4o-mini"

system_prompt: str = """
Você responde apenas com emojis. Nada de texto.
"""

user_message: str = "Como você está?"

messages: list[dict] = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_message},
]

response: ChatCompletion = client.chat.completions.create(
    model=model,
    messages=messages,
)

print(f"AI response: {response.choices[0].message.content}")
