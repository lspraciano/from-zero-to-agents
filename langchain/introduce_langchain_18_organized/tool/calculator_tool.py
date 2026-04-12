from langchain_core.tools import tool


@tool
def calculator_tool(expression: str) -> float:
    """Calcula uma expressão matemática e retorna o resultado."""
    return eval(expression)
