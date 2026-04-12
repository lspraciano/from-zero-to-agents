import os
from typing import TypedDict, Literal

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage, ToolMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel, Field

load_dotenv()

model: str = "gpt-4.1-mini"

llm: ChatOpenAI = ChatOpenAI(
    model=model,
    api_key=os.getenv("OPENAI_API_KEY"),
)


# --- Tools ---


@tool
def calculator_tool(expression: str) -> float:
    """Calcula uma expressão matemática e retorna o resultado."""
    return eval(expression)


llm_with_tools = llm.bind_tools(tools=[calculator_tool])


# --- State ---


class State(TypedDict):
    user_message: str
    history: list[BaseMessage]
    agent: str
    response: str


# --- Router ---


class RouterResponse(BaseModel):
    agent: Literal["math", "general"] = Field(
        description="Agente para o qual a mensagem deve ser roteada"
    )


router_parse: PydanticOutputParser = PydanticOutputParser(
    pydantic_object=RouterResponse
)

router_system_prompt: str = """
Você é um roteador de mensagens. Analise o histórico da conversa e a mensagem atual do usuário para decidir para qual agente direcionar.

- "math": para perguntas matemáticas ou que envolvam cálculos
- "general": para perguntas de conhecimento geral

Considere o contexto completo da conversa para entender a real intenção do usuário.

{format_instructions}
"""

router_template: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessagePromptTemplate.from_template(template=router_system_prompt),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template(template="{user_message}"),
    ]
)

router_chain = router_template | llm | router_parse


# --- Math Agent ---


class MathResponse(BaseModel):
    response: str = Field(description="Resposta final ao usuário")


math_parse: PydanticOutputParser = PydanticOutputParser(pydantic_object=MathResponse)

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

math_chain = math_template | llm_with_tools


# --- General Agent ---


class GeneralResponse(BaseModel):
    response: str = Field(description="Resposta final ao usuário")


general_parse: PydanticOutputParser = PydanticOutputParser(
    pydantic_object=GeneralResponse
)

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

general_chain = general_template | llm | general_parse


# --- Nodes ---


def router_node(state: State) -> dict:
    router_response: RouterResponse = router_chain.invoke(
        input={
            "user_message": state["user_message"],
            "history": state["history"],
            "format_instructions": router_parse.get_format_instructions(),
        }
    )

    print(f"[Router] → {router_response.agent}")

    return {"agent": router_response.agent}


def math_node(state: State) -> dict:
    response: AIMessage = math_chain.invoke(
        input={
            "user_message": state["user_message"],
            "format_instructions": math_parse.get_format_instructions(),
            "history": state["history"],
        }
    )

    local_history: list[BaseMessage] = []

    while response.tool_calls:
        local_history.append(response)

        for tool_call in response.tool_calls:
            tool_result: float = calculator_tool.invoke(input=tool_call["args"])

            print(f"[Tool] {tool_call['name']}({tool_call['args']}) = {tool_result}")

            tool_message: ToolMessage = ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"],
            )

            local_history.append(tool_message)

        response: AIMessage = math_chain.invoke(
            input={
                "user_message": state["user_message"],
                "format_instructions": math_parse.get_format_instructions(),
                "history": state["history"] + local_history,
            }
        )

    parsed_response: MathResponse = math_parse.invoke(input=response)

    updated_history: list[BaseMessage] = state["history"] + [
        HumanMessage(content=state["user_message"]),
        AIMessage(content=parsed_response.response),
    ]

    return {
        "response": parsed_response.response,
        "history": updated_history,
    }


def general_node(state: State) -> dict:
    parsed_response: GeneralResponse = general_chain.invoke(
        input={
            "user_message": state["user_message"],
            "format_instructions": general_parse.get_format_instructions(),
            "history": state["history"],
        }
    )

    updated_history: list[BaseMessage] = state["history"] + [
        HumanMessage(content=state["user_message"]),
        AIMessage(content=parsed_response.response),
    ]

    return {
        "response": parsed_response.response,
        "history": updated_history,
    }


def decide_agent(state: State) -> str:
    return state["agent"]


# --- Graph ---

graph: StateGraph = StateGraph(State)  # type: ignore

graph.add_node(node="router", action=router_node)  # type: ignore
graph.add_node(node="math", action=math_node)  # type: ignore
graph.add_node(node="general", action=general_node)  # type: ignore

graph.add_edge(start_key=START, end_key="router")

graph.add_conditional_edges(
    source="router",
    path=decide_agent,
    path_map={
        "math": "math",
        "general": "general",
    },
)

graph.add_edge(start_key="math", end_key=END)
graph.add_edge(start_key="general", end_key=END)

app: CompiledStateGraph = graph.compile()

history: list[BaseMessage] = []

while True:
    user_message: str = input("You: ")

    initial_state: State = {
        "user_message": user_message,
        "history": history,
        "agent": "",
        "response": "",
    }

    result: dict = app.invoke(input=initial_state)  # type: ignore

    history = result["history"]

    print(f"AI response: {result['response']}")
