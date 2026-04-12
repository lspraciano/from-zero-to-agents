import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage, ToolMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
)
from langchain_core.runnables import RunnableSerializable
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool, BaseTool
from pydantic import BaseModel, Field
from typing import Literal

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


# --- Router ---

class RouterResponse(BaseModel):
    agent: Literal["math", "general"] = Field(description="Agente para o qual a mensagem deve ser roteada")


router_parse: PydanticOutputParser = PydanticOutputParser(pydantic_object=RouterResponse)

router_system_prompt: str = """
Você é um roteador de mensagens. Sua única função é decidir para qual agente a mensagem do usuário deve ser enviada.

- "math": para perguntas matemáticas ou que envolvam cálculos
- "general": para perguntas de conhecimento geral

{format_instructions}
"""

router_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessagePromptTemplate.from_template(template=router_system_prompt),
        HumanMessagePromptTemplate.from_template(template="{user_message}"),
    ]
)

router_chain: RunnableSerializable = router_template | llm | router_parse


# --- Math Agent ---

class MathResponse(BaseModel):
    response: str = Field(description="Resposta final ao usuário")


math_parse: PydanticOutputParser = PydanticOutputParser(pydantic_object=MathResponse)

llm_with_tools = llm.bind_tools(tools=[calculator_tool])

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

tools: dict[str, BaseTool] = {
    calculator_tool.name: calculator_tool,
}


# --- General Agent ---

class GeneralResponse(BaseModel):
    response: str = Field(description="Resposta final ao usuário")


general_parse: PydanticOutputParser = PydanticOutputParser(pydantic_object=GeneralResponse)

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

general_chain: RunnableSerializable = general_template | llm | general_parse


# --- Orquestrador ---

history: list[BaseMessage] = []

while True:
    user_message: str = input("You: ")

    # Roteamento
    router_response: RouterResponse = router_chain.invoke(
        input={
            "user_message": user_message,
            "format_instructions": router_parse.get_format_instructions(),
        }
    )

    print(f"[Router] → {router_response.agent}")

    if router_response.agent == "math":
        response: AIMessage = math_chain.invoke(
            input={
                "user_message": user_message,
                "format_instructions": math_parse.get_format_instructions(),
                "history": history,
            }
        )

        while response.tool_calls:
            history.append(response)

            for tool_call in response.tool_calls:
                selected_tool: BaseTool = tools[tool_call["name"]]
                tool_result = selected_tool.invoke(input=tool_call["args"])

                print(f"[Tool] {tool_call['name']}({tool_call['args']}) = {tool_result}")

                tool_message: ToolMessage = ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"],
                )

                history.append(tool_message)

            response = math_chain.invoke(
                input={
                    "user_message": user_message,
                    "format_instructions": math_parse.get_format_instructions(),
                    "history": history,
                }
            )

        parsed_response: MathResponse = math_parse.invoke(input=response)

    else:
        parsed_response: GeneralResponse = general_chain.invoke(
            input={
                "user_message": user_message,
                "format_instructions": general_parse.get_format_instructions(),
                "history": history,
            }
        )

    human_message: HumanMessage = HumanMessage(content=user_message)

    ai_message: AIMessage = AIMessage(content=parsed_response.response)

    history.append(human_message)

    history.append(ai_message)

    print(f"AI response: {parsed_response.response}")