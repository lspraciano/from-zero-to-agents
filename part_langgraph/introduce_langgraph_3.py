import os
from typing import TypedDict, Literal

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
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


router_agent: CompiledStateGraph = create_agent(
    model=llm,
    tools=[],
    system_prompt="""
Você é um roteador de mensagens. Analise o histórico da conversa e a mensagem atual do usuário para decidir para qual agente direcionar.

- "math": para perguntas matemáticas ou que envolvam cálculos
- "general": para perguntas de conhecimento geral

Considere o contexto completo da conversa para entender a real intenção do usuário.
""",
    response_format=RouterResponse,
)


# --- Math Agent ---


class MathResponse(BaseModel):
    response: str = Field(description="Resposta final ao usuário")


math_agent: CompiledStateGraph = create_agent(
    model=llm,
    tools=[calculator_tool],
    system_prompt="Você é um assistente especialista em matemática.",
    response_format=MathResponse,
)


# --- General Agent ---


class GeneralResponse(BaseModel):
    response: str = Field(description="Resposta final ao usuário")


general_agent: CompiledStateGraph = create_agent(
    model=llm,
    tools=[],
    system_prompt="Você é um assistente de conhecimento geral.",
    response_format=GeneralResponse,
)


# --- Nodes ---


def router_node(state: State) -> dict:
    messages: list[BaseMessage] = state["history"] + [
        HumanMessage(content=state["user_message"])
    ]

    result: dict = router_agent.invoke(input={"messages": messages})

    router_response: RouterResponse = result["structured_response"]

    print(f"[Router] → {router_response.agent}")

    return {"agent": router_response.agent}


def math_node(state: State) -> dict:
    messages: list[BaseMessage] = state["history"] + [
        HumanMessage(content=state["user_message"])
    ]

    result: dict = math_agent.invoke(input={"messages": messages})

    response: str = result["structured_response"].response

    updated_history: list[BaseMessage] = state["history"] + [
        HumanMessage(content=state["user_message"]),
        AIMessage(content=response),
    ]

    return {"response": response, "history": updated_history}


def general_node(state: State) -> dict:
    messages: list[BaseMessage] = state["history"] + [
        HumanMessage(content=state["user_message"])
    ]

    result: dict = general_agent.invoke(input={"messages": messages})

    response: str = result["structured_response"].response

    updated_history: list[BaseMessage] = state["history"] + [
        HumanMessage(content=state["user_message"]),
        AIMessage(content=response),
    ]

    return {"response": response, "history": updated_history}


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
