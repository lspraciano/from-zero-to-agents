from langchain_core.runnables import RunnableSerializable

from part_langchain.introduce_langchain_18_organized_2.agents.general_agent.general_agent_parser import (
    general_agent_parser,
)
from part_langchain.introduce_langchain_18_organized_2.agents.general_agent.general_agent_template import (
    general_agent_template,
)
from part_langchain.introduce_langchain_18_organized_2.llm.llm import llm

general_agent_chain: RunnableSerializable = (
    general_agent_template | llm | general_agent_parser
)
