from pydantic import BaseModel, Field


class GeneralAgentResponseFormat(BaseModel):
    response: str = Field(description="Resposta final ao usuário")
