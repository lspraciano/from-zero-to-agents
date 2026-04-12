from langchain_core.output_parsers import PydanticOutputParser

from part_langchain.introduce_langchain_18_organized_2.agents.bio_agent.bio_agent_response_format import (
    BioAgentResponseFormat,
)

bio_agent_parser: PydanticOutputParser = PydanticOutputParser(
    pydantic_object=BioAgentResponseFormat
)
