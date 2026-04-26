from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from part_langgraph.introduce_langgraph_12.agents.general_agent.general_agent import general_agent
from part_langgraph.introduce_langgraph_12.agents.reverse_text_agent.reverse_text_agent import reverse_text_agent
from part_langgraph.introduce_langgraph_12.agents.router_agent.router_agent import router_agent
from part_langgraph.introduce_langgraph_12.states.state import State

graph: StateGraph = StateGraph(State)

graph.add_node(node="router_agent", action=router_agent)
graph.add_node(node="reverse_text_agent", action=reverse_text_agent)
graph.add_node(node="general_agent", action=general_agent)

graph.add_edge(start_key=START, end_key="router_agent")

graph_compiled: CompiledStateGraph = graph.compile()
