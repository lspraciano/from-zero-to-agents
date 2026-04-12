from langchain_core.runnables import RunnableSerializable


from part_langchain.introduce_langchain_20.agents.bio_agent.bio_agent_parser import (
    bio_agent_parser,
)
from part_langchain.introduce_langchain_20.agents.bio_agent.bio_agent_template import (
    bio_agent_template,
)
from part_langchain.introduce_langchain_20.llm.llm import llm

bio_agent_chain: RunnableSerializable = bio_agent_template | llm | bio_agent_parser
