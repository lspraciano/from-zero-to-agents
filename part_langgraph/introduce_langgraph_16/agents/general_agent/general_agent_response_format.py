from pydantic import BaseModel


class GeneralAgentResponseFormat(BaseModel):
    response: str
