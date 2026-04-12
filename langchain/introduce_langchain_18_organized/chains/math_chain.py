from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
)
from langchain_core.runnables import RunnableSerializable, Runnable
from pydantic import BaseModel, Field

from langchain.introduce_langchain_18_organized.llm.llm import llm
from langchain.introduce_langchain_18_organized.tool.calculator_tool import calculator_tool

load_dotenv()


class MathResponse(BaseModel):
    response: str = Field(description="Resposta final ao usuário")


math_parser: PydanticOutputParser = PydanticOutputParser(pydantic_object=MathResponse)

llm_with_tools: Runnable = llm.bind_tools(tools=[calculator_tool])

math_system_prompt: str = """
Você é um assistente especialista em matemática.

Quando não houver mais tool calls, responda APENAS com um JSON válido, sem texto adicional.

{format_instructions}
"""

math_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessagePromptTemplate.from_template(template=math_system_prompt),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template(template="{user_message}"),
    ]
)

math_chain: RunnableSerializable = math_template | llm_with_tools
