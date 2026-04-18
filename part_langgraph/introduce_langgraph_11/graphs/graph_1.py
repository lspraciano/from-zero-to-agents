from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from part_langgraph.introduce_langgraph_11.edges.router_node_conditional_edge import (
    router_node_conditional_edge,
)
from part_langgraph.introduce_langgraph_11.nodes.general_node import general_node
from part_langgraph.introduce_langgraph_11.nodes.reverse_text_node import (
    reverse_text_node,
)
from part_langgraph.introduce_langgraph_11.nodes.router_node import router_node
from part_langgraph.introduce_langgraph_11.states.state import State

graph: StateGraph = StateGraph(State)

graph.add_node(node="router_node", action=router_node)
graph.add_node(node="reverse_text_node", action=reverse_text_node)
graph.add_node(node="general_node", action=general_node)

graph.add_edge(start_key=START, end_key="router_node")

graph.add_conditional_edges(source="router_node", path=router_node_conditional_edge)

graph.add_edge(start_key="reverse_text_node", end_key=END)
graph.add_edge(start_key="general_node", end_key=END)

graph_compiled: CompiledStateGraph = graph.compile()
