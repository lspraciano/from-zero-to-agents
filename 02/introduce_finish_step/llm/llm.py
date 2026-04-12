import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

model: str = "gpt-4o-mini"

llm: ChatOpenAI = ChatOpenAI(
    model=model,
    api_key=os.getenv("OPENAI_API_KEY"),
)
