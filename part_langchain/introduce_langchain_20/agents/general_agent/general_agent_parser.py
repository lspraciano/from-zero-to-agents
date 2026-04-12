from langchain_core.output_parsers import PydanticOutputParser

from part_langchain.introduce_langchain_20.agents.general_agent.general_agent_response_format import (
    GeneralAgentResponseFormat,
)

general_agent_parser: PydanticOutputParser = PydanticOutputParser(
    pydantic_object=GeneralAgentResponseFormat
)
