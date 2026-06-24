from langchain_core.vectorstores import InMemoryVectorStore

from part_langgraph.introduce_langgraph_16.embeddings.embeddings import (
    get_embeddings_model,
)

knowledge_vector_store: InMemoryVectorStore = InMemoryVectorStore(
    embedding=get_embeddings_model(),
)
