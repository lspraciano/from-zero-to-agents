from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_core.prompt_values import PromptValue
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command

from part_langgraph.introduce_langgraph_12.agents.reverse_text_agent.reverse_text_agent_response_format import (
    ReverseTextAgentResponseFormat,
)
from part_langgraph.introduce_langgraph_12.agents.reverse_text_agent.reverse_text_agent_template import (
    reverse_text_agent_template,
)
from part_langgraph.introduce_langgraph_12.llm_models.llm_models import get_llm_model
from part_langgraph.introduce_langgraph_12.states.state import State
from part_langgraph.introduce_langgraph_12.tools.invert_text_tool import (
    reverse_text_tool,
)

_reverse_text_agent: CompiledStateGraph = create_agent(
    name="reverse_text_agent",
    model=get_llm_model(model_name="gpt-4.1-mini"),
    response_format=ReverseTextAgentResponseFormat,
    tools=[reverse_text_tool],
)


def reverse_text_agent(state: State) -> Command:
    reverse_text_input: PromptValue = reverse_text_agent_template.invoke(
        input={
            "history": state["messages"],
        },
    )

    reverse_text_result: dict = current_agent.invoke(input=reverse_text_input)

    reverse_text_response: ReverseTextAgentResponseFormat = reverse_text_result[
        "structured_response"
    ]

    ai_message: AIMessage = AIMessage(content=reverse_text_response.response)

    return Command(
        goto="__end__",
        update={
            "messages": [ai_message],
        },
    )