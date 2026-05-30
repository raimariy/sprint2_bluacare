"""
retriever.py

Configura e executa buscas no vector store.
Retorna os chunks mais relevantes para uma query.
"""

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


def obter_retriever(vector_store: Chroma, k: int = 3):
    """
    Cria um retriever a partir do vector store.

    Args:
        vector_store: instância do Chroma já carregada
        k: número de chunks mais relevantes a retornar

    Returns:
        Retriever configurado
    """
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
    print(f"✅ Retriever configurado (top-{k} documentos por busca)")
    return retriever


def buscar_contexto(query: str, vector_store: Chroma, k: int = 3) -> str:
    """
    Busca os chunks mais relevantes para uma query
    e retorna como texto formatado para o LLM.

    Args:
        query: pergunta ou sintoma do usuário
        vector_store: instância do Chroma
        k: número de resultados

    Returns:
        Texto com os chunks relevantes concatenados
    """
    retriever = obter_retriever(vector_store, k=k)
    docs: list[Document] = retriever.invoke(query)

    if not docs:
        return ""

    partes = []
    for i, doc in enumerate(docs, 1):
        fonte = doc.metadata.get("source", "desconhecido")
        partes.append(f"[Fonte {i}: {fonte}]\n{doc.page_content}")

    contexto = "\n\n---\n\n".join(partes)
    return contexto