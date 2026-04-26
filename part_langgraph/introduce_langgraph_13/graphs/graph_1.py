from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from part_langgraph.introduce_langgraph_13.agents.general_agent.general_agent import (
    general_agent,
)
from part_langgraph.introduce_langgraph_13.agents.pokemon_agent.pokemon_agent import (
    pokemon_agent,
)
from part_langgraph.introduce_langgraph_13.agents.router_agent.router_agent import (
    router_agent,
)
from part_langgraph.introduce_langgraph_13.states.state import State

graph: StateGraph = StateGraph(State)

graph.add_node(node="router_agent", action=router_agent)
graph.add_node(node="pokemon_agent", action=pokemon_agent)
graph.add_node(node="general_agent", action=general_agent)

graph.add_edge(start_key=START, end_key="router_agent")

graph_compiled: CompiledStateGraph = graph.compile()
