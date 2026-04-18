from typing import Literal

from pydantic import BaseModel, Field


class RouterAgentResponseFormat(BaseModel):
    router_destination: Literal[
        "invert_agent",
        "general_agent",
    ] = Field(
        description="Agente de destino",
        default="general_agent",
    )
