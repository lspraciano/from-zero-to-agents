from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_core.prompt_values import PromptValue
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command

from part_langgraph.introduce_langgraph_13.agents.pokemon_agent.pokemon_agent_response_format import (
    PokemonAgentResponseFormat,
)
from part_langgraph.introduce_langgraph_13.agents.pokemon_agent.pokemon_agent_template import (
    pokemon_agent_template,
)
from part_langgraph.introduce_langgraph_13.llm_models.llm_models import get_llm_model
from part_langgraph.introduce_langgraph_13.states.state import State
from part_langgraph.introduce_langgraph_13.tools.pokemon_tool import pokemon_tool

_pokemon_agent: CompiledStateGraph = create_agent(
    name="pokemon_agent",
    model=get_llm_model(model_name="gpt-4.1-mini"),
    response_format=PokemonAgentResponseFormat,
    tools=[pokemon_tool],
)


def pokemon_agent(state: State) -> Command:
    pokemon_input: PromptValue = pokemon_agent_template.invoke(
        input={
            "history": state["messages"],
        },
    )

    pokemon_result: dict = _pokemon_agent.invoke(input=pokemon_input)

    pokemon_response: PokemonAgentResponseFormat = pokemon_result["structured_response"]

    ai_message: AIMessage = AIMessage(content=pokemon_response.response)

    return Command(
        goto="__end__",
        update={
            "messages": [ai_message],
        },
    )
