"""
vector_store.py

Gerencia o vector store ChromaDB para armazenar
e recuperar embeddings dos documentos clínicos.

O índice é persistido em disco na pasta chroma_db/
para não precisar reindexar a cada execução.
"""

import os

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from src.rag.embeddings import obter_embeddings


# Pasta onde o ChromaDB vai salvar o índice em disco
CHROMA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "chroma_db"
)

COLLECTION_NAME = "bluadiagnostics_kb"


def criar_vector_store(chunks: list[Document]) -> Chroma:
    """
    Cria e persiste o vector store a partir dos chunks.

    Deve ser chamado apenas uma vez para indexar a base.
    Nas chamadas seguintes, use carregar_vector_store().

    Args:
        chunks: lista de chunks gerados pelo chunking.py

    Returns:
        Instância do Chroma pronta para consultas
    """
    embeddings = obter_embeddings()
    chroma_path = os.path.abspath(CHROMA_PATH)

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=chroma_path,
    )

    print(f"✅ Vector store criado com {len(chunks)} chunks")
    print(f"   Persistido em: {chroma_path}")
    return vector_store


def carregar_vector_store() -> Chroma:
    """
    Carrega o vector store já existente em disco.

    Returns:
        Instância do Chroma carregada do disco
    """
    embeddings = obter_embeddings()
    chroma_path = os.path.abspath(CHROMA_PATH)

    if not os.path.exists(chroma_path):
        raise FileNotFoundError(
            f"Vector store não encontrado em {chroma_path}.\n"
            "Execute criar_vector_store() primeiro."
        )

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=chroma_path,
    )

    print(f"✅ Vector store carregado de: {chroma_path}")
    return vector_store