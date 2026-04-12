import os

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSerializable
from langchain_openai import ChatOpenAI

load_dotenv()

model: str = "gpt-4o-mini"

llm: ChatOpenAI = ChatOpenAI(
    model=model,
    api_key=os.getenv("OPENAI_API_KEY"),
)

parse: StrOutputParser = StrOutputParser()

system_prompt: str = """
Você responde apenas com emojis. Nada de texto.
"""

user_message: str = "Como você está?"

messages: list[BaseMessage] = [
    SystemMessage(content=system_prompt),
    HumanMessage(content=user_message),
]

chain: RunnableSerializable = llm | parse

response: str = chain.invoke(input=messages)

print(f"AI response: {response}")
