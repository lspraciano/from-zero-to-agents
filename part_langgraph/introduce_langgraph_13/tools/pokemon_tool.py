import requests
from langchain_core.tools import tool


@tool
def pokemon_tool(name: str) -> dict:
    """Busca informações de um Pokémon pelo nome na PokeAPI.

    Args:
        name: Nome do Pokémon em inglês (ex: 'pikachu', 'charizard').
    """
    url: str = f"https://pokeapi.co/api/v2/pokemon/{name.lower().strip()}"

    try:
        response: requests.Response = requests.get(
            url=url,
            timeout=10,
        )

    except requests.RequestException as error:
        return {"error": f"Falha ao consultar a PokeAPI: {error}"}

    if response.status_code == 404:
        return {"error": f"Pokémon '{name}' não encontrado."}

    if response.status_code != 200:
        return {"error": f"Erro inesperado: status {response.status_code}"}

    data: dict = response.json()

    types: list[str] = []

    for type_entry in data["types"]:
        types.append(type_entry["type"]["name"])

    abilities: list[str] = []

    for ability_entry in data["abilities"]:
        abilities.append(ability_entry["ability"]["name"])

    base_stats: dict[str, int] = {}

    for stat_entry in data["stats"]:
        stat_name: str = stat_entry["stat"]["name"]
        stat_value: int = stat_entry["base_stat"]
        base_stats[stat_name] = stat_value

    return {
        "id": data["id"],
        "name": data["name"],
        "height_m": data["height"] / 10,
        "weight_kg": data["weight"] / 10,
        "types": types,
        "abilities": abilities,
        "base_stats": base_stats,
    }
