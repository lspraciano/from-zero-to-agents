import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables import RunnableSerializable
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()

model: str = "gpt-4.1-mini"

llm: ChatOpenAI = ChatOpenAI(
    model=model,
    api_key=os.getenv("OPENAI_API_KEY"),
)


class Response(BaseModel):
    response: str = Field(description="Resposta do assistente")
    summary: str = Field(description="Resumo da intenção do usuário")


parser: PydanticOutputParser = PydanticOutputParser(pydantic_object=Response)

system_prompt: str = """
Você é um assistente especialista em {area}.

{format_instructions}
"""

user_message: str = "{user_message}"

template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessagePromptTemplate.from_template(template=system_prompt),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template(template=user_message),
    ]
)

chain: RunnableSerializable = template | llm | parser

history: list[BaseMessage] = []

while True:
    user_message: str = input("You: ")

    response: Response = chain.invoke(
        input={
            "area": "Física",
            "user_message": user_message,
            "history": history,
            "format_instructions": parser.get_format_instructions(),
        }
    )

    response_dumped: str = response.model_dump_json()

    ai_message: AIMessage = AIMessage(content=response_dumped)

    human_message: HumanMessage = HumanMessage(content=user_message)

    history.append(human_message)

    history.append(ai_message)

    print(f"AI response: {response}")
