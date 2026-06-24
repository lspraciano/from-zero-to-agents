from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from part_langgraph.introduce_langgraph_16.vector_stores.knowledge_vector_store import (
    knowledge_vector_store,
)


def run_ingestion_pipeline(file_path: str) -> None:
    """Pipeline de ingestão para o vector store.

    Executa os 4 passos canônicos da indexação para RAG vetorial:

      1. Load   — lê o arquivo bruto do disco.
      2. Split  — quebra o texto em chunks menores (RecursiveCharacterTextSplitter).
      3. Embed  — transforma cada chunk em um vetor (feito pelo vector store).
      4. Index  — armazena os vetores em memória para busca por similaridade.

    Os passos 3 e 4 acontecem juntos dentro de `add_documents`: o vector store
    chama o modelo de embeddings para cada chunk e guarda o vetor resultante.

    Args:
        file_path: Caminho absoluto do arquivo .txt com o corpus.
    """
    file_path_object: Path = Path(file_path)

    raw_text: str = file_path_object.read_text(encoding="utf-8")

    if not raw_text.strip():
        print(
            f"[ingestion_pipeline] '{file_path}' está vazio. "
            "Vector store permanece sem documentos."
        )

        return

    raw_document: Document = Document(
        page_content=raw_text,
        metadata={"source": file_path},
    )

    text_splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    chunks: list[Document] = text_splitter.split_documents(documents=[raw_document])

    knowledge_vector_store.add_documents(documents=chunks)

    print(
        f"[ingestion_pipeline] {len(chunks)} chunks indexados a partir de '{file_path}'."
    )
