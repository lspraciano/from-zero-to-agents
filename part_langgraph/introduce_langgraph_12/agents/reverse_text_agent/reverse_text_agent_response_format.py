from pydantic import BaseModel


class ReverseTextAgentResponseFormat(BaseModel):
    response: str
