from langchain_core.output_parsers import PydanticOutputParser

from part_langchain.introduce_langchain_20.agents.router_agent.router_agent_response_format import (
    RouterAgentResponseFormat,
)

router_agent_parser: PydanticOutputParser = PydanticOutputParser(
    pydantic_object=RouterAgentResponseFormat
)
