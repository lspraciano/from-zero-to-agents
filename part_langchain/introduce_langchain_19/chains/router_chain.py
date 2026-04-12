from typing import Literal

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.runnables import RunnableSerializable
from pydantic import BaseModel, Field

from part_langchain.introduce_langchain_19.llm.llm import llm


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
