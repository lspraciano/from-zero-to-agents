from typing import Literal

from pydantic import BaseModel, Field


class RouterAgentResponseFormat(BaseModel):
    agent: Literal["bio", "general"] = Field(
        description="Agente para o qual a mensagem deve ser roteada"
    )
