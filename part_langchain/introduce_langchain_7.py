import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.runnables import RunnableSerializable
from langchain_openai import ChatOpenAI

load_dotenv()

model: str = "gpt-4.1-mini"

llm: ChatOpenAI = ChatOpenAI(
    model=model,
    api_key=os.getenv("OPENAI_API_KEY"),
)

parser: StrOutputParser = StrOutputParser()

system_prompt: str = """
Você é um assistente especialista em {area}.
"""

user_message: str = "{user_message}"

template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessagePromptTemplate.from_template(template=system_prompt),
        HumanMessagePromptTemplate.from_template(template=user_message),
    ]
)

chain: RunnableSerializable = template | llm | parser


user_message: str = input("You: ")

response: str = chain.invoke(
    input={
        "area": "Física",
        "user_message": user_message,
    }
)

print(f"AI response: {response}")
