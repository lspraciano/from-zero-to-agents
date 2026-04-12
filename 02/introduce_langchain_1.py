import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI

load_dotenv()

model: str = "gpt-4o-mini"

llm: ChatOpenAI = ChatOpenAI(
    model=model,
    api_key=os.getenv("OPENAI_API_KEY"),
)

system_prompt: str = """
Você responde apenas com emojis. Nada de texto.
"""

user_message: str = "Como você está?"

messages: list[dict] = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_message},
]

response: AIMessage = llm.invoke(input=messages)

print(f"AI response: {response.content}")
