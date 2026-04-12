from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from part_langgraph.introduce_langgraph_10.edges.node_router_conditional_edge import (
    node_router_conditional_edge,
)
from part_langgraph.introduce_langgraph_10.nodes.node_a import node_a
from part_langgraph.introduce_langgraph_10.nodes.node_b import node_b
from part_langgraph.introduce_langgraph_10.nodes.node_router import node_router
from part_langgraph.introduce_langgraph_10.states.state import State

graph: StateGraph = StateGraph(State)  # type: ignore

graph.add_node(node="node_router", action=node_router)  # type: ignore
graph.add_node(node="node_a", action=node_a)  # type: ignore
graph.add_node(node="node_b", action=node_b)  # type: ignore

graph.add_edge(start_key=START, end_key="node_router")

graph.add_conditional_edges(source="node_router", path=node_router_conditional_edge)

graph.add_edge(start_key="node_a", end_key=END)
graph.add_edge(start_key="node_b", end_key=END)

graph_compiled: CompiledStateGraph = graph.compile()
