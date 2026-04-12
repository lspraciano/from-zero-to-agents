import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage, ToolMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables import RunnableSerializable, Runnable
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()

model: str = "gpt-4.1-mini"

llm: ChatOpenAI = ChatOpenAI(
    model=model,
    api_key=os.getenv("OPENAI_API_KEY"),
)


@tool
def calculator_tool(expression: str) -> float:
    """Calcula uma expressão matemática e retorna o resultado."""
    return eval(expression)


llm_with_tools: Runnable = llm.bind_tools(tools=[calculator_tool])


class Response(BaseModel):
    response: str = Field(description="Resposta final ao usuário")


parser: PydanticOutputParser = PydanticOutputParser(pydantic_object=Response)

system_prompt: str = """
Você é um assistente geral.

Quando não houver mais tool calls, responda APENAS com um JSON válido, sem texto adicional.

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

chain: RunnableSerializable = template | llm_with_tools

history: list[BaseMessage] = []

while True:
    user_message: str = input("You: ")

    human_message: HumanMessage = HumanMessage(content=user_message)

    history.append(human_message)

    ai_message: AIMessage = chain.invoke(
        input={
            "user_message": user_message,
            "format_instructions": parser.get_format_instructions(),
            "history": history,
        }
    )

    history.append(ai_message)

    while ai_message.tool_calls:
        for tool_call in ai_message.tool_calls:
            tool_args: dict = tool_call["args"]
            tool_expression: str = tool_args["expression"]

            tool_result: float = calculator_tool.invoke(input=tool_args)

            tool_response: str = (
                f"[Tool] O resultado de {tool_expression} é {tool_result}"
            )

            print(tool_response)

            tool_message: ToolMessage = ToolMessage(
                content=tool_response,
                tool_call_id=tool_call["id"],
            )

            history.append(tool_message)

        ai_message: AIMessage = chain.invoke(
            input={
                "user_message": user_message,
                "format_instructions": parser.get_format_instructions(),
                "history": history,
            }
        )

        history.append(ai_message)

        print(f"[After Tool Response] {ai_message}")

    response: Response = parser.invoke(input=ai_message)

    print(f"AI response: {response}")
