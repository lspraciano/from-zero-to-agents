import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage, ToolMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
)
from langchain_core.runnables import RunnableSerializable
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()

model: str = "gpt-4o-mini"

llm: ChatOpenAI = ChatOpenAI(
    model=model,
    api_key=os.getenv("OPENAI_API_KEY"),
)


@tool
def calculator_tool(expression: str) -> float:
    """Calcula uma expressão matemática e retorna o resultado."""
    return eval(expression)


class Response(BaseModel):
    use_tool: bool = Field(description="Se deve usar a calculadora ou não")
    expression: str = Field(description="Expressão matemática para calcular, vazia se não usar tool")
    response: str = Field(description="Resposta final ao usuário")


parse: PydanticOutputParser = PydanticOutputParser(pydantic_object=Response)

system_prompt: str = f"""
Você é um assistente geral.

Você tem acesso às seguintes ferramentas:
- {calculator_tool.name}: {calculator_tool.description}

Quando o usuário fizer uma pergunta matemática,
use a calculadora definindo use_tool como true e a expressão em expression.
Você pode chamar a calculadora quantas vezes precisar até ter a resposta final.
Quando o resultado da calculadora estiver disponível no histórico, use-o na sua resposta.
Quando não precisar da calculadora, apenas responda normalmente.

{{format_instructions}}
"""

user_message: str = "{user_message}"

template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessagePromptTemplate.from_template(template=system_prompt),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template(template=user_message),
    ]
)

chain: RunnableSerializable = template | llm | parse

history: list[BaseMessage] = []

while True:
    user_message: str = input("You: ")

    human_message: HumanMessage = HumanMessage(content=user_message)

    history.append(human_message)

    response: Response = chain.invoke(
        input={
            "user_message": user_message,
            "format_instructions": parse.get_format_instructions(),
            "history": history,
        }
    )

    while response.use_tool:
        tool_result: float = calculator_tool.invoke(input={"expression": response.expression})

        print(f"[Tool] {response.expression} = {tool_result}")

        tool_message: ToolMessage = ToolMessage(
            content=str(tool_result),
            tool_call_id=calculator_tool.name,
        )

        history.append(tool_message)

        response = chain.invoke(
            input={
                "user_message": user_message,
                "format_instructions": parse.get_format_instructions(),
                "history": history,
            }
        )

    ai_message: AIMessage = AIMessage(content=response.response)

    history.append(ai_message)

    print(f"AI response: {response.response}")
