from langchain_core.messages import AIMessage
from langchain_core.prompt_values import PromptValue

from part_langgraph.introduce_langgraph_11.agents.general_agent.general_agent import (
    general_agent,
)
from part_langgraph.introduce_langgraph_11.agents.general_agent.general_agent_response_format import (
    GeneralAgentResponseFormat,
)
from part_langgraph.introduce_langgraph_11.agents.general_agent.general_agent_template import (
    general_agent_template,
)
from part_langgraph.introduce_langgraph_11.states.state import State


def general_node(state: State) -> dict:
    general_input: PromptValue = general_agent_template.invoke(
        input={
            "history": state["messages"],
        },
    )

    general_result: dict = general_agent.invoke(input=general_input)

    general_response: GeneralAgentResponseFormat = general_result["structured_response"]

    ai_message: AIMessage = AIMessage(content=general_response.response)

    return {
        "messages": [ai_message],
    }
