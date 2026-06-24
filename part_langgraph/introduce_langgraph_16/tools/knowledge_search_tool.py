from langchain_core.documents import Document
from langchain_core.tools import tool

from part_langgraph.introduce_langgraph_16.vector_stores.knowledge_vector_store import (
    knowledge_vector_store,
)


@tool
def knowledge_search_tool(query: str) -> list[dict]:
    """
    Busca trechos relevantes na base de conhecimento.

    Args:
        query: Pergunta ou tópico em linguagem natural.
    """
    print(f"\n[knowledge_search_tool] query: {query!r}")

    documents: list[Document] = knowledge_vector_store.similarity_search(
        query=query,
        k=3,
    )

    print(f"[knowledge_search_tool] {len(documents)} chunks recuperados:")

    results: list[dict] = []

    for document in documents:
        results.append(
            {
                "content": document.page_content,
                "source": document.metadata.get("source"),
            }
        )

    return results
