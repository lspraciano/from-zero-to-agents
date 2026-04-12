from pydantic import BaseModel, Field


class BioAgentResponseFormat(BaseModel):
    response: str = Field(description="Resposta final ao usuário")
