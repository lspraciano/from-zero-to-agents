from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
)
from langchain_core.runnables import RunnableSerializable
from pydantic import BaseModel, Field

from part_langchain.introduce_langchain_18_organized.llm.llm import llm


class GeneralResponse(BaseModel):
    response: str = Field(description="Resposta final ao usuário")


general_parser: PydanticOutputParser = PydanticOutputParser(pydantic_object=GeneralResponse)

general_system_prompt: str = """
Você é um assistente de conhecimento geral.

Responda APENAS com um JSON válido, sem texto adicional.

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
