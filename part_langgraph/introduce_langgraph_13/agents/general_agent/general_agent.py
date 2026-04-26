from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_core.prompt_values import PromptValue
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command

from part_langgraph.introduce_langgraph_13.agents.general_agent.general_agent_response_format import (
    GeneralAgentResponseFormat,
)
from part_langgraph.introduce_langgraph_13.agents.general_agent.general_agent_template import (
    general_agent_template,
)
from part_langgraph.introduce_langgraph_13.llm_models.llm_models import get_llm_model
from part_langgraph.introduce_langgraph_13.states.state import State

_general_agent: CompiledStateGraph = create_agent(
    name="general_agent",
    model=get_llm_model(model_name="gpt-4.1-mini"),
    response_format=GeneralAgentResponseFormat,
    tools=[],
)


def general_agent(state: State) -> Command:
    general_input: PromptValue = general_agent_template.invoke(
        input={
            "history": state["messages"],
        },
    )

    general_result: dict = _general_agent.invoke(input=general_input)

    general_response: GeneralAgentResponseFormat = general_result["structured_response"]

    ai_message: AIMessage = AIMessage(content=general_response.response)

    return Command(
        goto="__end__",
        update={
            "messages": [ai_message],
        },
    )