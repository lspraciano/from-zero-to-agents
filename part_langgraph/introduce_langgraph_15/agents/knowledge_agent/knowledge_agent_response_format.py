from pydantic import BaseModel


class KnowledgeAgentResponseFormat(BaseModel):
    response: str
