import os
from typing import Literal

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


# --- Router ---


class RouterResponse(BaseModel):
    agent: Literal["bio", "general"] = Field(
        description="Agente para o qual a mensagem deve ser roteada"
    )


router_parser: PydanticOutputParser = PydanticOutputParser(
    pydantic_object=RouterResponse
)

router_system_prompt: str = """
Você é um roteador de mensagens. Sua única função é decidir para qual agente a mensagem do usuário deve ser enviada.

- "bio": para perguntas voltadas para biológia
- "general": para perguntas de conhecimento geral

{format_instructions}
"""

router_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessagePromptTemplate.from_template(template=router_system_prompt),
        HumanMessagePromptTemplate.from_template(template="{user_message}"),
    ]
)

router_chain: RunnableSerializable = router_template | llm | router_parser


# --- Bio Agent ---


class BioResponse(BaseModel):
    response: str = Field(description="Resposta final ao usuário")


bio_parser: PydanticOutputParser = PydanticOutputParser(pydantic_object=BioResponse)

bio_system_prompt: str = """
Você é um assistente especialista em biologia.

{format_instructions}
"""

bio_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessagePromptTemplate.from_template(template=bio_system_prompt),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template(template="{user_message}"),
    ]
)

bio_chain: RunnableSerializable = bio_template | llm | bio_parser


# --- General Agent ---


class GeneralResponse(BaseModel):
    response: str = Field(description="Resposta final ao usuário")


general_parser: PydanticOutputParser = PydanticOutputParser(
    pydantic_object=GeneralResponse
)

general_system_prompt: str = """
Você é um assistente de conhecimento geral.

{format_instructions}
"""

general_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessagePromptTemplate.from_template(template=general_system_prompt),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template(template="{user_message}"),
    ]
)

general_chain: RunnableSerializable = general_template | llm | general_parser

# --- Orquestrador ---

history: list[BaseMessage] = []

while True:
    user_message: str = input("You: ")

    human_message: HumanMessage = HumanMessage(content=user_message)

    history.append(human_message)

    router_response: RouterResponse = router_chain.invoke(
        input={
            "user_message": user_message,
            "format_instructions": router_parser.get_format_instructions(),
        }
    )

    print(f"[Router] → {router_response}")

    if router_response.agent == "bio":
        bio_response: BioResponse = bio_chain.invoke(
            input={
                "user_message": user_message,
                "format_instructions": bio_parser.get_format_instructions(),
                "history": history,
            }
        )

        ai_message: AIMessage = AIMessage(content=bio_response.response)

        print(f"[Bio Agent] → {bio_response}")

    else:
        general_response: GeneralResponse = general_chain.invoke(
            input={
                "user_message": user_message,
                "format_instructions": general_parser.get_format_instructions(),
                "history": history,
            }
        )

        ai_message: AIMessage = AIMessage(content=general_response.response)

        print(f"[General Agent] → {general_response}")

    history.append(ai_message)

    print(f"AI response: {ai_message}")
