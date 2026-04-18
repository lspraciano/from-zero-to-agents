from langchain_core.messages import AIMessage
from langchain_core.prompt_values import PromptValue

from part_langgraph.introduce_langgraph_11.agents.reverse_text_agent.reverse_text_agent import (
    reverse_text_agent,
)
from part_langgraph.introduce_langgraph_11.agents.reverse_text_agent.reverse_text_agent_response_format import (
    ReverseTextAgentResponseFormat,
)
from part_langgraph.introduce_langgraph_11.agents.reverse_text_agent.reverse_text_agent_template import (
    reverse_text_agent_template,
)
from part_langgraph.introduce_langgraph_11.states.state import State


def reverse_text_node(state: State) -> dict:
    reverse_text_input: PromptValue = reverse_text_agent_template.invoke(
        input={
            "history": state["messages"],
        },
    )

    reverse_text_result: dict = reverse_text_agent.invoke(input=reverse_text_input)

    reverse_text_response: ReverseTextAgentResponseFormat = reverse_text_result[
        "structured_response"
    ]

    ai_message: AIMessage = AIMessage(content=reverse_text_response.response)

    return {
        "messages": [ai_message],
    }
