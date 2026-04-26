from pydantic import BaseModel


class PokemonAgentResponseFormat(BaseModel):
    response: str
