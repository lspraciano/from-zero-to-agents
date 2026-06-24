from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_core.prompt_values import PromptValue
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command

from part_langgraph.introduce_langgraph_16.agents.knowledge_agent.knowledge_agent_response_format import (
    KnowledgeAgentResponseFormat,
)
from part_langgraph.introduce_langgraph_16.agents.knowledge_agent.knowledge_agent_template import (
    knowledge_agent_template,
)
from part_langgraph.introduce_langgraph_16.llm_models.llm_models import get_llm_model
from part_langgraph.introduce_langgraph_16.states.state import State
from part_langgraph.introduce_langgraph_16.tools.knowledge_search_tool import (
    knowledge_search_tool,
)

_knowledge_agent: CompiledStateGraph = create_agent(
    name="knowledge_agent",
    model=get_llm_model(model_name="gpt-4.1-mini"),
    response_format=KnowledgeAgentResponseFormat,
    tools=[knowledge_search_tool],
)


def knowledge_agent(state: State) -> Command:
    knowledge_input: PromptValue = knowledge_agent_template.invoke(
        input={
            "history": state["messages"],
        },
    )

    knowledge_result: dict = _knowledge_agent.invoke(input=knowledge_input)

    knowledge_response: KnowledgeAgentResponseFormat = knowledge_result[
        "structured_response"
    ]

    ai_message: AIMessage = AIMessage(content=knowledge_response.response)

    return Command(
        goto="__end__",
        update={
            "messages": [ai_message],
        },
    )
