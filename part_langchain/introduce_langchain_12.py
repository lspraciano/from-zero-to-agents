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
    use_tool: bool = Field(description="Se deve usar a calculadora ou não")
    expression: str = Field(
        description="Expressão matemática para calcular, vazia se não usar tool"
    )
    response: str = Field(description="Resposta final ao usuário")


parser: PydanticOutputParser = PydanticOutputParser(pydantic_object=Response)

system_prompt: str = """
Você é um assistente geral.

Você tem acesso a uma calculadora. Quando o usuário fizer uma pergunta matemática,
use a calculadora definindo use_tool como true e a expressão em expression.
Quando o resultado da calculadora estiver disponível, use-o na sua resposta.
Quando não precisar da calculadora, apenas responda normalmente.

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


def calculator_tool(expression: str) -> float:
    return eval(expression)


while True:
    user_message: str = input("You: ")

    response: Response = chain.invoke(
        input={
            "user_message": user_message,
            "format_instructions": parser.get_format_instructions(),
            "history": history,
        }
    )

    print(f"[Raw Response] {response}")

    if response.use_tool:
        tool_expression: str = response.expression

        tool_result: float = calculator_tool(expression=tool_expression)

        print(f"[Tool] {tool_expression} = {tool_result}")

        response.response = f"O resultado de {tool_expression} é {tool_result}"

    response_dumped: str = response.model_dump_json()

    ai_message: AIMessage = AIMessage(content=response_dumped)

    human_message: HumanMessage = HumanMessage(content=user_message)

    history.append(human_message)

    history.append(ai_message)

    print(f"AI response: {response}")
