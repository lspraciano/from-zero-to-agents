from typing import Literal

from pydantic import BaseModel, Field


class RouterAgentResponseFormat(BaseModel):
    router_destination: Literal[
        "pokemon_agent",
        "general_agent",
    ] = Field(
        description="Agente de destino",
    )
