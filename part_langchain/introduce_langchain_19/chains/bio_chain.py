from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables import RunnableSerializable
from pydantic import BaseModel, Field

from part_langchain.introduce_langchain_19.llm.llm import llm


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
