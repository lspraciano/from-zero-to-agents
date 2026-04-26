from langchain_core.tools import tool


@tool
def reverse_text_tool(text: str) -> str:
    """Inverte o texto fornecido."""
    return text[::-1]
