from langchain_core.runnables import RunnableSerializable

from part_langchain.introduce_langchain_20.agents.router_agent.router_agent_parser import (
    router_agent_parser,
)
from part_langchain.introduce_langchain_20.agents.router_agent.router_agent_template import (
    router_agent_template,
)
from part_langchain.introduce_langchain_20.llm.llm import llm

router_agent_chain: RunnableSerializable = (
    router_agent_template | llm | router_agent_parser
)
